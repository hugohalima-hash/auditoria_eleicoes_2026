"""Motor v2: classificação conservadora, logs aninhados e sequências rastreáveis."""
import csv
import hashlib
import io
import json
import math
import re
import zipfile
from collections import Counter
from pathlib import Path

VERSION = '2.1'
NAME = re.compile(r'o0*(\d+)([a-z]{2})(\d{5})(\d{4})(\d{4})-(.+)\.(.+)$', re.I)
MESARIO = {'mesario_explicito', 'digital_mesario_gravada', 'digital_mesario_sem_associacao'}
NONBIO = MESARIO | {'ano_nascimento_sem_evento_biometrico'}
CAT = ['biometrica', 'mesario_explicito', 'digital_mesario_gravada',
       'digital_mesario_sem_associacao', 'ano_nascimento_sem_evento_biometrico',
       'tipo_outro', 'indefinida']

def section(name):
    m = NAME.search(Path(name).name)
    if not m:
        return {}
    return dict(zip(['pleito','uf','municipio','zona','secao','tipo_arquivo','extensao'],m.groups()))

def read_logs(raw):
    """Deduplicação por multiplicidade máxima de linhas idênticas entre arquivos.
    Preserva a ordem de cada log e lê contingências antes do log corrente.
    """
    blocks = []
    total = 0
    def descend(data, label, level=0):
        nonlocal total
        if level > 6:
            raise ValueError('aninhamento excede 6 níveis')
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            infos = [x for x in z.infolist() if not x.is_dir()]
            total += sum(x.file_size for x in infos)
            if total > 256 * 1024 * 1024:
                raise ValueError('limite descompactado de 256 MiB excedido')
            def key(x):
                m = re.match(r'^\d{8}(\d{2})(\d{2})(\d{4})(\d{2})(\d{2})(\d{2})',Path(x.filename).name)
                if m:
                    d,mo,y,h,mi,s=m.groups()
                    return (0,y+mo+d+h+mi+s,x.filename)
                return (1,'',x.filename)
            for info in sorted(infos,key=key):
                if info.filename.lower().endswith(('.jez','.logjez')):
                    descend(z.read(info),label+'!'+info.filename,level+1)
            for info in sorted(infos,key=key):
                if info.filename.lower().endswith('logd.dat'):
                    blocks.append((label+'!'+info.filename,z.read(info).decode('latin-1')))
    try:
        descend(raw,'raiz')
    finally:
        # A função recursiva fecha sobre si mesma e sobre blocks. Sem romper
        # essa referência, textos grandes ficam retidos até a coleta cíclica.
        descend=None
    if not blocks:
        raise ValueError('nenhum logd.dat encontrado, inclusive nos aninhados')
    if len(blocks)==1:
        # Sem cópias aninhadas, não há deduplicação entre arquivos a fazer.
        # Evita construir dois Counters e uma lista adicional de todos os eventos.
        label,txt=blocks[0]
        def plain_lines():
            for lineno,line in enumerate(txt.splitlines(),1):
                yield label,lineno,line
        return plain_lines(),1,0
    seen = Counter()
    output=[]
    duplicates=0
    for label,txt in blocks:
        local=Counter()
        lines=[]
        for lineno,line in enumerate(txt.splitlines(),1):
            local[line]+=1
            if line.strip() and local[line]<=seen[line]:
                duplicates+=1
                continue
            lines.append((label,lineno,line))
        seen |= local
        output.extend(lines)
    return output,len(blocks),duplicates

def seconds(stamp):
    return int(stamp[11:13])*3600+int(stamp[14:16])*60+int(stamp[17:19])

