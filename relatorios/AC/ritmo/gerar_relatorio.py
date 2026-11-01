from pathlib import Path
import csv,json,html,hashlib,zipfile,textwrap
from statistics import mean
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Preformatted
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
r=Path(__file__).parent;base=r.parent;out=base/'output';out.mkdir(exist_ok=True)
def read(p):return list(csv.DictReader(open(p,encoding='utf-8-sig')))
s=json.loads((r/'resumo.json').read_text());seq=read(r/'02_sequencias.csv');cases=read(r/'04_casos_destacados.csv');flags=read(base/'anexos/10_secoes_proporcao_elevada.csv');municipal=read(base/'anexos/16_resumo_municipal_por_votos.csv')
def n(v):return f'{int(v):,}'.replace(',','.')
def d(v):return f'{float(v):.2f}'.rstrip('0').rstrip('.').replace('.',',')
def stamp(v):return v[11:]
def secname(c):return f"{c['municipio']} - zona {c['zona']}, seção {c['secao']}"
def label(c):return 'Somente mesário' if c['grupo']=='mesario' else 'Mesário ou ano de nascimento'
def cid(c):return next((x['caso'] for x in cases if x['id']==c['id']),'')
sections=[]
def section(title):
 a=[];sections.append((title,a));return a
def p(a,t):a.append(('p',t))
def table(a,h,rs,w):a.append(('t',h,rs,w))
a=section('1. Resultado principal')
p(a,'ACRE | Auditoria dos logs do segundo turno de 25/10/2026. Emissão: 01/11/2026. Foco: liberações sucessivas de eleitores e intervalo entre uma liberação e a seguinte.')
p(a,'Sim, houve liberações sucessivas pelo mesário na mesma zona e seção. Uma sequência significa que esses atendimentos ocorreram um após o outro, sem uma liberação de outra categoria no meio.')
rows=[]
for g in ['mesario','conjunto']:
 k=s['sequencias'][g];rows.append(['Somente mesário' if g=='mesario' else 'Mesário ou ano de nascimento',n(k['ge2']),n(k['ge3']),str(k['maximo']),str(k['triadas_ritmo'])])
