import csv,json,zipfile,sys,hashlib
from pathlib import Path
from collections import defaultdict
r=Path(__file__).parent;base=r.parent;repo=base.parents[1];sys.path.insert(0,str(repo));from motor import read_logs
read=lambda p:list(csv.DictReader(open(p,encoding='utf-8-sig')))
seq=read(r/'02_sequencias.csv');pro=read(base/'dados/resultados/AC/urnas.csv');cases=read(r/'04_casos_destacados.csv');flags=read(base/'anexos/10_secoes_proporcao_elevada.csv')
for group,col in [('mesario','maior_sequencia_com_voto_mesario'),('conjunto','maior_sequencia_com_voto_sem_biometria')]:
 maxima=defaultdict(int)
 for x in seq:
  if x['apenas_concluidas']=='True' and x['grupo']==group:maxima[x['arquivo']]=max(maxima[x['arquivo']],int(x['liberacoes']))
 for x in pro:assert maxima[x['arquivo']]==(int(x[col]) if int(x[col])>=2 else 0),(x['arquivo'],group)
for s in seq:
 gaps=list(map(int,s['intervalos_seg'].split(' | ')));assert len(gaps)==int(s['liberacoes'])-1
 assert abs(sum(gaps)/len(gaps)-float(s['media_seg']))<1e-9
src=repo/'downloads/bu_imgbu_logjez_rdv_vscmr_2026_2t_AC.zip';files=sorted({x['arquivo'] for x in flags+cases});ld=r/'logs';full=r/'logs_dia_inteiro';full.mkdir(exist_ok=True)
with zipfile.ZipFile(src) as z:
 for name in files:
  raw=z.read(name);(ld/name).write_bytes(raw);lines,_,_=read_logs(raw)
  day=[f'{origin}\t{ln:06d}\t{line}' for origin,ln,line in lines if line.startswith('25/10/2026 ')]
  (full/(name+'.txt')).write_text('Origem\tLinha original\tRegistro integral do log\n'+'\n'.join(day)+'\n')
 for c in cases:
  lines,_,_=read_logs(z.read(c['arquivo']));look={(origin,ln):txt for origin,ln,txt in lines}
  for row in (r/c['log_trecho']).read_text().splitlines()[5:]:
   if not row:continue
   ln,txt=row.split('\t',1);assert look[(c['origem'],int(ln))]==txt
  for time in c['horarios'].split(' | '):assert any(txt.startswith('25/10/2026 '+time) and '\tEleitor foi habilitado\t' in txt for txt in look.values())
validation={'maximos_conferidos':len(pro)*2,'sequencias_com_intervalos_recalculados':len(seq),'casos_com_trechos_conferidos_linha_a_linha':len(cases),'secoes_com_log_integral_no_anexo':len(files),'referencia_rapidez':'Percentil 10 biométrico da mesma seção; mínimo 30 pares; série >=3; qualidade admissível','observacao':'Sem ajuste de significância, fila, horário ou perfil individual; seleção exploratória.'}
(r/'validacao.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2))
for filename,paths in [('Acre_Sequencias_e_Logs.zip',sorted(r.glob('*.csv'))+sorted(r.glob('*.json'))+sorted(ld.glob('*.txt'))+[base/'RELATORIO_COMPLETO_AC.md']),('Acre_Logs_Integrais.zip',sorted(ld.glob('*.jez'))+sorted(full.glob('*')))]:
 output=base/filename
 with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  checks=[]
  for p in paths:
   arc=str(p.relative_to(base));z.write(p,arc);checks.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+arc)
  z.writestr('SHA256SUMS.txt','\n'.join(checks)+'\n')
 print('ZIP',filename,output.stat().st_size,hashlib.sha256(output.read_bytes()).hexdigest())
print(validation)