def extract(raw, day):
    lines,nblocks,dups=read_logs(raw)
    sessions=[]; warnings=[]; active=None; attempt={}; votes=0
    kinds=Counter(); unparsed=0; changes=0; prev=None; epoch=0
    for source,lineno,line in lines:
        if not line.startswith(day+' '):
            continue
        p=line.split('\t')
        if len(p)<5:
            unparsed+=1
            continue
        stamp=p[0];msg=p[4];low=msg.casefold(); unit=p[2]
        if len(stamp)!=19:
            unparsed+=1;continue
        if ('relógio' in low or 'relogio' in low) and ('ajust' in low or 'acert' in low):
            changes+=1;epoch+=1
        if low.startswith('aguardando digitação do identificador') or low=='identificador do eleitor digitado pelo mesário':
            attempt={}
        if 'habilitação cancelada' in low:
            attempt={}
        if 'tipo de habilitação do eleitor [' in low:
            attempt['type']='biometrica' if '[biométrica]' in low or '[biometrica]' in low else 'tipo_outro'
            kinds[msg]+=1
        if 'solicita digital' in low and 'mesário' not in low:
            attempt['tentativa_biometrica']=True
        if 'ano de nascimento digitado é igual ao do cadastro' in low:
            attempt['ano']=True
        if 'capturada a digital do mesário' in low:
            attempt['digital_mesario']=True
        if 'não encontrou digital coletada em nenhum dos arquivos' in low and attempt.get('digital_mesario'):
            attempt['nova_digital']=True
        if 'não é possível associar a habilitação a um mesário' in low:
            attempt['sem_associacao']=True
        if 'mesário' in low and ' habilitou o eleitor' in low:
            attempt['explicito']=True
            attempt['autorizacao']=stamp
        if 'eleitor foi habilitado' in low:
            if active is not None:
                warnings.append({'codigo':'nova_habilitacao_sem_desfecho','origem':source,'linha':lineno})
            if attempt.get('explicito'):
                kind='mesario_explicito'
            elif attempt.get('type')=='biometrica':
                kind='biometrica'
            elif attempt.get('sem_associacao'):
                kind='digital_mesario_sem_associacao'
            elif attempt.get('nova_digital'):
                kind='digital_mesario_gravada'
            elif attempt.get('type'):
                kind='tipo_outro'
            elif attempt.get('ano') and not attempt.get('tentativa_biometrica') and not attempt.get('digital_mesario'):
                kind='ano_nascimento_sem_evento_biometrico'
            else:
                kind='indefinida'
            current=(unit,seconds(stamp))
            if prev and (prev[0]!=unit or current[1]<prev[1]):
                epoch+=1
            prev=current
            active={'tipo':kind,'hora':stamp,'seg':current[1],'origem':source,'linha':lineno,
                    'urna':unit,'epoca':epoch,'autorizacao':attempt.get('autorizacao',''),
                    'tentativa_biometrica':bool(attempt.get('tentativa_biometrica'))}
            sessions.append(active);attempt={}
        if 'o voto do eleitor foi computado' in low:
            votes+=1
            if active is not None and active['urna']==unit:
                active['voto']=stamp
            else:
                warnings.append({'codigo':'voto_sem_habilitacao','origem':source,'linha':lineno})
            active=None;attempt={}
        if any(s in low for s in ['votação cancelada','votacao cancelada','eleitor não votou']):
            if active is not None:
                active['cancelada']=True
            active=None;attempt={}
    if active is not None:
        warnings.append({'codigo':'habilitacao_sem_desfecho_final','origem':active['origem'],'linha':active['linha']})
    return sessions,warnings,{'blocos_log':nblocks,'linhas_duplicadas_removidas':dups,
            'linhas_dia_malformadas':unparsed,'eventos_ajuste_relogio':changes,
            'votos_computados':votes,'mensagens_tipo':dict(kinds)}

def expected_starts(n,k,r):
    """E[número de inícios de séries >=r] sob permutação uniforme com n/k fixos.
    Não é p-valor, nem controla dependência temporal ou multiplicidade nacional.
    """
    if not r or k<r or n<r:
        return 0.0
    p=1.0
    for i in range(r):
        p *= (k-i)/(n-i)
    # P(r sucessos no início) + (n-r)*P(falha, r sucessos).
    return p*(1+n-k if n>r else 1)