table(a,['Procedimento','Séries com 2+','Séries com 3+','Maior série','Séries rápidas*'],rows,[54,28,28,28,36])
p(a,'* Séries com pelo menos três liberações que terminaram em voto computado e intervalo médio menor que a referência rápida das liberações biométricas na própria seção. O critério e os casos estão detalhados adiante.')
m=s['sequencias']['mesario']['top_quantidade'][0];c=s['sequencias']['conjunto']['top_quantidade'][0]
p(a,f"A maior série exclusivamente de mesário teve {m['liberacoes']} liberações, em {secname(m)}. Os intervalos foram {m['intervalos_seg'].replace(' | ', ', ')} segundos. A média foi {d(m['media_seg'])} segundos entre liberações.")
p(a,f"A maior série do conjunto teve {c['liberacoes']} liberações, em {secname(c)}. Ela mistura os dois procedimentos e não corresponde a dez liberações exclusivamente pelo mesário. Sua média foi {d(c['media_seg'])} segundos.")
p(a,'A única série que atingiu a triagem rápida teve três confirmações por ano de nascimento, sem autorização explícita de mesário: Rio Branco, zona 0001, seção 0830, às 10:12:12, 10:12:55 e 10:13:51. Os intervalos foram 43 e 56 segundos, média de 49,5 s. É um resultado limítrofe: apenas 0,5 s abaixo da referência rápida local de 50 s.')
p(a,'Os totais permanecem relevantes, mesmo quando não há sequência: 22.654 votações concluídas com registros de mesário e 15.325 com ano de nascimento, somando 37.979 de 453.654 votações no estado. Quarenta e uma seções apresentam concentração elevada do conjunto.')
p(a,'Os resultados selecionam registros para conferência. Os logs, sozinhos, não demonstram que um eleitor estava ausente ou que outra pessoa votou em seu lugar.')
a=section('2. Como ler os intervalos')
p(a,'O relógio começa na mensagem “Eleitor foi habilitado” e termina na mesma mensagem do eleitor seguinte. Esse é o intervalo entre liberações. Ele abrange a votação anterior e o atendimento necessário até liberar a pessoa seguinte.')
table(a,['Exemplo ilustrativo','Horário','Intervalo'],[['Primeira liberação','10:00:00','-'],['Segunda liberação','10:01:20','80 segundos'],['Terceira liberação','10:02:30','70 segundos']],[85,35,54])
p(a,'Nesse exemplo, há três liberações e dois intervalos. A média é (80 + 70) ÷ 2 = 75 segundos. O tempo que cada pessoa levou para digitar e confirmar não é usado como critério de suspeita neste relatório.')
p(a,'A comparação usa o mesmo marco para todos os procedimentos. Quando há a mensagem específica “Mesário N habilitou o eleitor”, o horário também é preservado no arquivo de pares. Ele não é misturado com o marco comum “Eleitor foi habilitado”.')
p(a,'A referência da própria seção usa pares biométricos consecutivos: uma liberação biométrica seguida de outra biométrica. Assim, compara-se o ritmo de atendimento dentro do mesmo local. A média inclui esperas longas; a mediana representa o valor central e é menos afetada por essas esperas.')
p(a,'Não há um tempo obrigatório presumido para liberar o eleitor. O procedimento por mesário pode exigir etapas adicionais, mas o efeito no intervalo precisa aparecer nos dados. Diferenças de fila, horário, dificuldade de identificação e perfil dos eleitores também podem alterar o ritmo.')
p(a,'As sequências são interrompidas por outro procedimento, por atendimento sem conclusão no recorte de votos concluídos, por mudança de equipamento ou origem e por quebra de continuidade do relógio. Não são unidos atendimentos de zonas ou seções diferentes.')
a=section('3. Houve sucessão? Quantas liberações?')
rows=[]
for g in ['mesario','conjunto']:
 k=s['sequencias'][g];allseq=[x for x in seq if x['grupo']==g and x['apenas_concluidas']=='False'];rows.append([label({'grupo':g}),n(len(allseq)),str(max(int(x['liberacoes']) for x in allseq)),n(k['ge2']),n(k['secoes_ge2']),n(k['secoes_ge3'])])
table(a,['Procedimento','Séries de liberações 2+','Maior','Séries concluídas 2+','Seções com série 2+','Seções com série 3+'],rows,[43,29,18,31,27,26])
p(a,'“Séries de liberações” inclui também as que não terminaram em voto computado. “Séries concluídas” exige conclusão de todos os atendimentos da série. As tabelas de ritmo a seguir usam as concluídas. As duas contagens estão disponíveis nos anexos; não são somadas.')
p(a,'Distribuição dos intervalos de pares consecutivos concluídos, em todo o Acre:')
rows=[]
for key,name in [('bio_bio','Biométrica → biométrica'),('mes_mes','Mesário → mesário'),('ano_ano','Ano → ano'),('bio_mes','Biométrica → mesário')]:
 k=s['pares_por_transicao'][key];rows.append([name,n(k['n']),d(k['media']),d(k['mediana']),d(k['p10']),d(k['minimo'])])
table(a,['Par consecutivo','Pares','Média (s)','Mediana (s)','10% até (s)','Mínimo (s)'],rows,[53,23,25,25,25,23])
p(a,'“10% até” é a referência rápida: dez em cada cem intervalos biométricos ficaram nesse valor ou abaixo. A tabela estadual é descritiva. A seleção de casos rápidos compara cada série com a biometria de sua própria seção, evitando usar uma média estadual como regra para todos os locais.')
p(a,'O anexo de sequências informa todas as séries: município, zona, seção, horários de cada liberação, intervalo de cada par, média, menor e maior intervalo e referência biométrica local. Não há limite de dez ocorrências na relação de dados.')
a=section('4.1. Maiores sequências somente de mesário')
for g in ['mesario','conjunto']:
 if g=='conjunto':a=section('4.2. Maiores sequências do conjunto')
 for k in s['sequencias'][g]['top_quantidade'][:2]:
  p(a,f"{cid(k)} | {secname(k)}. {label(k)}: {k['liberacoes']} liberações; {k['mesario']} de mesário e {k['ano']} de ano de nascimento.")
  times=k['horarios'].split(' | ');gaps=k['intervalos_seg'].split(' | ')
  table(a,['Ordem','Liberação','Intervalo desde a anterior'],[[str(i+1),v,'-' if i==0 else gaps[i-1]+' s'] for i,v in enumerate(times)],[22,58,94])
  p(a,f"Média da série: {d(k['media_seg'])} s. Na mesma seção, {n(k['pares_biometricos_secao'])} pares biométricos tiveram média {d(k['biometrica_media_seg'])} s e mediana {d(k['biometrica_mediana_seg'])} s. A média da série equivale a {d(k['percentual_da_media_biometrica'])}% da média biométrica.")
