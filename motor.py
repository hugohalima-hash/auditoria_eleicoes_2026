"""Motor v2: classificação conservadora, logs aninhados e sequências rastreáveis."""
import csv
import hashlib
import io
import json
import math
import re
import zipfile
import unicodedata
from datetime import datetime
from collections import Counter
from pathlib import Path

VERSION = '3.0'
ENGINE_SHA256 = hashlib.sha256(b''.join(
    name.encode()+b'\0'+Path(__file__).with_name(name).read_bytes()
    for name in ('motor.py','lote.py','integridade.py'))).hexdigest()
CACHE_VERSION = VERSION + ':' + ENGINE_SHA256
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
    """Remove apenas blocos integralmente idênticos, nunca linhas isoladas.

    A ordem entre blocos distintos não é certificada pelo nome do pacote.
    O extrator rompe os ciclos e as séries em cada fronteira de origem.
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
    seen = set()
    output=[]
    duplicates=0
    for label,txt in blocks:
        digest=hashlib.sha256(txt.encode('latin-1')).digest()
        if digest in seen:
            duplicates+=len(txt.splitlines())
            continue
        seen.add(digest)
        output.extend((label,lineno,line) for lineno,line in enumerate(txt.splitlines(),1))
    return output,len(blocks),duplicates

def seconds(stamp):
    return int(stamp[11:13])*3600+int(stamp[14:16])*60+int(stamp[17:19])

def normalized(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text.casefold())
                   if unicodedata.category(c) != 'Mn').strip()


def classify(evidence):
    """Decide somente ao fechar o ciclo, aceitando evidência tardia.

    Conflitos não são resolvidos por precedência arbitrária.
    Ausência de mensagem biométrica não comprova ausência de biometria.
    """
    mesario = evidence.get('explicito') or evidence.get('sem_associacao') or evidence.get('nova_digital')
    if evidence.get('type') == 'biometrica' and mesario:
        return 'indefinida', 'evidencias_conflitantes'
    if evidence.get('types_conflitantes'):
        return 'indefinida', 'evidencias_conflitantes'
    if evidence.get('explicito'):
        return 'mesario_explicito', ''
    if evidence.get('type') == 'biometrica':
        return 'biometrica', ''
    if evidence.get('sem_associacao'):
        return 'digital_mesario_sem_associacao', ''
    if evidence.get('nova_digital'):
        return 'digital_mesario_gravada', ''
    if evidence.get('type'):
        return 'tipo_outro', 'tipo_nao_suportado'
    if evidence.get('ano') and not evidence.get('tentativa_biometrica') and not evidence.get('digital_mesario'):
        return 'ano_nascimento_sem_evento_biometrico', ''
    return 'indefinida', 'evidencia_insuficiente'


def extract(raw, day):
    datetime.strptime(day, '%d/%m/%Y')
    lines, nblocks, dups = read_logs(raw)
    sessions = []; warnings = []; active = None; attempt = {}
    kinds = Counter(); unparsed = 0; changes = 0; epoch = 0
    prev_unit = None; prev_stamp = None; prev_source = None
    sources = set(); orphan_votes = 0; discarded_attempts = 0; votes = 0
    regressions = 0; partials = 0

    def warn(code, source, lineno):
        warnings.append({'codigo': code, 'origem': source, 'linha': lineno})

    def finish(outcome, source, lineno, stamp=None):
        nonlocal active
        if active is None:
            return
        evidence=active.pop('evidencias')
        active['tipo'], reason = classify(evidence)
        active['tentativa_biometrica']=bool(evidence.get('tentativa_biometrica'))
        active['autorizacao']=evidence.get('autorizacao','')
        active['motivo_classificacao'] = reason
        active['desfecho'] = outcome
        active['origem_desfecho'] = source
        active['linha_desfecho'] = lineno
        if stamp:
            active['hora_desfecho'] = stamp
        if active['tipo'] in ('indefinida', 'tipo_outro'):
            warn(reason, active['origem'], active['linha'])
        if outcome in ('sem_desfecho', 'interrompida', 'fronteira_origem',
                       'fronteira_equipamento', 'regressao_relogio', 'registro_malformado'):
            warn('ciclo_' + outcome, active['origem'], active['linha'])
        if active.get('suspensao_parcial') and outcome != 'voto_computado':
            warn('suspensao_parcial_sem_computado', source, lineno)
        active = None

    for source, lineno, line in lines:
        # Other dates are not silently joined to an election-day cycle.
        if not line.startswith(day + ' '):
            continue
        sources.add(source)
        if prev_source is not None and source != prev_source:
            finish('fronteira_origem', source, lineno)
            attempt = {}; epoch += 1; prev_unit = None; prev_stamp = None
        prev_source = source
        p = line.split('\t')
        if len(p) != 6 or not p[2].strip():
            unparsed += 1; finish('registro_malformado', source, lineno)
            attempt = {}; epoch += 1; warn('registro_malformado', source, lineno)
            continue
        stamp, unit, msg = p[0], p[2], p[4]
        try:
            parsed = datetime.strptime(stamp, '%d/%m/%Y %H:%M:%S')
            if parsed.strftime('%d/%m/%Y %H:%M:%S') != stamp:
                raise ValueError('data não canônica')
        except ValueError:
            unparsed += 1; finish('registro_malformado', source, lineno)
            attempt = {}; epoch += 1; warn('timestamp_invalido', source, lineno)
            continue
        if prev_unit is not None and unit != prev_unit:
            finish('fronteira_equipamento', source, lineno)
            attempt = {}; epoch += 1
        elif prev_stamp is not None and parsed < prev_stamp:
            regressions += 1; finish('regressao_relogio', source, lineno)
            attempt = {}; epoch += 1; warn('regressao_relogio', source, lineno)
        prev_unit = unit; prev_stamp = parsed
        low = normalized(msg)
        if ('relogio' in low) and ('ajust' in low or 'acert' in low):
            changes += 1; finish('interrompida', source, lineno)
            attempt = {}; epoch += 1
        if low in ('urna desligada pela chave', 'mudanca do estado da chave: urna desligada',
                   'reiniciando a urna', 'urna reiniciada a pedido do aplicativo',
                   'inicio das operacoes do logd'):
            finish('interrompida', source, lineno, stamp)
            attempt = {}; epoch += 1
        start_attempt = low.startswith('aguardando digitacao do identificador') or low == 'identificador do eleitor digitado pelo mesario'
        if start_attempt:
            finish('sem_desfecho', source, lineno)
            attempt = {}
        if low.startswith('habilitacao cancelada') or low == 'mesario cancelou entrada dos dados':
            if active is None:
                discarded_attempts += 1
            # Before habilitation this cancels an attempt, not a vote.
            if active is not None:
                finish('sem_desfecho', source, lineno)
            attempt = {}
            continue
        evidence = active['evidencias'] if active is not None else attempt
        if re.fullmatch(r'tipo de habilitacao do eleitor \[[^\]]+\]',low):
            kind = 'biometrica' if '[biometrica]' in low else 'tipo_outro'
            if evidence.get('type') and evidence['type'] != kind:
                evidence['types_conflitantes'] = True
            evidence['type'] = kind
            kinds[msg] += 1
        if 'solicita digital' in low and 'mesario' not in low:
            evidence['tentativa_biometrica'] = True
        if 'ano de nascimento digitado e igual ao do cadastro' in low:
            evidence['ano'] = True
        if 'capturada a digital do mesario' in low:
            evidence['digital_mesario'] = True
        if 'nao encontrou digital coletada em nenhum dos arquivos' in low and evidence.get('digital_mesario'):
            evidence['nova_digital'] = True
        if 'nao e possivel associar a habilitacao a um mesario' in low:
            evidence['sem_associacao'] = True
        if re.fullmatch(r'mesario \d+ habilitou o eleitor[.!]?',low):
            evidence['explicito'] = True; evidence['autorizacao'] = stamp
        if low == 'eleitor foi habilitado':
            if active is not None:
                finish('sem_desfecho', source, lineno)
                # Do not copy previous cycle's evidence into new habilitation.
                attempt = {}
            active = {'tipo': 'indefinida', 'hora': stamp, 'seg': seconds(stamp),
                'origem': source, 'linha': lineno, 'urna': unit, 'epoca': epoch,
                'autorizacao': attempt.get('autorizacao', ''),
                'tentativa_biometrica': bool(attempt.get('tentativa_biometrica')),
                'evidencias': attempt}
            sessions.append(active); attempt = {}
        if low == 'eleitor foi suspenso e nao confirmou nenhum voto' or low == 'eleitor nao votou':
            if active is not None:
                active['cancelada'] = True
                finish('suspensa_sem_voto', source, lineno, stamp)
            else:
                warn('suspensao_sem_habilitacao', source, lineno)
            attempt = {}
        if low in ('votacao cancelada',):
            if active is not None:
                active['cancelada'] = True
                finish('cancelada_sem_voto', source, lineno, stamp)
            else:
                warn('cancelamento_sem_habilitacao', source, lineno)
            attempt = {}
        if low == 'eleitor votou parcialmente e em seguida foi suspenso':
            partials += 1
            if active is not None:
                active['suspensao_parcial'] = True
            else:
                warn('suspensao_parcial_sem_habilitacao', source, lineno)
        if low == 'o voto do eleitor foi computado':
            votes += 1
            if active is not None:
                active['voto'] = stamp
                finish('voto_computado', source, lineno, stamp)
            else:
                orphan_votes += 1; warn('voto_sem_habilitacao', source, lineno)
            attempt = {}
    if active is not None:
        finish('sem_desfecho', active['origem'], active['linha'])
    outcomes = Counter(s['desfecho'] for s in sessions)
    linked = outcomes['voto_computado']
    unresolved = sum(v for k,v in outcomes.items() if k not in
                     ('voto_computado', 'suspensa_sem_voto', 'cancelada_sem_voto'))
    admissible = not (unparsed or orphan_votes or unresolved or regressions or changes
                      or len(sources) > 1 or warnings)
    return sessions, warnings, {'blocos_log': nblocks, 'blocos_distintos': len(sources),
        'linhas_duplicadas_removidas': dups, 'linhas_dia_malformadas': unparsed,
        'eventos_ajuste_relogio': changes, 'regressoes_relogio': regressions,
        'votos_computados': votes, 'votos_sem_habilitacao': orphan_votes,
        'suspensas_sem_voto': outcomes['suspensa_sem_voto'],
        'canceladas_sem_voto': outcomes['cancelada_sem_voto'],
        'ciclos_sem_desfecho_explicado': unresolved,
        'tentativas_canceladas_antes_habilitacao': discarded_attempts,
        'suspensoes_parciais': partials,
        'residuo_conservacao_habilitacoes': len(sessions) - linked - outcomes['suspensa_sem_voto'] - outcomes['cancelada_sem_voto'] - unresolved,
        'residuo_conservacao_votos': votes - linked - orphan_votes,
        'admissivel_estatistica': admissible, 'mensagens_tipo': dict(kinds)}

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
        if s.get('desfecho') not in (None, 'voto_computado', 'suspensa_sem_voto', 'cancelada_sem_voto'):
            good=False
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
            'regressoes_relogio','suspensas_sem_voto','canceladas_sem_voto',
            'ciclos_sem_desfecho_explicado','votos_sem_habilitacao',
            'tentativas_canceladas_antes_habilitacao','suspensoes_parciais',
            'residuo_conservacao_habilitacoes','residuo_conservacao_votos',
            'sequencias_2mais_mesario','sequencias_2mais_sem_biometria']
    result={'versao_motor':VERSION,'sha256_motor':ENGINE_SHA256,'data':day,'arquivos_processados':len(rows),'erros':len(errors)}
    result.update({k:sum(r.get(k,0) for r in rows) for k in fields})
    for group in ['mesario','sem_biometria']:
        result['maior_sequencia_'+group]=max((r['maior_sequencia_'+group] for r in rows),default=0)
    result['arquivos_sem_habilitacoes']=sum(r['habilitacoes']==0 for r in rows)
    result['arquivos_com_avisos']=sum(r['avisos']>0 for r in rows)
    result['arquivos_admissiveis_estatistica']=sum(bool(r.get('admissivel_estatistica',False)) for r in rows)
    result['arquivos_em_quarentena']=len(rows)-result['arquivos_admissiveis_estatistica']
    result['validacao_independente']='pendente; nenhuma acurácia de 99,9% certificada'
    return result
