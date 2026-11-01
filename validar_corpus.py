"""Reconciliação independente de contagens; não certifica classificação semântica."""
import argparse
import hashlib
import importlib.util
import io
import json
import zipfile
from collections import Counter
from pathlib import Path
from motor import analyze, ENGINE_SHA256

DAY='25/10/2026'


def direct_count(raw):
    # Implementação separada do leitor e do classificador de produção.
    blocks=[]
    def visit(data):
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for name in z.namelist():
                if name.lower().endswith(('.jez','.logjez')):visit(z.read(name))
                elif name.lower().endswith('logd.dat'):blocks.append(z.read(name))
    visit(raw)
    distinct=set(blocks)
    if len(distinct)!=1:
        return None  # Não presume continuidade entre origens.
    counts=Counter()
    for line in next(iter(distinct)).decode('latin-1').splitlines():
        if not line.startswith(DAY+' '):continue
        p=line.split('\t')
        if len(p)!=6:return None
        if p[4]=='Eleitor foi habilitado':counts['habilitacoes']+=1
        elif p[4]=='O voto do eleitor foi computado':counts['votos_computados']+=1
    return counts


def validate(folder, destination):
    old_path=Path(__file__).parent/'validacao/motor_v21_referencia.py'
    spec=importlib.util.spec_from_file_location('reference_v21',old_path)
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    totals=Counter();prior=Counter();failures=[];files=[];reconciled=0
    for p in sorted(folder.glob('*.jez')):
        raw=p.read_bytes();row,_,warnings,ss,_=analyze(p.name,raw,DAY)
        previous=old.analyze(p.name,raw,DAY)[0]
        for key in ('habilitacoes','votos_computados','votos_vinculados','indefinida','avisos','suspensas_sem_voto','canceladas_sem_voto','ciclos_sem_desfecho_explicado','votos_sem_habilitacao'):
            totals[key]+=row.get(key,0);prior[key]+=previous.get(key,0)
        counts=direct_count(raw)
        if counts is not None:
            reconciled+=1
            for key in ('habilitacoes','votos_computados'):
                if row[key]!=counts[key]:failures.append({'arquivo':p.name,'erro':'contagem_independente','campo':key,'esperado':counts[key],'obtido':row[key]})
        # Conferência dos balanços a partir dos ciclos efetivamente exportados.
        linked=sum(s['desfecho']=='voto_computado' for s in ss)
        canceled=sum(s['desfecho'] in ('suspensa_sem_voto','cancelada_sem_voto') for s in ss)
        unresolved=sum(s['desfecho'] not in ('voto_computado','suspensa_sem_voto','cancelada_sem_voto') for s in ss)
        if linked+canceled+unresolved!=row['habilitacoes'] or linked+row['votos_sem_habilitacao']!=row['votos_computados']:
            failures.append({'arquivo':p.name,'erro':'conservacao'})
        files.append({'arquivo':p.name,'sha256':hashlib.sha256(raw).hexdigest(),
            'classificacoes_indefinidas_v21':previous['indefinida'],'classificacoes_indefinidas_v3':row['indefinida'],
            'avisos_v21':previous['avisos'],'avisos_v3':row['avisos'],
            'admissivel_estatistica':row['admissivel_estatistica']})
    result={'sha256_motor':ENGINE_SHA256,'amostras':len(files),'logs_com_contagem_independente':reconciled,
        'totais_v21':dict(prior),'totais_v3':dict(totals),'falhas_reconciliacao':failures,
        'arquivos':files,'acuracia_classificacao_certificada':None,
        'base_referencia_independente_rotulada':False,
        'limitacao':'Amostra de desenvolvimento: casos problemáticos e controles do Amazonas. Concordância de contagens não mede acurácia semântica, não certifica 99,9% e não representa todos os estados.'}
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='arquivos'},ensure_ascii=False,indent=2))
    return bool(failures)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--amostras',type=Path,default=Path('validacao/amostras'))
    p.add_argument('--saida',type=Path,default=Path('validacao/resultado_corpus.json'))
    a=p.parse_args();raise SystemExit(validate(a.amostras,a.saida))