a=section('5. Sequências mais rápidas e comparação local')
p(a,'Para uma triagem de ritmo, foram selecionadas séries com pelo menos três liberações, todas concluídas, cuja média ficou abaixo da referência rápida biométrica da própria seção. Exigiram-se pelo menos trinta pares biométricos e registros adequados à comparação. O limite é exploratório; não indica uma probabilidade de fraude nem foi ajustado para múltiplas comparações.')
tri=[x for x in cases if x['triagem_ritmo']=='True']
p(a,f"Resultado: {s['sequencias']['mesario']['triadas_ritmo']} séries exclusivamente de mesário e {s['sequencias']['conjunto']['triadas_ritmo']} séries do conjunto atenderam ao critério. Os grupos podem se sobrepor e não devem ser somados.")
for g in ['mesario','conjunto']:
 p(a,'Duas séries mais rápidas com pelo menos três liberações: '+label({'grupo':g})+'.')
 for k in s['sequencias'][g]['top_rapidez_ge3'][:2]:
  p(a,f"{cid(k)} | {secname(k)}. {k['liberacoes']} liberações ({k['mesario']} de mesário; {k['ano']} de ano), de {stamp(k['inicio'])} a {stamp(k['fim'])}. Intervalos: {k['intervalos_seg'].replace(' | ', ', ')} s. Média: {d(k['media_seg'])} s; biometria local: média {d(k['biometrica_media_seg'])} s, mediana {d(k['biometrica_mediana_seg'])} s, referência rápida {d(k['biometrica_p10_seg'])} s ({n(k['pares_biometricos_secao'])} pares).")
if tri:
 table(a,['Caso / município','Zona / seção','Grupo','Nº','Média (s)','Ref. rápida (s)'],[[x['caso']+' / '+x['municipio'],x['zona']+' / '+x['secao'],'Mesário' if x['grupo']=='mesario' else 'Conjunto',x['liberacoes'],d(x['media_seg']),d(x['biometrica_p10_seg'])] for x in tri],[48,29,28,15,27,27])
else:p(a,'Nenhuma série cumpriu todos os requisitos. Isso não afasta a necessidade de conferir os totais e as concentrações por seção.')
p(a,'O caso C05 é composto por três confirmações de ano de nascimento. Sua média, 49,5 s, está somente 0,5 s abaixo do corte local de 50 s. Uma diferença tão pequena exige cautela: o caso serve para conferência, sem evidência forte de ritmo excepcional. Não há uma sequência de autorização explícita de mesário nesse caso.')
p(a,'Uma série pode ser mais rápida que a média sem estar fora do padrão: aproximadamente metade dos intervalos fica abaixo da mediana. Por isso, a média isolada não basta para rotular um caso como anormal. Os logs integrais dos casos destacados permitem verificar se houve tentativas biométricas, confirmações, cancelamentos ou outros acontecimentos entre as liberações.')
a=section('6. Totais e concentrações por seção')
p(a,'Uma possível utilização indevida não precisa ocorrer em série. O universo de conferência inclui todas as 37.979 votações concluídas do conjunto, distribuídas ao longo do dia. São 22.654 com registro de mesário e 15.325 com confirmação do ano de nascimento. Ano de nascimento não equivale automaticamente a autorização identificada de mesário.')
p(a,'Quarenta e uma seções ultrapassaram a referência local de concentração, reunindo 2.458 votações do conjunto em 8.702 votações concluídas nessas seções. A concentração e o ritmo são critérios diferentes e não devem ser somados como se contassem fraudes distintas.')
table(a,['Município','Zona / seção','Mesário','Ano','Total','%'],[[x['municipio'],x['zona']+' / '+x['secao'],x['votos_com_evento_mesario'],x['votos_com_ano_nascimento'],x['total_verificacao'],d(x['percentual_verificacao'])+'%'] for x in flags],[51,32,23,20,21,27])

