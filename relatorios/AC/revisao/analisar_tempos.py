import csv,json,zipfile,sys,hashlib
from pathlib import Path
from collections import Counter,defaultdict
from statistics import median
base=Path(__file__).resolve().parents[1];repo=next(p for p in [base.parent/'github_project',base.parent.parent,Path.cwd()] if (p/'motor.py').exists());sys.path.insert(0,str(repo))
from motor import extract,seconds,MESARIO,ENGINE_SHA256
root=base/'dados/resultados/AC';profile=list(csv.DictReader(open(root/'urnas.csv',encoding='utf-8-sig')));by={r['arquivo']:r for r in profile};summary=json.loads((root/'resumo.json').read_text());assert ENGINE_SHA256==summary['sha256_motor']
cfg=json.loads((root/'config_oficial.json').read_text());names={str(m['cd']).zfill(5):m['nm'] for a in cfg['abr'] for m in a.get('mu',[])}
source=repo/'downloads/bu_imgbu_logjez_rdv_vscmr_2026_2t_AC.zip'
assert hashlib.file_digest(source.open('rb'),'sha256').hexdigest()==json.loads((base/'dados/conferencias/AC/conferencia.json').read_text())['sha256_pacote']
out=base/'revisao';out.mkdir(exist_ok=True)
fields=['municipio','zona','secao','arquivo','tipo','grupo','habilitacao','voto_computado','duracao_seg','intervalo_habilitacoes_seg','pausa_apos_voto_anterior_seg','tipo_anterior','origem','linha_habilitacao','linha_voto','fora_comparacao_estatistica']
durations=defaultdict(list);counters=defaultdict(Counter);coverage=Counter();totals=Counter();filecounts=[]
# Timing rows include every completed cycle in the target group, not only runs.
with zipfile.ZipFile(source) as archive,(out/'votacoes_verificacao.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for i,name in enumerate(sorted(by),1):
  raw=archive.read(name);r=by[name];ss,warning,meta=extract(raw,'25/10/2026')
  assert len(ss)==int(r['habilitacoes']) and meta['votos_computados']==int(r['votos_computados']),name
  types=Counter(s['tipo'] for s in ss);assert all(types[k]==int(r[k]) for k in types),name
  previous=None;cnt=Counter()
  for session in ss:
   if 'voto' in session:
    dur=seconds(session['voto'])-session['seg'];assert dur>=0
    group='mesario' if session['tipo'] in MESARIO else 'ano_nascimento' if session['tipo']=='ano_nascimento_sem_evento_biometrico' else 'biometrica' if session['tipo']=='biometrica' else 'outro'
    durations[group].append(dur);durations['todos'].append(dur);totals[group]+=1;cnt[group]+=1
    for limit in [5,10,15,20,30]:counters[group]['duracao_ate_'+str(limit)]+=dur<=limit
    gap=idle='';prior=''
    if previous is not None and 'voto' in previous and previous['epoca']==session['epoca']:
     gap=session['seg']-previous['seg'];idle=session['seg']-seconds(previous['voto']);assert gap>=0 and idle>=0,(name,gap,idle)
     prior=previous['tipo']
     if group in ('mesario','ano_nascimento'):
      coverage[group]+=1
      for limit in [15,30,60]:counters[group]['intervalo_habilitacoes_ate_'+str(limit)]+=gap<=limit
      for limit in [300,600]:
       counters[group]['pausa_anterior_ge_'+str(limit)]+=idle>=limit
       counters[group]['pausa_ge_'+str(limit)+'_e_duracao_ate_10']+=idle>=limit and dur<=10
    if group in ('mesario','ano_nascimento'):
     w.writerow(dict(municipio=names[r['municipio']],zona=r['zona'],secao=r['secao'],arquivo=name,tipo=session['tipo'],grupo=group,habilitacao=session['hora'],voto_computado=session['voto'],duracao_seg=dur,intervalo_habilitacoes_seg=gap,pausa_apos_voto_anterior_seg=idle,tipo_anterior=prior,origem=session['origem'],linha_habilitacao=session['linha'],linha_voto=session['linha_desfecho'],fora_comparacao_estatistica=r['admissivel_estatistica']!='True'))
   previous=session
  filecounts.append({'municipio':names[r['municipio']],'zona':r['zona'],'secao':r['secao'],'arquivo':name,'votos_computados':int(r['votos_computados']),'votos_com_evento_mesario':cnt['mesario'],'votos_com_ano_nascimento':cnt['ano_nascimento'],'total_verificacao':cnt['mesario']+cnt['ano_nascimento'],'percentual_verificacao':100*(cnt['mesario']+cnt['ano_nascimento'])/int(r['votos_computados']) if int(r['votos_computados']) else 0,'fora_comparacao_estatistica':r['admissivel_estatistica']!='True'})
  if i%500==0:print('Tempos:',i,'/',len(by),flush=True)
def q(values,p):
 s=sorted(values);x=(len(s)-1)*p;j=int(x);return s[j]+(s[min(j+1,len(s)-1)]-s[j])*(x-j)
report={'motor_sha256':ENGINE_SHA256,'logs':len(by),'totais':dict(totals),'contagens_tempos':{g:dict(c) for g,c in counters.items()},'ciclos_com_intervalo_anterior_avaliavel':dict(coverage),'distribuicao_duracao':{g:{'n':len(v),'minimo':min(v),'p10':q(v,.1),'mediana':median(v),'p90':q(v,.9),'maximo':max(v)} for g,v in durations.items()},'observacao':'Intervalos são diferenças entre mensagens do log, em segundos inteiros. Não demonstram presença do eleitor, identidade, escolha ou fraude. Intervalos entre ciclos não cruzam origens, equipamentos ou ciclos sem voto computado.'}
assert totals['mesario']==22654 and totals['ano_nascimento']==15325 and sum(totals.values())==453654
(out/'resumo_tempos.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
with (out/'totais_por_secao.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=filecounts[0]);w.writeheader();w.writerows(filecounts)
print(json.dumps(report,ensure_ascii=False,indent=2))
