import sys,csv,json,zipfile,hashlib
from pathlib import Path
from collections import Counter,defaultdict
from statistics import mean,median
base=Path(__file__).resolve().parents[1];repo=base.parents[1];sys.path.insert(0,str(repo))
from motor import extract,read_logs,seconds,MESARIO,ENGINE_SHA256
out=Path(__file__).parent;data=base/'dados';src=repo/'downloads/bu_imgbu_logjez_rdv_vscmr_2026_2t_AC.zip'
assert hashlib.file_digest(src.open('rb'),'sha256').hexdigest()=='7e58076367c9a0d8002b7918fe33183a2aee8aaf562d32555cf62ce10d188dc5'
assert hashlib.file_digest((data/'publicado.zip').open('rb'),'sha256').hexdigest()=='e72a82e0720f62bfc7a682946f4cda37fcbeb94aa22bf94e06d6fb7ed5ab1d95'
profiles=list(csv.DictReader(open(data/'resultados/AC/urnas.csv',encoding='utf-8-sig')));cfg=json.loads((data/'resultados/AC/config_oficial.json').read_text());names={str(m['cd']).zfill(5):m['nm'] for a in cfg['abr'] for m in a.get('mu',[])}
assert ENGINE_SHA256==json.loads((data/'resultados/AC/resumo.json').read_text())['sha256_motor']
def group(s):return 'mesario' if s['tipo'] in MESARIO else 'ano' if s['tipo']=='ano_nascimento_sem_evento_biometrico' else 'biometrica' if s['tipo']=='biometrica' else 'outro'
def q(a,p):
 a=sorted(a);x=(len(a)-1)*p;j=int(x);return a[j]+(a[min(j+1,len(a)-1)]-a[j])*(x-j)
def stat(a):return dict(n=len(a),media=mean(a),mediana=median(a),p10=q(a,.1),p90=q(a,.9),minimo=min(a),maximo=max(a)) if a else {'n':0}
def write(name,rows):
 if not rows:return
 with (out/name).open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
all_sessions={};pairs=[];seqs=[];bio=defaultdict(list);counts=Counter();releases=Counter();sectionstats=[]
with zipfile.ZipFile(src) as z:
 for i,r in enumerate(profiles):
  filename=r['arquivo'];ss,warning,meta=extract(z.read(filename),'25/10/2026');all_sessions[filename]=ss
  assert len(ss)==int(r['habilitacoes']) and meta['votos_computados']==int(r['votos_computados'])
  for s in ss:releases[group(s)]+=1;counts[group(s)]+='voto' in s
  common=dict(municipio=names[r['municipio']],zona=r['zona'],secao=r['secao'],arquivo=filename,admissivel=r['admissivel_estatistica'])
  for a,b in zip(ss,ss[1:]):
   if a['epoca']!=b['epoca'] or a['origem']!=b['origem'] or a['urna']!=b['urna']:continue
   gap=b['seg']-a['seg'];assert gap>=0
   row=dict(**common,origem=a['origem'],urna=a['urna'],epoca=a['epoca'],liberacao_anterior=a['hora'],liberacao_seguinte=b['hora'],intervalo_seg=gap,tipo_anterior=group(a),tipo_seguinte=group(b),tipo_detalhado_anterior=a['tipo'],tipo_detalhado_seguinte=b['tipo'],anterior_com_voto='voto' in a,seguinte_com_voto='voto' in b,linha_anterior=a['linha'],linha_seguinte=b['linha'],autorizacao_anterior=a['autorizacao'],autorizacao_seguinte=b['autorizacao'],intervalo_autorizacoes_seg=seconds(b['autorizacao'])-seconds(a['autorizacao']) if a['autorizacao'] and b['autorizacao'] else '')
   pairs.append(row)
   if 'voto' in a and 'voto' in b and group(a)==group(b)=='biometrica':bio[filename].append(gap)
  for mode in ['mesario','conjunto']:
   for completed in [True,False]:
    current=[]
    def flush():
     if len(current)<2:return
     gaps=[b['seg']-a['seg'] for a,b in zip(current,current[1:])]
     seqs.append(dict(**common,id=f'{filename}:{mode}:{completed}:{current[0]["linha"]}',grupo=mode,apenas_concluidas=completed,liberacoes=len(current),votos=sum('voto' in s for s in current),mesario=sum(group(s)=='mesario' for s in current),ano=sum(group(s)=='ano' for s in current),inicio=current[0]['hora'],fim=current[-1]['hora'],origem=current[0]['origem'],urna=current[0]['urna'],epoca=current[0]['epoca'],linha_inicio=current[0]['linha'],linha_fim=current[-1]['linha'],linha_ultimo_desfecho=current[-1]['linha_desfecho'],horarios=' | '.join(s['hora'][11:] for s in current),tipos=' | '.join(group(s) for s in current),intervalos_seg=' | '.join(str(x) for x in gaps),media_seg=mean(gaps),mediana_seg=median(gaps),minimo_seg=min(gaps),maximo_seg=max(gaps)))
    for s in ss:
     good=(group(s)=='mesario' if mode=='mesario' else group(s) in ('mesario','ano')) and (not completed or 'voto' in s)
     continuous=not current or (s['epoca']==current[-1]['epoca'] and s['origem']==current[-1]['origem'] and s['urna']==current[-1]['urna'])
     if not good or not continuous:flush();current=[]
     if good:current.append(s)
    flush()
  if i%500==0:print(i,flush=True)
