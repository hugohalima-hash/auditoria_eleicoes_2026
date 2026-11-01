"""Análise estadual de ritmo: mesma regra validada no Acre, memória por seção."""
import csv,gzip,hashlib,io,json,zipfile
from collections import Counter,defaultdict
from pathlib import Path
from statistics import mean,median,quantiles
from motor import extract,read_logs,seconds,MESARIO,ENGINE_SHA256
from integridade import digest,verified

GROUPS=('mesario','conjunto')
TRANSITIONS={('biometrica','biometrica'):'bio_bio',('mesario','mesario'):'mes_mes',('ano','ano'):'ano_ano',('biometrica','mesario'):'bio_mes'}

def group(s):
 return 'mesario' if s['tipo'] in MESARIO else 'ano' if s['tipo']=='ano_nascimento_sem_evento_biometrico' else 'biometrica' if s['tipo']=='biometrica' else 'outro'
def q(a,p):
 a=sorted(a);x=(len(a)-1)*p;j=int(x);return a[j]+(a[min(j+1,len(a)-1)]-a[j])*(x-j)
def stats(a):
 return dict(n=len(a),media=mean(a),mediana=median(a),p10=q(a,.1),p90=q(a,.9),minimo=min(a),maximo=max(a)) if a else {'n':0}
def histogram_stats(c):
 n=sum(c.values())
 if not n:return {'n':0}
 items=sorted(c.items())
 def at(i):
  acc=0
  for value,count in items:
   acc+=count
   if acc>i:return value
 def quant(p):
  x=(n-1)*p;j=int(x);return at(j)+(at(min(j+1,n-1))-at(j))*(x-j)
 return dict(n=n,media=sum(k*v for k,v in items)/n,mediana=quant(.5),p10=quant(.1),p90=quant(.9),minimo=items[0][0],maximo=items[-1][0])
def csvrows(path):return list(csv.DictReader(open(path,encoding='utf-8-sig')))
def write_csv(path,rows,fields=None):
 rows=list(rows)
 with Path(path).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields or list(dict.fromkeys(k for row in rows for k in row)));w.writeheader();w.writerows(rows)
class StreamCSV:
 def __init__(self,path):self.f=gzip.open(path,'wt',encoding='utf-8-sig',newline='');self.writer=None
 def write(self,row):
  if self.writer is None:self.writer=csv.DictWriter(self.f,fieldnames=list(row));self.writer.writeheader()
  self.writer.writerow(row)
 def close(self):
  if self.writer is None:self.f.write('sem_ocorrencias\n')
  self.f.close()

def sequences(ss,common,ref):
 """Não cruza origens/urnas/épocas e não salta ciclos de outra categoria."""
 result=[];baseline=stats(ref)
 for mode in GROUPS:
  for completed in [True,False]:
   current=[]
   def flush():
    if len(current)<2:return
    gaps=[b['seg']-a['seg'] for a,b in zip(current,current[1:])]
    item=dict(**common,id=f'{common["arquivo"]}:{mode}:{completed}:{current[0]["linha"]}',grupo=mode,apenas_concluidas=completed,liberacoes=len(current),votos=sum('voto' in s for s in current),mesario=sum(group(s)=='mesario' for s in current),ano=sum(group(s)=='ano' for s in current),inicio=current[0]['hora'],fim=current[-1]['hora'],origem=current[0]['origem'],urna=current[0]['urna'],epoca=current[0]['epoca'],linha_inicio=current[0]['linha'],linha_fim=current[-1]['linha'],linha_ultimo_desfecho=current[-1]['linha_desfecho'],horarios=' | '.join(s['hora'][11:] for s in current),tipos=' | '.join(group(s) for s in current),intervalos_seg=' | '.join(map(str,gaps)),media_seg=mean(gaps),mediana_seg=median(gaps),minimo_seg=min(gaps),maximo_seg=max(gaps),pares_biometricos_secao=len(ref))
    for k in ['media','mediana','p10']:item['biometrica_'+k+'_seg']=baseline.get(k,'')
    item['percentual_da_media_biometrica']=100*item['media_seg']/baseline['media'] if ref else ''
    item['percentil_intervalo_medio_na_biometria']=100*sum(x<=item['media_seg'] for x in ref)/len(ref) if ref else ''
    item['triagem_ritmo']=completed and len(current)>=3 and common['admissivel']=='True' and len(ref)>=30 and item['media_seg']<baseline['p10']
    result.append(item)
   for s in ss:
    good=(group(s)=='mesario' if mode=='mesario' else group(s) in ('mesario','ano')) and (not completed or 'voto' in s)
    contiguous=not current or all(s[k]==current[-1][k] for k in ('epoca','origem','urna'))
    if not good or not contiguous:flush();current=[]
    if good:current.append(s)
   flush()
 return result

