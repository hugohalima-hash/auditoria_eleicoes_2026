import csv,json,collections
from pathlib import Path
from datetime import datetime
from statistics import median,quantiles
base=Path(__file__).parent;rows=list(csv.DictReader(open(base/'votacoes_verificacao.csv',encoding='utf-8-sig')));profile=list(csv.DictReader(open(base/'totais_por_secao.csv',encoding='utf-8-sig')));original=list(csv.DictReader(open(base.parent/'dados/resultados/AC/urnas.csv',encoding='utf-8-sig')))
allowed={'mesario_explicito','digital_mesario_gravada','digital_mesario_sem_associacao','ano_nascimento_sem_evento_biometrico'}
def stamp(x):return datetime.strptime(x,'%d/%m/%Y %H:%M:%S')
sequences=[]
for group in ['mesario','conjunto']:
 current=[];previous=None
 def flush():
  if len(current)<2:return
  first,last=current[0],current[-1];gaps=[int(x['intervalo_habilitacoes_seg']) for x in current[1:]]
  sequences.append({'municipio':first['municipio'],'zona':first['zona'],'secao':first['secao'],'arquivo':first['arquivo'],'grupo':group,'votacoes':len(current),'inicio':first['habilitacao'],'ultima_habilitacao':last['habilitacao'],'ultimo_voto_computado':last['voto_computado'],'intervalo_medio_habilitacoes_seg':sum(gaps)/len(gaps),'menor_intervalo_habilitacoes_seg':min(gaps),'maior_intervalo_habilitacoes_seg':max(gaps)})
 for r in rows:
  good=group=='conjunto' or r['grupo']=='mesario'
  consecutive=bool(previous and previous['arquivo']==r['arquivo'] and previous['origem']==r['origem'] and r['tipo_anterior'] in allowed and r['intervalo_habilitacoes_seg'] and (stamp(r['habilitacao'])-stamp(previous['habilitacao'])).total_seconds()==int(r['intervalo_habilitacoes_seg']))
  if group=='mesario':consecutive=consecutive and previous['grupo']=='mesario' if previous else False
  if not good or not consecutive:
   flush();current=[]
  if good:current.append(r)
  previous=r
 flush()
for group,col in [('mesario','maior_sequencia_com_voto_mesario'),('conjunto','maior_sequencia_com_voto_sem_biometria')]:
 maxima=collections.defaultdict(int)
 for r in sequences:
  if r['grupo']==group:maxima[r['arquivo']]=max(maxima[r['arquivo']],r['votacoes'])
 for r in original:
  expected=int(r[col]);got=maxima[r['arquivo']]
  if expected<2:assert got==0
  else:assert got==expected,(r['arquivo'],group,got,expected)
with (base/'sequencias_concluidas.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(sequences[0]));w.writeheader();w.writerows(sequences)
flagged=list(csv.DictReader(open(base/'secoes_proporcao_elevada_combinada.csv',encoding='utf-8-sig')));fs={r['arquivo'] for r in flagged};fast=[r for r in rows if int(r['duracao_seg'])<=10];idlefast=[r for r in fast if r['pausa_apos_voto_anterior_seg'] and int(r['pausa_apos_voto_anterior_seg'])>=300]
result={'votacoes_conjunto':len(rows),'secoes_com_votacoes_conjunto':sum(int(r['total_verificacao'])>0 for r in profile),'secoes_proporcao_elevada':len(flagged),'votacoes_conjunto_nessas_secoes':sum(int(r['total_verificacao']) for r in flagged),'votacoes_totais_nessas_secoes':sum(int(r['votos_computados']) for r in flagged),'ate_10_segundos':len(fast),'ate_10_segundos_apos_pausa_5min':len(idlefast),'secoes_com_caso_apos_pausa':len({r['arquivo'] for r in idlefast}),'secoes_com_concentracao_e_caso_apos_pausa':len(fs & {r['arquivo'] for r in idlefast}),'casos_apos_pausa_nas_secoes_concentradas':sum(r['arquivo'] in fs for r in idlefast),'sequencias':{g:{'ge2':sum(r['grupo']==g for r in sequences),'ge3':sum(r['grupo']==g and r['votacoes']>=3 for r in sequences),'ge5':sum(r['grupo']==g and r['votacoes']>=5 for r in sequences),'maximo':max(r['votacoes'] for r in sequences if r['grupo']==g)} for g in ['mesario','conjunto']}}
(base/'indicadores_foco.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
for g in ['mesario','conjunto']:
 print('topseries',g,sorted([r for r in sequences if r['grupo']==g],key=lambda x:-x['votacoes'])[:2])
