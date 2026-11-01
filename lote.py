"""Execução estadual, download retomável por faixas e cobertura oficial."""
import concurrent.futures as cf
import hashlib
import json
import multiprocessing
import os
import re
import shutil
import sqlite3
import time
import urllib.request
import zipfile
from pathlib import Path
from motor import analyze, section, summarize, write_csv, VERSION, CACHE_VERSION, ENGINE_SHA256
from integridade import manifest, verified

UFS='AC AL AM AP BA CE DF ES GO MA MG MS MT PA PB PE PI PR RJ RN RO RR RS SC SE SP TO ZZ'.split()
URL='https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2026/arqurnatot/bu_imgbu_logjez_rdv_vscmr_2026_2t_{uf}.zip'
_WORKER_ARCHIVES={}
MIN_FREE_BYTES=6*1024*1024*1024

class DiskBudgetError(RuntimeError):
    pass

def analyze_member(task):
    """Cada processo abre o índice ZIP uma vez; não transfere logs por IPC."""
    path,name,day=task
    try:
        if path not in _WORKER_ARCHIVES:
            _WORKER_ARCHIVES[path]=zipfile.ZipFile(path)
        raw=_WORKER_ARCHIVES[path].read(name)
        row,runs,warnings,_,_=analyze(name,raw,day)
        return name,row,runs,warnings,None
    except Exception as e:
        return name,None,None,None,f'{type(e).__name__}: {e}'

def worker_memory_limit():
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_AS,(768*1024*1024,768*1024*1024))
    except ImportError:
        pass

def bounded_results(pool,tasks,limit):
    iterator=iter(tasks)
    pending=set()
    for _ in range(limit):
        try:pending.add(pool.submit(analyze_member,next(iterator)))
        except StopIteration:break
    while pending:
        done,pending=cf.wait(pending,return_when=cf.FIRST_COMPLETED)
        for future in done:
            yield future.result()
            try:pending.add(pool.submit(analyze_member,next(iterator)))
            except StopIteration:pass

def request(url,headers=None,method='GET'):
    return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AuditorEleitoralIndependente/2.0',
        'Accept-Encoding':'identity',**(headers or {})},method=method),timeout=45)