def concentration(profiles):
 groups=defaultdict(list);refs=[];flags=[]
 for r in profiles:
  if r['admissivel']=='True' and r['votos_computados']>=100:groups[(r['codigo_municipio'],r['zona'])].append(r)
 eligible=0
 for (mu,zone),peers in sorted(groups.items()):
  if len(peers)<20:continue
  eligible+=len(peers);values=[r['percentual_verificacao']/100 for r in peers];lo,_,hi=quantiles(values,n=4,method='inclusive');threshold=max(hi+3*(hi-lo),median(values)+.1)
  refs.append(dict(codigo_municipio=mu,municipio=peers[0]['municipio'],zona=zone,secoes=len(peers),mediana=median(values),q1=lo,q3=hi,limite=threshold))
  for r in peers:
   if r['percentual_verificacao']/100>threshold:flags.append(dict(r,limite_percentual=100*threshold))
 return sorted(flags,key=lambda x:(-x['percentual_verificacao'],x['arquivo'])),refs,eligible

def analyze(uf,package,published,out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);root=Path(published)/'resultados'/uf
 assert verified(root,ENGINE_SHA256),'Manifesto da análise original inválido'
 published_summary=json.loads((root/'resumo.json').read_text());source_sha=json.loads((Path(published)/'conferencias'/uf/'conferencia.json').read_text())['sha256_pacote']
 assert digest(package)==source_sha,'Pacote bruto difere da fonte congelada'
 profiles=csvrows(root/'urnas.csv');cfg=json.loads((root/'config_oficial.json').read_text());names={str(m['cd']).zfill(5):m['nm'] for a in cfg['abr'] for m in a.get('mu',[])}
 counts=Counter();releases=Counter();hist=defaultdict(Counter);state_profiles=[];municipal=defaultdict(Counter);references=[];seq_count={g:Counter() for g in GROUPS};all_seq_count={g:Counter() for g in GROUPS};section_sets={g:{'ge2':set(),'ge3':set()} for g in GROUPS};tops={g:{'top_quantidade':[],'top_rapidez_ge3':[]} for g in GROUPS};selected={};validated=0
 pairfile=StreamCSV(out/'01_intervalos_todos.csv.gz');seqfile=StreamCSV(out/'02_sequencias.csv.gz');votesfile=StreamCSV(out/'05_votacoes_mesario_ano.csv.gz')
 try:
  with zipfile.ZipFile(package) as archive:
   for i,r in enumerate(profiles,1):
    name=r['arquivo'];ss,warn,meta=extract(archive.read(name),'25/10/2026');assert len(ss)==int(r['habilitacoes']) and meta['votos_computados']==int(r['votos_computados']),name
    kinds=Counter(s['tipo'] for s in ss);assert all(kinds[k]==int(r[k]) for k in kinds),name
    common=dict(uf=uf,municipio=names.get(r['municipio'],r['municipio']),zona=r['zona'],secao=r['secao'],arquivo=name,admissivel=r['admissivel_estatistica']);ref=[];local=Counter()
    for session in ss:
     g=group(session);releases[g]+=1;counts[g]+='voto' in session
     if 'voto' in session:
      local[g]+=1
      if g in ('mesario','ano'):votesfile.write(dict(**common,grupo=g,tipo=session['tipo'],habilitacao=session['hora'],voto_computado=session['voto'],origem=session['origem'],urna=session['urna'],linha_habilitacao=session['linha'],linha_voto=session['linha_desfecho']))
    for a,b in zip(ss,ss[1:]):
     if any(a[k]!=b[k] for k in ('epoca','origem','urna')):continue
     gap=b['seg']-a['seg'];assert gap>=0
     row=dict(**common,origem=a['origem'],urna=a['urna'],epoca=a['epoca'],liberacao_anterior=a['hora'],liberacao_seguinte=b['hora'],intervalo_seg=gap,tipo_anterior=group(a),tipo_seguinte=group(b),tipo_detalhado_anterior=a['tipo'],tipo_detalhado_seguinte=b['tipo'],anterior_com_voto='voto' in a,seguinte_com_voto='voto' in b,linha_anterior=a['linha'],linha_seguinte=b['linha'],autorizacao_anterior=a['autorizacao'],autorizacao_seguinte=b['autorizacao'],intervalo_autorizacoes_seg=seconds(b['autorizacao'])-seconds(a['autorizacao']) if a['autorizacao'] and b['autorizacao'] else '')
     pairfile.write(row)
     if 'voto' in a and 'voto' in b:
      key=TRANSITIONS.get((group(a),group(b)))
      if key:hist[key][gap]+=1
      if key=='bio_bio':ref.append(gap)
    refs=dict(common,**stats(ref));references.append(refs)
    series=sequences(ss,common,ref)
    for mode,col in [('mesario','maior_sequencia_com_voto_mesario'),('conjunto','maior_sequencia_com_voto_sem_biometria')]:
     expected=int(r[col]);got=max((x['liberacoes'] for x in series if x['grupo']==mode and x['apenas_concluidas']),default=0);assert got==(expected if expected>=2 else 0),(name,mode,got,expected);validated+=1
    for item in series:
     seqfile.write(item);g=item['grupo'];cnt=seq_count[g] if item['apenas_concluidas'] else all_seq_count[g];cnt['ge2']+=1;cnt['ge3']+=item['liberacoes']>=3;cnt['ge5']+=item['liberacoes']>=5;cnt['maximo']=max(cnt['maximo'],item['liberacoes'])
     if not item['apenas_concluidas']:continue
     section_sets[g]['ge2'].add(name)
     if item['liberacoes']>=3:section_sets[g]['ge3'].add(name)
     if item['triagem_ritmo']:selected[item['id']]=item;seq_count[g]['triadas_ritmo']+=1
     tops[g]['top_quantidade']=sorted(tops[g]['top_quantidade']+[item],key=lambda x:(-x['liberacoes'],x['media_seg'],x['arquivo'],x['inicio']))[:5]
     if item['liberacoes']>=3:tops[g]['top_rapidez_ge3']=sorted(tops[g]['top_rapidez_ge3']+[item],key=lambda x:(x['media_seg'],x['arquivo'],x['inicio']))[:5]
    total=sum(local.values());p=dict(common,codigo_municipio=r['municipio'],habilitacoes=len(ss),votos_computados=total,votos_com_evento_mesario=local['mesario'],votos_com_ano_nascimento=local['ano'],total_verificacao=local['mesario']+local['ano'],percentual_verificacao=100*(local['mesario']+local['ano'])/total if total else 0);state_profiles.append(p)
    for k in ('habilitacoes','votos_computados','votos_com_evento_mesario','votos_com_ano_nascimento','total_verificacao'):municipal[common['municipio']][k]+=p[k]
    if i%500==0:print(uf,'logs',i,'/',len(profiles),flush=True)
 finally:pairfile.close();seqfile.close();votesfile.close()
 flags,limits,eligible=concentration(state_profiles)
 for g in GROUPS:
  for key in tops[g]:
   for item in tops[g][key][:2]:selected[item['id']]=item
 cases=sorted(selected.values(),key=lambda x:(x['arquivo'],x['grupo'],x['inicio']))
 for i,c in enumerate(cases,1):c['caso']=f'C{i:05d}';c['log_trecho']='trechos/'+c['caso']+'.txt'
 summary=dict(uf=uf,motor=ENGINE_SHA256,sha256_pacote_oficial=source_sha,logs=len(profiles),total_liberacoes=dict(releases),total_votos=dict(counts),pares_por_transicao={k:histogram_stats(hist[k]) for k in TRANSITIONS.values()},sequencias={},sequencias_todas_liberacoes={g:dict(x) for g,x in all_seq_count.items()},concentracao=dict(secoes_comparadas=eligible,secoes_sinalizadas=len(flags),votos_conjunto=sum(x['total_verificacao'] for x in flags),votos_totais=sum(x['votos_computados'] for x in flags)),quarentena=sum(r['admissivel_estatistica']!='True' for r in profiles),publicado=published_summary,validacao=dict(maximos_conferidos=validated,contagens_reconciliadas=len(profiles)))
 for g in GROUPS:summary['sequencias'][g]=dict(seq_count[g],secoes_ge2=len(section_sets[g]['ge2']),secoes_ge3=len(section_sets[g]['ge3']),**tops[g])
 write_csv(out/'03_referencia_biometrica_secao.csv',references);write_csv(out/'04_casos_destacados.csv',cases,['caso'] if not cases else None);write_csv(out/'06_totais_por_secao.csv',state_profiles);write_csv(out/'07_concentracao.csv',flags,list(state_profiles[0])+['limite_percentual']);write_csv(out/'08_referencias_concentracao.csv',limits,['codigo_municipio','municipio','zona','secoes','mediana','q1','q3','limite']);write_csv(out/'09_totais_municipais.csv',[dict(municipio=k,**v) for k,v in sorted(municipal.items())])
 # All selected cases and high-concentration sections retain full originals.
 selected_files={x['arquivo'] for x in flags+cases};(out/'trechos').mkdir(exist_ok=True)
 with zipfile.ZipFile(package) as archive,zipfile.ZipFile(out/f'{uf}_Logs_Integrais.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as logs:
  checks=[]
  for name in sorted(selected_files):
   raw=archive.read(name);logs.writestr('originais/'+name,raw);checks.append(hashlib.sha256(raw).hexdigest()+'  originais/'+name);lines,_,_=read_logs(raw);lines=list(lines)
   day=('Origem\tLinha original\tRegistro integral\n'+'\n'.join(f'{o}\t{ln:06d}\t{txt}' for o,ln,txt in lines if txt.startswith('25/10/2026 '))+'\n').encode();logs.writestr('dia_inteiro/'+name+'.txt',day);checks.append(hashlib.sha256(day).hexdigest()+'  dia_inteiro/'+name+'.txt')
   relevant=[c for c in cases if c['arquivo']==name]
   if relevant:
    sessions,_,_=extract(raw,'25/10/2026')
    for c in relevant:
     prev=[x for x in sessions if x['origem']==c['origem'] and x['epoca']==c['epoca'] and x['linha']<c['linha_inicio']];lo=prev[-1]['linha_desfecho'] if prev else max(1,c['linha_inicio']-60);hi=c['linha_ultimo_desfecho'];segment=[(ln,txt) for o,ln,txt in lines if o==c['origem'] and lo<=ln<=hi]
     header=f"{c['caso']} | {c['municipio']} | Zona {c['zona']} | Seção {c['secao']}\nArquivo: {name}\nOrigem: {c['origem']}\nLinhas {lo}-{hi}, sem cortes internos.\n\n"
     (out/c['log_trecho']).write_text(header+'\n'.join(f'{ln:06d}\t{txt}' for ln,txt in segment)+'\n');assert len(segment)==hi-lo+1
  logs.writestr('SHA256SUMS.txt','\n'.join(checks)+'\n')
 summary['logs_integrais_preservados']=len(selected_files);summary['casos_destacados']=len(cases)
 (out/'resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));return summary