for seq in seqs:
 ref=bio[seq['arquivo']];seq['pares_biometricos_secao']=len(ref)
 for key in ['media','mediana','p10']:seq['biometrica_'+key+'_seg']=stat(ref).get(key,'')
 seq['percentual_da_media_biometrica']=100*seq['media_seg']/mean(ref) if ref else ''
 seq['percentil_intervalo_medio_na_biometria']=100*sum(x<=seq['media_seg'] for x in ref)/len(ref) if ref else ''
 seq['triagem_ritmo']=seq['apenas_concluidas'] and seq['liberacoes']>=3 and seq['admissivel']=='True' and len(ref)>=30 and seq['media_seg']<q(ref,.1)
for r in profiles:
 ref=bio[r['arquivo']];sectionstats.append(dict(municipio=names[r['municipio']],zona=r['zona'],secao=r['secao'],arquivo=r['arquivo'],**stat(ref)))
write('01_intervalos_todos.csv',pairs);write('02_sequencias.csv',seqs);write('03_referencia_biometrica_secao.csv',sectionstats)
summary={'motor':ENGINE_SHA256,'total_liberacoes':dict(releases),'total_votos':dict(counts),'pares_por_transicao':{},'sequencias':{},'criterio_ritmo':'Sequência concluída com >=3 liberações, seção admissível, >=30 pares biométricos B->B na própria seção, média dos intervalos inferior ao percentil 10 desses pares. Triagem exploratória, não prova de fraude.'}
for key,types in [('bio_bio',('biometrica','biometrica')),('mes_mes',('mesario','mesario')),('ano_ano',('ano','ano')),('bio_mes',('biometrica','mesario'))]:
 summary['pares_por_transicao'][key]=stat([r['intervalo_seg'] for r in pairs if (r['tipo_anterior'],r['tipo_seguinte'])==types and r['anterior_com_voto'] and r['seguinte_com_voto']])
for g in ['mesario','conjunto']:
 a=[s for s in seqs if s['grupo']==g and s['apenas_concluidas']];summary['sequencias'][g]={'ge2':len(a),'ge3':sum(s['liberacoes']>=3 for s in a),'maximo':max(s['liberacoes'] for s in a),'secoes_ge2':len({s['arquivo'] for s in a}),'secoes_ge3':len({s['arquivo'] for s in a if s['liberacoes']>=3}),'triadas_ritmo':sum(s['triagem_ritmo'] for s in a),'top_quantidade':sorted(a,key=lambda s:(-s['liberacoes'],s['media_seg']))[:5],'top_rapidez_ge3':sorted([s for s in a if s['liberacoes']>=3],key=lambda s:s['media_seg'])[:5]}
(out/'resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False,indent=2))
# Preserve complete source logs and unabridged chronological windows for all selected sequences.
selected=[s for s in seqs if s['apenas_concluidas'] and (s['triagem_ritmo'] or s in summary['sequencias'][s['grupo']]['top_quantidade'][:2] or s in summary['sequencias'][s['grupo']]['top_rapidez_ge3'][:2])]
for idx,s in enumerate(selected,1):s['caso']=f'C{idx:02}';s['log_trecho']=f'logs/{s["caso"]}_trecho_integral.txt'
write('04_casos_destacados.csv',selected)
logdir=out/'logs';logdir.mkdir(exist_ok=True)
with zipfile.ZipFile(src) as z:
 for s in selected:
  raw=z.read(s['arquivo']);lines,_,_=read_logs(raw);lines=[(ln,line) for origin,ln,line in lines if origin==s['origem']]
  ss=all_sessions[s['arquivo']];first=next(x for x in ss if x['linha']==s['linha_inicio'] and x['origem']==s['origem']);prev=[x for x in ss if x['origem']==s['origem'] and x['epoca']==s['epoca'] and x['linha']<first['linha']];lo=prev[-1]['linha_desfecho'] if prev else max(1,first['linha']-60)
  # Include the full next identification attempt leading to the first habilitation.
  hi=s['linha_ultimo_desfecho'];segment=[(ln,line) for ln,line in lines if lo<=ln<=hi]
  header=f"{s['caso']} | {s['municipio']} | Zona {s['zona']} | Seção {s['secao']}\nArquivo: {s['arquivo']}\nOrigem: {s['origem']}\nLinhas {lo}-{hi}, sem omitir eventos intermediários. Prefixo numérico = linha original.\n\n"
  (out/s['log_trecho']).write_text(header+'\n'.join(f'{ln:06d}\t{line}' for ln,line in segment)+'\n')
  (logdir/s['arquivo']).write_bytes(raw)
write('04_casos_destacados.csv',selected)