def atomic_json(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(path.suffix+'.tmp')
    temp.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
    os.replace(temp,path)

def download(uf,dest,workers=4):
    url=URL.format(uf=uf)
    dest.mkdir(parents=True,exist_ok=True)
    path=dest/url.rsplit('/',1)[-1]
    if path.exists() and zipfile.is_zipfile(path):
        return path
    with request(url,method='HEAD') as resp:
        size=int(resp.headers['Content-Length']); etag=resp.headers.get('ETag','')
    partial=path.with_suffix('.range.part')
    state=path.with_suffix('.range.json')
    chunk=16*1024*1024
    old=json.loads(state.read_text()) if state.exists() else {}
    if old.get('size')!=size or old.get('etag')!=etag or old.get('chunk')!=chunk:
        old={'size':size,'etag':etag,'chunk':chunk,'done':[],'url':url}
        with open(partial,'wb') as f:
            f.truncate(size)
        atomic_json(state,old)
    elif not partial.exists():
        old['done']=[]
        with open(partial,'wb') as f:f.truncate(size)
    done=set(old['done']);n=(size+chunk-1)//chunk
    fd=os.open(partial,os.O_RDWR)
    def get(indices):
        a=indices[0]*chunk;b=min(size,(indices[-1]+1)*chunk)
        error=None
        for retry in range(4):
            try:
                if shutil.disk_usage(dest).free < MIN_FREE_BYTES+(b-a):
                    raise DiskBudgetError('reserva mínima de 6 GiB atingida; download suspenso sem preencher o disco')
                with request(url,{'Range':f'bytes={a}-{b-1}','If-Range':etag}) as resp:
                    expected=f'bytes {a}-{b-1}/{size}'
                    if resp.status!=206 or resp.headers.get('Content-Range')!=expected:
                        raise ValueError('servidor não confirmou faixa '+expected)
                    data=resp.read(b-a+1)
                    if len(data)!=b-a:raise ValueError('faixa truncada')
                pos=0
                if hasattr(os,'pwrite'):
                    while pos<len(data):pos+=os.pwrite(fd,data[pos:],a+pos)
                else:
                    # Windows: cada thread usa seu próprio cursor de arquivo.
                    with open(partial,'r+b',buffering=0) as writer:
                        writer.seek(a)
                        while pos<len(data):pos+=writer.write(data[pos:])
                return indices
            except DiskBudgetError:
                raise
            except Exception as e:
                error=e
        raise RuntimeError(f'faixas {indices}: {error}')
    last=time.monotonic()
    print(f'{uf}: download {size/1e9:.2f} GB, {len(done)}/{n} blocos existentes',flush=True)
    try:
        with cf.ThreadPoolExecutor(max_workers=workers) as pool:
            missing=[i for i in range(n) if i not in done]
            batches=[]
            for i in missing:
                if batches and len(batches[-1])<2 and i==batches[-1][-1]+1:
                    batches[-1].append(i)
                else:
                    batches.append([i])
            futures=[pool.submit(get,indices) for indices in batches]
            for future in cf.as_completed(futures):
                done.update(future.result());old['done']=sorted(done)
                os.fsync(fd);atomic_json(state,old)
                if time.monotonic()-last>20:
                    print(f'{uf}: download {len(done)}/{n} blocos ({100*len(done)/n:.1f}%)',flush=True)
                    last=time.monotonic()
        os.fsync(fd)
    finally:
        os.close(fd);old['done']=sorted(done);atomic_json(state,old)
    if not zipfile.is_zipfile(partial):
        # Um checkpoint de download não substitui a validação do arquivo.
        # Invalida as faixas para que a próxima execução faça a coleta de novo.
        old['done']=[]
        old['last_error']='ZIP inválido após download; faixas invalidadas'
        atomic_json(state,old)
        with open(partial,'wb') as f:f.truncate(size)
        raise ValueError(old['last_error'])
    os.replace(partial,path)
    return path

def config_state(uf,out):
    target=out/'config_oficial.json'
    url=f'https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3221/config/{uf.lower()}/{uf.lower()}-p003221-cs.json'
    if target.exists():data=json.loads(target.read_text())
    else:
        with request(url) as resp:data=json.load(resp)
        atomic_json(target,data)
    sections={};aggregated=[]
    for abr in data.get('abr',[]):
        for mun in abr.get('mu',[]):
            for zona in mun.get('zon',[]):
                for sec in zona.get('sec',[]):
                    key=(str(mun['cd']).zfill(5),str(zona['cd']).zfill(4),str(sec['ns']).zfill(4))
                    if sec.get('nsp'):
                        aggregated.append(key)
                    else:sections[key]=mun.get('nm','')
    if not sections:raise ValueError('configuração oficial não contém seções principais')
    return sections,aggregated,url

def process_archive(path,out,day,uf='LOCAL',keep_events=False,processes=1):
    out.mkdir(parents=True,exist_ok=True)
    (out/'manifesto.json').unlink(missing_ok=True)
    con=sqlite3.connect(out/'checkpoint.sqlite')
    con.execute('CREATE TABLE IF NOT EXISTS results (name TEXT PRIMARY KEY, crc INTEGER, size INTEGER, version TEXT, day TEXT, row TEXT, runs TEXT, warnings TEXT)')
    con.execute('CREATE TABLE IF NOT EXISTS errors (name TEXT PRIMARY KEY, message TEXT)')
    start=time.monotonic();processed=0;fresh=0
    if path.suffix.lower() in ('.jez','.logjez'):
        archive=None;infos=[None]
    else:
        archive=zipfile.ZipFile(path)
        infos=[i for i in archive.infolist() if i.filename.lower().endswith(('.jez','.logjez'))]
    try:
        if not infos:raise ValueError('pacote sem logs de urna')
        print(f'{uf}: analisando {len(infos)} logs',flush=True)
        tasks=[]
        for info in infos:
            name=info.filename if info else path.name
            crc=info.CRC if info else -1
            size=info.file_size if info else path.stat().st_size
            previous=con.execute('SELECT crc,size,version,day FROM results WHERE name=?',(name,)).fetchone()
            if previous==(crc,size,CACHE_VERSION,day):
                processed+=1;continue
            tasks.append(info)
        def sequential():
            for info in tasks:
                name=info.filename if info else path.name
                try:
                    raw=archive.read(info) if archive else path.read_bytes()
                    row,runs,warnings,sessions,meta=analyze(name,raw,day)
                    if keep_events:
                        with open(out/'habilitacoes.jsonl','a',encoding='utf-8') as f:
                            for s in sessions:
                                f.write(json.dumps({'arquivo':name,**{k:v for k,v in s.items() if k!='urna'}},ensure_ascii=False)+'\n')
                    yield name,row,runs,warnings,None
                except Exception as e:
                    yield name,None,None,None,f'{type(e).__name__}: {e}'
        pool=None
        if archive and not keep_events and processes>1:
            pool=cf.ProcessPoolExecutor(max_workers=processes,mp_context=multiprocessing.get_context('spawn'),initializer=worker_memory_limit)
            results=bounded_results(pool,((str(path.resolve()),i.filename,day) for i in tasks),processes*12)
        else:
            results=sequential()
        info_by_name={i.filename if i else path.name:i for i in tasks}
        for name,row,runs,warnings,error in results:
            info=info_by_name[name]
            crc=info.CRC if info else -1
            size=info.file_size if info else path.stat().st_size
            try:
                if error:raise ValueError(error)
                con.execute('INSERT OR REPLACE INTO results VALUES (?,?,?,?,?,?,?,?)',
                    (name,crc,size,CACHE_VERSION,day,json.dumps(row,ensure_ascii=False),json.dumps(runs,ensure_ascii=False),json.dumps(warnings,ensure_ascii=False)))
                con.execute('DELETE FROM errors WHERE name=?',(name,))
                fresh+=1
            except Exception as e:
                con.execute('INSERT OR REPLACE INTO errors VALUES (?,?)',(name,str(e)))
            processed+=1
            if processed%100==0:
                con.commit()
            if processed%1000==0:
                print(f'{uf}: {processed}/{len(infos)} logs, {time.monotonic()-start:.0f}s',flush=True)
                atomic_json(out/'progresso.json',{'status':'processando','total_logs_pacote':len(infos),'processados':processed,'versao':VERSION})
        if pool:
            pool.shutdown()
        con.commit()
        names={i.filename if i else path.name for i in infos}
        rows=[];runs=[];warnings=[];errors=[]
        for name,row,rs,ws in con.execute('SELECT name,row,runs,warnings FROM results WHERE version=? AND day=?',(CACHE_VERSION,day)):
            if name in names:
                rows.append(json.loads(row));runs.extend(json.loads(rs))
                warnings.extend({'arquivo':name,**w} for w in json.loads(ws))
        errors=[{'arquivo':n,'erro':m} for n,m in con.execute('SELECT name,message FROM errors') if n in names]
        rows.sort(key=lambda r:r['arquivo'])
        write_csv(out/'urnas.csv',rows)
        write_csv(out/'sequencias.csv',sorted(runs,key=lambda x:(-x['tamanho'],x['arquivo'],x['grupo'])))
        write_csv(out/'avisos.csv',warnings,['arquivo','codigo','origem','linha'])
        write_csv(out/'erros.csv',errors,['arquivo','erro'])
        result=summarize(rows,errors,day)
        result.update({'uf':uf,'logs_no_pacote':len(infos),'tempo_processamento_seg':round(time.monotonic()-start,2),'fonte':str(path.name)})
        observed={tuple(r.get(k,'') for k in ['municipio','zona','secao']) for r in rows}
        inventory={}
        if archive:
            for n in archive.namelist():
                sec=section(n)
                if sec:
                    key=tuple(sec[k] for k in ['municipio','zona','secao'])
                    inventory.setdefault(key,set()).add(sec['tipo_arquivo'])
        result['secoes_distintas_com_log_processado']=len(observed)
        result['secoes_distintas_no_pacote']=len(inventory)
        result['secoes_pacote_sem_log_processado']=len(set(inventory)-observed)
        missing=[]
        for key in sorted(set(inventory)-observed):missing.append({'municipio':key[0],'zona':key[1],'secao':key[2],'motivo':'consta_pacote_sem_log_processado'})
        if uf!='LOCAL':
            try:
                expected,aggr,url=config_state(uf,out)
                result.update({'secoes_principais_config_oficial':len(expected),'secoes_agregadas_config_oficial':len(aggr),
                    'secoes_oficiais_com_log_processado':len(set(expected)&observed),
                    'secoes_config_sem_log_processado':len(set(expected)-observed),
                    'secoes_processadas_fora_config':len(observed-set(expected)),
                    'cobertura_config_pct':100*len(set(expected)&observed)/len(expected),
                    'url_config':url})
                for key in sorted(set(expected)-observed):missing.append({'municipio':key[0],'zona':key[1],'secao':key[2],'motivo':'config_oficial_sem_log_processado'})
            except Exception as e:
                result['erro_cobertura_oficial']=str(e)
        write_csv(out/'lacunas_cobertura.csv',missing,['municipio','zona','secao','motivo'])
        result['status']='processado_com_ressalvas' if errors or missing or result['indefinida'] or result.get('erro_cobertura_oficial') or result['avisos'] or result['arquivos_em_quarentena'] else 'processado'
        atomic_json(out/'resumo.json',result)
        atomic_json(out/'manifesto.json',manifest(out,ENGINE_SHA256))
        atomic_json(out/'progresso.json',{'status':result['status'],'processados':len(rows),'total_logs_pacote':len(infos)})
        print(f"{uf}: FINALIZADO logs={len(rows)} erros={len(errors)} "
              f"cobertura={result.get('cobertura_config_pct','NA')}% "
              f"mesario={result['com_evento_mesario']} indefinidas={result['indefinida']} "
              f"maior_serie_mesario={result['maior_sequencia_mesario']}",flush=True)
        return result
    finally:
        if 'pool' in locals() and pool:
            pool.shutdown(wait=True,cancel_futures=True)
        if archive:archive.close()
        con.close()

def execute_state(uf,root,downloads,day,workers,delete=False,processes=1):
    out=root/uf
    try:
        saved=out/'resumo.json'
        if saved.exists():
            result=json.loads(saved.read_text())
            if (result.get('versao_motor')==VERSION and result.get('data')==day
                    and result.get('sha256_motor')==ENGINE_SHA256
                    and verified(out,ENGINE_SHA256)
                    and result.get('erros')==0
                    and result.get('arquivos_processados')==result.get('logs_no_pacote')
                    and (out/'urnas.csv').exists() and (out/'sequencias.csv').exists()):
                print(f'{uf}: resultado já processado nesta versão; reutilizando checkpoint completo',flush=True)
                return result
        error=None
        for retry in range(3):
            try:
                path=download(uf,downloads,workers)
                error=None
                break
            except Exception as e:
                error=e
                print(f'{uf}: tentativa de download {retry+1} falhou: {e}',flush=True)
                if isinstance(e,DiskBudgetError):
                    break
        if error:
            raise error
        result=process_archive(path,out,day,uf,processes=processes)
        result['url_pacote']=URL.format(uf=uf)
        result['tamanho_pacote_bytes']=path.stat().st_size
        # Hash completo do pacote não é necessário para conferir CRC dos membros;
        # SHA-256 de cada log é registrado. Nenhuma assinatura é autenticada.
        atomic_json(out/'resumo.json',result)
        atomic_json(out/'manifesto.json',manifest(out,ENGINE_SHA256))
        if delete and not result['erros']:
            path.unlink()
        return result
    except Exception as e:
        result={'uf':uf,'status':'falhou','erro':str(e),'data':day}
        atomic_json(out/'falha.json',result)
        print(json.dumps(result,ensure_ascii=False),flush=True)
        return result

def main(args):
    root=args.saida;root.mkdir(parents=True,exist_ok=True)
    states=UFS if args.brasil else args.ufs or []
    if not states and not args.arquivos:
        raise SystemExit('informe --brasil, --ufs ou --arquivos')
    if args.data!='25/10/2026' and states:
        raise SystemExit('download v2 restrito ao segundo turno de 25/10/2026; use --arquivos para outra data')
    allresults=[]
    for i,path in enumerate(args.arquivos):
        allresults.append(process_archive(path,root/('LOCAL_'+str(i+1)),args.data,keep_events=args.eventos,processes=args.processos))
    with cf.ThreadPoolExecutor(max_workers=args.estados_simultaneos) as pool:
        futures={pool.submit(execute_state,uf,root,args.pasta_download,args.data,args.conexoes,args.apagar_pacotes,args.processos):uf for uf in states}
        for future in cf.as_completed(futures):
            result=future.result();allresults.append(result)
            atomic_json(root/'andamento_nacional.json',{'ufs_solicitadas':states,'ufs_concluidas':[r.get('uf') for r in allresults if r.get('status')!='falhou'],
                'resultados':allresults,'atualizacao_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())})
    atomic_json(root/'resumo_estados.json',sorted(allresults,key=lambda r:r.get('uf','')))
    fields=list(dict.fromkeys(k for r in allresults for k in r))
    write_csv(root/'resumo_estados.csv',allresults,fields)
    return 1 if any(r.get('status')=='falhou' for r in allresults) else 0