a=section('7. Ocorrências técnicas e conclusão')
p(a,'Os 2.270 logs foram lidos e as contagens por seção reconciliadas com o pacote publicado. Houve 453.714 liberações e 453.654 votações concluídas: a diferença corresponde a 53 suspensões explícitas sem voto e sete interrupções. Não houve voto computado sem habilitação associada, classificação indefinida ou erro de leitura.')
p(a,'Sete atendimentos foram interrompidos por desligamento antes de uma conclusão vinculada. Quatro seções tinham registros de equipamentos diferentes no dia; uma delas também estava entre as sete interrupções. Essas dez seções não foram usadas para selecionar anormalidades estatísticas. Os históricos e motivos estão nos anexos técnicos.')
p(a,'Houve sucessão de liberações pelo mesário. O relatório identifica onde ocorreu, quantas liberações compõem cada série e qual foi o intervalo de cada par. A rapidez é avaliada diante do atendimento biométrico da própria seção, sem utilizar a velocidade de digitação do voto como sinal de fraude.')
p(a,'A prioridade de conferência são as séries selecionadas pelo ritmo e as 41 seções com concentração elevada. Devem ser confrontadas com os registros de comparecimento, as atas e os documentos de atendimento técnico. As séries maiores e as mais rápidas também são apresentadas, mesmo quando não atingem o critério de triagem, para permitir leitura direta das evidências.')
p(a,'Uma suspeita de voto em nome de faltante exige confirmar que o eleitor registrado não compareceu e que sua habilitação foi usada indevidamente. A sequência temporal permite orientar essa verificação; não identifica quem estava diante da urna.')
a=section('8. Fontes e anexos de conferência')
p(a,'Comparação de concentração: mesma zona e município; pelo menos cem votações concluídas; grupo de vinte ou mais seções. O limite é o maior entre terceiro quartil + três intervalos interquartis e mediana + dez pontos percentuais. Foram comparadas 2.200 seções. O perfil de cadastramento biométrico individual não foi ajustado.')
p(a,'Fonte: pacote oficial do TSE do Acre, segundo turno de 2026. Os horários foram mantidos como gravados no equipamento, sem conversão de fuso. Cada sequência preserva a origem, o equipamento e as linhas do log. Não se presume sincronização externa entre urnas.')
p(a,'Resultado publicado: https://github.com/hugohalima-hash/auditoria_eleicoes_2026/releases/tag/auditoria-v3-41263277696. Arquivo de referência: AC-tentativa1.zip. SHA-256: e72a82e0720f62bfc7a682946f4cda37fcbeb94aa22bf94e06d6fb7ed5ab1d95.')
p(a,'Pacote bruto: https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2026/arqurnatot/bu_imgbu_logjez_rdv_vscmr_2026_2t_AC.zip. SHA-256: 7e58076367c9a0d8002b7918fe33183a2aee8aaf562d32555cf62ce10d188dc5.')
p(a,'Anexos digitais: Acre_Sequencias_e_Logs.zip contém todos os pares consecutivos, todas as séries com dois ou mais atendimentos, referências biométricas por seção, casos destacados e trechos cronológicos sem cortes internos. Acre_Logs_Integrais.zip contém os arquivos originais e os logs do dia inteiro de 46 seções: as 41 com concentração elevada e as demais dos exemplos destacados, sem duplicar seções. Os dois pacotes incluem SHA-256.')
p(a,'Nas páginas seguintes estão os trechos integrais dos casos de ritmo e dos exemplos destacados. O trecho começa no encerramento do atendimento anterior e vai até a conclusão do último da série. Quando não há atendimento anterior no mesmo bloco, inclui o contexto disponível antes da primeira liberação. Todas as linhas intermediárias são preservadas; quebras visuais de linha não alteram a ordem. O arquivo original completo está no anexo digital.')
p(a,'A análise não realizou conferência de cadernos, perícia do equipamento, validação criptográfica de assinaturas ou conciliação individual por candidato. A comparação de ritmo é exploratória e não controla, individualmente, fila e perfil dos eleitores. Os dados são públicos e a reprodução está no repositório auditoria_eleicoes_2026, em relatorios/AC/ritmo/.')
# Shared body for PDF and Markdown; log windows are complete in both versions.
md=['# Acre - liberações sucessivas e intervalo entre eleitores','']
for title,items in sections:
 md+=['## '+title,'']
 for item in items:
  if item[0]=='p':md += [item[1],'']
  else:
   _,h,rs,_=item;clean=lambda x:str(x).replace('|',' / ')
   md+=['| '+' | '.join(h)+' |','| '+' | '.join(['---']*len(h))+' |']+['| '+' | '.join(map(clean,x))+' |' for x in rs]+['']
