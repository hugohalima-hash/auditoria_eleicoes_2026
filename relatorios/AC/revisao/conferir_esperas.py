import csv,zipfile,sys,json
from pathlib import Path
from collections import defaultdict,Counter
base=Path(__file__).parent;root=base.parent;repo=next(p for p in [root.parent/'github_project',root.parent.parent,Path.cwd()] if (p/'motor.py').exists());sys.path.insert(0,str(repo));from motor import read_logs,seconds
rows=list(csv.DictReader(open(base/'votacoes_verificacao.csv',encoding='utf-8-sig')));grouped=defaultdict(dict)
for r in rows:grouped[r['arquivo']][(r['origem'],int(r['linha_habilitacao']))]=r
fields=list(rows[0])+['aguardando_identificador_desde','identificador_digitado_em','tempo_aguardando_identificador_seg','tempo_da_digitacao_a_habilitacao_seg']
matched=0
with zipfile.ZipFile(repo/'downloads/bu_imgbu_logjez_rdv_vscmr_2026_2t_AC.zip') as z:
 for name,targets in grouped.items():
  wait=ident=None;oldsource=unit=prevsecs=None
  for src,n,line in read_logs(z.read(name))[0]:
   p=line.split('\t')
   if len(p)!=6 or not p[0].startswith('25/10/2026'):wait=ident=None;continue
   stamp,dev,msg=p[0],p[2],p[4];now=seconds(stamp)
   if oldsource!=src or unit!=dev or (prevsecs is not None and now<prevsecs):wait=ident=None
   oldsource,unit,prevsecs=src,dev,now
   if msg.startswith('Aguardando digitação do identificador'):wait=stamp;ident=None
   elif msg=='Identificador do eleitor digitado pelo mesário':ident=stamp
   elif msg.startswith('Habilitação cancelada') or msg=='Mesário cancelou entrada dos dados':wait=ident=None
   elif msg=='Eleitor foi habilitado':
    if (src,n) in targets:
     r=targets[(src,n)];matched+=1
     r['aguardando_identificador_desde']=wait or '';r['identificador_digitado_em']=ident or ''
     r['tempo_aguardando_identificador_seg']=seconds(ident)-seconds(wait) if wait and ident and seconds(ident)>=seconds(wait) else ''
     r['tempo_da_digitacao_a_habilitacao_seg']=now-seconds(ident) if ident and now>=seconds(ident) else ''
    wait=ident=None
   elif msg=='O voto do eleitor foi computado':wait=ident=None
assert matched==37979,matched
with (base/'votacoes_verificacao.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
selected=[r for r in rows if r['tempo_aguardando_identificador_seg']!='' and int(r['tempo_aguardando_identificador_seg'])>=300 and int(r['duracao_seg'])<=10]
with (base/'ciclos_ate_10_segundos_apos_aguardo_5min.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(selected)
result={'votacoes_com_tempos_identificador':sum(r['tempo_aguardando_identificador_seg']!='' for r in rows),'aguardo_identificador_ge_5min_e_duracao_ate_10':len(selected),'secoes_nesse_recorte':len({r['arquivo'] for r in selected}),'por_grupo':dict(Counter(r['grupo'] for r in selected)),'definicao':'Diferença entre a última mensagem de espera por identificador e a digitação do identificador da tentativa que gerou a habilitação. Não comprova ausência física de eleitor ou ociosidade da mesa.'}
(base/'resumo_esperas.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