def runs_for(sessions, group, completed=False):
    allowed=MESARIO if group=='mesario' else NONBIO
    current=[];groups=[]
    for i,s in enumerate(sessions,1):
        good=s['tipo'] in allowed and (not completed or 'voto' in s)
        if current and s['epoca']!=current[-1][1]['epoca']:
            groups.append(current);current=[]
        if good:
            current.append((i,s))
        elif current:
            groups.append(current);current=[]
    if current:
        groups.append(current)
    return groups

def analyze(name,raw,day):
    ss,w,meta=extract(raw,day)
    c=Counter(s['tipo'] for s in ss)
    row={'arquivo':name,'sha256':hashlib.sha256(raw).hexdigest(),**section(name),
         'habilitacoes':len(ss),**{k:c[k] for k in CAT},
         **{k+'_com_voto':sum(s['tipo']==k and 'voto' in s for s in ss) for k in CAT},
         'com_evento_mesario':sum(c[k] for k in MESARIO),
         'sem_evento_biometrico':sum(c[k] for k in NONBIO),
         'com_evento_mesario_com_voto':sum(s['tipo'] in MESARIO and 'voto' in s for s in ss),
         'sem_evento_biometrico_com_voto':sum(s['tipo'] in NONBIO and 'voto' in s for s in ss),
         'votos_vinculados':sum('voto' in s for s in ss),'avisos':len(w),
         **{k:v for k,v in meta.items() if k!='mensagens_tipo'}}
    runs=[]
    for group in ['mesario','sem_biometria']:
        gs=runs_for(ss,group)
        maximum=max((len(g) for g in gs),default=0)
        row['maior_sequencia_'+group]=maximum
        row['sequencias_2mais_'+group]=sum(len(g)>1 for g in gs)
        row['maior_sequencia_com_voto_'+group]=max((len(g) for g in runs_for(ss,group,True)),default=0)
        k=row['com_evento_mesario' if group=='mesario' else 'sem_evento_biometrico']
        row['inicios_esperados_ge_max_'+group]=expected_starts(len(ss),k,maximum)
        for g in gs:
            if len(g)<2:
                continue
            a,b=g[0][1],g[-1][1]
            gaps=[g[j][1]['seg']-g[j-1][1]['seg'] for j in range(1,len(g))]
            runs.append({'arquivo':name,'grupo':group,'tamanho':len(g),'inicio':a['hora'],
                'fim':b['hora'],'duracao_seg':b['seg']-a['seg'],'min_intervalo_seg':min(gaps),
                'max_intervalo_seg':max(gaps),'votos_vinculados':sum('voto' in s for _,s in g),
                'indice_inicio':g[0][0],'indice_fim':g[-1][0],
                'origem_inicio':a['origem'],'linha_inicio':a['linha'],
                'origem_fim':b['origem'],'linha_fim':b['linha'],
                'categorias':json.dumps(dict(Counter(s['tipo'] for _,s in g)),ensure_ascii=False)})
    return row,runs,w,ss,meta

def write_csv(path,rows,fields=None):
    if fields is None:
        fields=list(rows[0]) if rows else ['arquivo']
    with open(path,'w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore')
        writer.writeheader();writer.writerows(rows)

def summarize(rows,errors,day):
    fields=['habilitacoes',*CAT,*[k+'_com_voto' for k in CAT],
            'com_evento_mesario','sem_evento_biometrico',
            'com_evento_mesario_com_voto','sem_evento_biometrico_com_voto',
            'votos_computados','votos_vinculados','avisos','linhas_dia_malformadas',
            'linhas_duplicadas_removidas','eventos_ajuste_relogio',
            'sequencias_2mais_mesario','sequencias_2mais_sem_biometria']
    result={'versao_motor':VERSION,'data':day,'arquivos_processados':len(rows),'erros':len(errors)}
    result.update({k:sum(r.get(k,0) for r in rows) for k in fields})
    for group in ['mesario','sem_biometria']:
        result['maior_sequencia_'+group]=max((r['maior_sequencia_'+group] for r in rows),default=0)
    result['arquivos_sem_habilitacoes']=sum(r['habilitacoes']==0 for r in rows)
    result['arquivos_com_avisos']=sum(r['avisos']>0 for r in rows)
    return result