for c in cases:
 md+=['## Anexo '+c['caso']+' - '+secname(c),'',label(c)+'. Horários: '+c['horarios']+'. Intervalos em segundos: '+c['intervalos_seg']+'.','', '```text',(r/c['log_trecho']).read_text(),'```','']
(base/'RELATORIO_COMPLETO_AC.md').write_text('\n'.join(md))
for name,file in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf'),('Mono','DejaVuSansMono.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
st=getSampleStyleSheet();st.add(ParagraphStyle(name='BodyR',fontName='DV',fontSize=9.2,leading=13,spaceAfter=9));st.add(ParagraphStyle(name='TitleR',fontName='DVB',fontSize=17,leading=22,spaceAfter=13,textColor=colors.HexColor('#173c5c')));st.add(ParagraphStyle(name='CellR',fontName='DV',fontSize=7.2,leading=10));st.add(ParagraphStyle(name='HeadR',fontName='DVB',fontSize=7.2,leading=10,textColor=colors.white));st.add(ParagraphStyle(name='LogR',fontName='Mono',fontSize=6.3,leading=8,spaceAfter=0))
def par(t,sty='BodyR'):return Paragraph(html.escape(str(t)),st[sty])
story=[]
for title,items in sections:
 if story:story.append(PageBreak())
 story.append(par(title,'TitleR'))
 for item in items:
  if item[0]=='p':story.append(par(item[1]));continue
  _,heads,rs,widths=item;scale=174*mm/sum(widths);body=[[par(x,'HeadR') for x in heads]]+[[par(x,'CellR') for x in row] for row in rs];t=Table(body,colWidths=[x*scale for x in widths],repeatRows=1,hAlign='LEFT');pad=1.4 if len(rs)>30 else 3
  t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#173c5c')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f0f4f7')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),pad),('BOTTOMPADDING',(0,0),(-1,-1),pad)]));story.extend([t,Spacer(1,10)])
for c in cases:
 story.append(PageBreak());story.append(par('Anexo '+c['caso']+' - '+secname(c),'TitleR'));story.append(par(label(c)+'. Horários: '+c['horarios']+'. Intervalos: '+c['intervalos_seg']+' segundos.'))
 for line in (r/c['log_trecho']).read_text().splitlines():
  # Explicit visual wrapping preserves every character of each original line in TXT.
  for wrapped in textwrap.wrap(line.expandtabs(2),width=127,replace_whitespace=False,drop_whitespace=False) or [' ']:story.append(Preformatted(wrapped,st['LogR']))
def footer(c,doc):
 c.setFont('DV',7);c.setFillColor(colors.HexColor('#52667b'));c.drawString(18*mm,12*mm,'ACRE | Liberações sucessivas e intervalo entre eleitores');c.drawRightString(192*mm,12*mm,str(doc.page))
SimpleDocTemplate(str(out/'Relatorio_Completo_Acre.pdf'),pagesize=(210*mm,297*mm),leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,title='Acre - Liberações sucessivas e intervalo entre eleitores',author='Auditor Eleitoral Independente 2026').build(story,onFirstPage=footer,onLaterPages=footer)
print('Relatório produzido:',out/'Relatorio_Completo_Acre.pdf')
