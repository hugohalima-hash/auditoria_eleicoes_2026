"""Relatórios autônomos e didáticos, sem referências à conversa."""
import csv,html,json,textwrap
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Preformatted
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from relatorios_nacionais.nomes import NAMES

def read(p):return list(csv.DictReader(open(p,encoding='utf-8-sig')))
def n(x):return f'{int(x):,}'.replace(',','.')
def d(x):return f'{float(x):.2f}'.rstrip('0').rstrip('.').replace('.',',') if x!='' else 'Não disponível'
def label(g):return 'Somente mesário' if g=='mesario' else 'Mesário ou ano de nascimento'
def loc(c):return f"{c['municipio']}, zona {c['zona']}, seção {c['secao']}"
def generate(uf,out):
 out=Path(out);s=json.loads((out/'resumo.json').read_text());cases=read(out/'04_casos_destacados.csv');flags=read(out/'07_concentracao.csv');municipal=read(out/'09_totais_municipais.csv');votes=s['total_votos'];total=sum(votes.values());target=votes.get('mesario',0)+votes.get('ano',0)
 # At most eight examples in the PDF; all flagged cases and logs remain in digital annexes.
 examples={}
 for g in ('mesario','conjunto'):
  for k in ('top_quantidade','top_rapidez_ge3'):
   for c in s['sequencias'][g][k][:2]:examples[c['id']]=next(x for x in cases if x['id']==c['id'])
 sections=[]
 def section(title):a=[];sections.append((title,a));return a
 def p(a,t):a.append(('p',t))
 def table(a,h,rows,w):a.append(('t',h,rows,w))
 a=section('1. Resultado principal')
 p(a,f"{NAMES[uf].upper()} | Auditoria dos registros de votação. Segundo turno de 25/10/2026. Foco: liberações sucessivas e intervalo entre uma liberação e a seguinte.")
 p(a,f"Foram examinados {n(s['logs'])} logs. Das {n(total)} votações concluídas, {n(votes.get('mesario',0))} tiveram registros de mesário e {n(votes.get('ano',0))} tiveram confirmação do ano de nascimento. O conjunto soma {n(target)} ({d(100*target/total if total else 0)}% do total). Ele inclui atendimentos isolados e sequências.")
 rows=[]
 for g in ('mesario','conjunto'):
  k=s['sequencias'][g];rows.append([label(g),n(k.get('ge2',0)),n(k.get('ge3',0)),n(k.get('maximo',0)),n(k.get('triadas_ritmo',0))])
 table(a,['Procedimento','Séries 2+','Séries 3+','Maior série','Triadas por ritmo'],rows,[57,27,27,27,36])
 p(a,'As séries desta tabela têm todos os atendimentos concluídos. “Triadas por ritmo” indica séries com três ou mais liberações cuja média ficou abaixo da referência rápida biométrica da própria seção. Não é uma contagem de fraudes.')
 p(a,f"A comparação de concentração selecionou {n(s['concentracao']['secoes_sinalizadas'])} seções, com {n(s['concentracao']['votos_conjunto'])} votações do conjunto. Concentração e rapidez são critérios diferentes e podem atingir os mesmos registros; seus totais não devem ser somados.")
 p(a,'Os logs permitem examinar a sequência de operações, mas não demonstram que o eleitor estava ausente ou que outra pessoa votou em seu lugar. A confirmação dessa hipótese depende dos registros de comparecimento e dos documentos da seção.')
 a=section('2. Como o tempo foi medido')
 p(a,'O intervalo vai da mensagem “Eleitor foi habilitado” à mesma mensagem do eleitor seguinte. Ele inclui a votação anterior e o atendimento até a liberação seguinte. A velocidade para digitar e confirmar o voto não é usada como critério de suspeita.')
 table(a,['Exemplo ilustrativo','Horário','Intervalo'],[['Primeira liberação','10:00:00','-'],['Segunda liberação','10:01:20','80 s'],['Terceira liberação','10:02:30','70 s']],[80,40,54])
 p(a,'Nesse exemplo, três liberações geram dois intervalos. A média é 75 segundos. O relatório preserva todos os horários e intervalos de cada série, além da média, do menor e do maior intervalo.')
 p(a,'Uma série exclusivamente de mesário termina quando aparece outra categoria. O conjunto admite mesário ou ano de nascimento; a quantidade de cada procedimento é informada. Ano de nascimento não equivale automaticamente a autorização explícita de um mesário.')
 p(a,'A referência local usa pares biométricos consecutivos na mesma seção. A média pode ser elevada por longas esperas; a mediana é o valor central. A referência rápida corresponde ao valor abaixo do qual ficaram 10% dos intervalos biométricos. Não há um tempo mínimo obrigatório presumido.')
 p(a,'Mudança de origem, equipamento ou continuidade do relógio interrompe o encadeamento. No recorte de votações concluídas, um atendimento sem conclusão também interrompe a série. Os dados incluem separadamente todas as liberações, inclusive as sem voto computado.')
 a=section('3. Ritmo geral e comparação local')
 rows=[]
 for key,name in [('bio_bio','Biométrica → biométrica'),('mes_mes','Mesário → mesário'),('ano_ano','Ano → ano'),('bio_mes','Biométrica → mesário')]:
  k=s['pares_por_transicao'][key];rows.append([name,n(k['n'])]+[d(k.get(x,'')) for x in ['media','mediana','p10','minimo']])
 table(a,['Par concluído','Pares','Média (s)','Mediana (s)','10% até (s)','Mínimo (s)'],rows,[52,25,25,25,25,22])
 p(a,'Esta tabela resume o estado. A seleção de rapidez usa a referência da própria seção, e não uma média estadual aplicada a todos os locais.')
 for g in ('mesario','conjunto'):
  k=s['sequencias'][g];allk=s['sequencias_todas_liberacoes'][g]
  p(a,f"{label(g)}: {n(k.get('ge2',0))} séries concluídas com duas ou mais liberações, em {n(k['secoes_ge2'])} seções. Com três ou mais, {n(k.get('ge3',0))} séries em {n(k['secoes_ge3'])} seções. Ao incluir liberações sem conclusão, são {n(allk.get('ge2',0))} séries com duas ou mais, e a maior tem {n(allk.get('maximo',0))} liberações.")
 a=section('4.1. Maiores sequências de mesário')
 for g in ('mesario','conjunto'):
  if g=='conjunto':a=section('4.2. Maiores sequências do conjunto')
  for c in s['sequencias'][g]['top_quantidade'][:2]:
   p(a,f"{loc(c)}. {label(g)}: {c['liberacoes']} liberações, sendo {c['mesario']} de mesário e {c['ano']} de ano de nascimento.")
   times=c['horarios'].split(' | ');gaps=c['intervalos_seg'].split(' | ')
   table(a,['Ordem','Liberação','Intervalo desde a anterior'],[[i+1,t,'-' if i==0 else gaps[i-1]+' s'] for i,t in enumerate(times)],[20,60,94])
   p(a,f"Média da série: {d(c['media_seg'])} s. Biometria local: média {d(c['biometrica_media_seg'])} s, mediana {d(c['biometrica_mediana_seg'])} s; {n(c['pares_biometricos_secao'])} pares. Referência rápida local: {d(c['biometrica_p10_seg'])} s.")
 a=section('5. Sequências mais rápidas')
 p(a,'Critério exploratório: pelo menos três liberações concluídas, registros adequados à comparação, pelo menos trinta pares biométricos na própria seção e média da série inferior à referência rápida local (percentil 10). Não é um teste de probabilidade de fraude; não há correção por múltiplas comparações ou ajuste individual por fila, horário e perfil dos eleitores.')
 for g in ('mesario','conjunto'):
  p(a,f"{label(g)}: {n(s['sequencias'][g].get('triadas_ritmo',0))} séries atenderam ao critério. Os conjuntos podem se sobrepor.")
  for c in s['sequencias'][g]['top_rapidez_ge3'][:2]:
   p(a,f"{loc(c)}. {c['liberacoes']} liberações ({c['mesario']} mesário; {c['ano']} ano), de {c['inicio'][11:]} a {c['fim'][11:]}. Intervalos: {c['intervalos_seg'].replace(' | ', ', ')} s. Média {d(c['media_seg'])} s; média biométrica {d(c['biometrica_media_seg'])} s, mediana {d(c['biometrica_mediana_seg'])} s e referência rápida {d(c['biometrica_p10_seg'])} s.")
 p(a,'Uma média abaixo da média biométrica não basta para indicar algo incomum: longas esperas elevam a média. A distribuição local precisa ser considerada. Resultados próximos do limite são limítrofes, não evidência forte de ritmo excepcional.')
 flagged=[c for c in cases if c['triagem_ritmo']=='True']
 if flagged:
  table(a,['Município','Zona / seção','Grupo','Nº','Média / ref. (s)'],[[c['municipio'],c['zona']+' / '+c['secao'],'Mesário' if c['grupo']=='mesario' else 'Conjunto',c['liberacoes'],d(c['media_seg'])+' / '+d(c['biometrica_p10_seg'])] for c in flagged[:20]],[48,30,29,16,51])
  p(a,f"Tabela: até vinte séries selecionadas, de {n(len(flagged))} no índice integral. Todas as séries selecionadas e seus trechos cronológicos completos estão nos anexos digitais.")
 a=section('6. Totais e concentração por seção')
 p(a,f"O universo de conferência é de {n(target)} votações concluídas, incluindo ocorrências isoladas. O procedimento de habilitação não prova que o voto foi indevido.")
 p(a,f"Concentração elevada: {n(len(flags))} seções, com {n(s['concentracao']['votos_conjunto'])} votações do conjunto, em {n(s['concentracao']['votos_totais'])} votações concluídas nessas seções. Foram comparadas {n(s['concentracao']['secoes_comparadas'])} seções.")
 if flags:
  table(a,['Município','Zona / seção','Mesário','Ano','Total','%'],[[c['municipio'],c['zona']+' / '+c['secao'],c['votos_com_evento_mesario'],c['votos_com_ano_nascimento'],c['total_verificacao'],d(c['percentual_verificacao'])] for c in flags[:45 if len(flags)<=45 else 20]],[51,32,23,20,21,27])
  if len(flags)>45:p(a,'A tabela apresenta as vinte maiores proporções. A lista integral está em 07_concentracao.csv; todos os logs correspondentes foram preservados.')
 p(a,'A referência de concentração usa mesma zona e município, pelo menos cem votações concluídas por seção e grupo de vinte seções ou mais. O limite é o maior entre terceiro quartil + três intervalos interquartis e mediana + dez pontos percentuais. O cadastramento biométrico individual não foi ajustado.')
 a=section('7. Conferência e limites')
 p(a,f"As contagens de todas as {n(s['logs'])} seções foram reconciliadas com a análise publicada. Os máximos das séries foram conferidos nos dois grupos, totalizando {n(s['validacao']['maximos_conferidos'])} comparações. {n(s['quarentena'])} seções com problemas de qualidade ficaram fora da seleção estatística; seus registros permanecem nos totais descritivos.")
 p(a,'A investigação de possível voto em nome de faltante deve confrontar os registros selecionados com o comparecimento, as atas e os documentos técnicos. Os logs não identificam quem estava fisicamente diante da urna e não permitem atribuir a escolha do eleitor.')
 p(a,'Os documentos digitais preservam todos os pares, sequências e votações do conjunto, não apenas os exemplos. O PDF apresenta até oito exemplos de maiores séries e séries mais rápidas, acompanhados dos trechos sem cortes internos. Todos os casos selecionados por ritmo têm seus trechos completos no anexo digital, mesmo quando não cabem nas tabelas de exemplos.')
 p(a,'Não houve perícia de hardware, validação criptográfica de assinaturas ou conferência de cadernos. Uma triagem estatística não confirma nem descarta, sozinha, uma ocorrência de fraude.')
 a=section('8. Fontes e anexos')
 p(a,'Resultados de referência: https://github.com/hugohalima-hash/auditoria_eleicoes_2026/releases/tag/auditoria-v3-41263277696. O pacote estadual foi conferido com o SHA-256 publicado e o manifesto interno.')
 p(a,f"Pacote bruto oficial: https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2026/arqurnatot/bu_imgbu_logjez_rdv_vscmr_2026_2t_{uf}.zip. SHA-256: {s['sha256_pacote_oficial']}.")
 p(a,'Horários reproduzidos como constam no equipamento, sem conversão de fuso nem presunção de sincronização externa entre urnas. Para cada trecho são informados arquivo, origem e linhas originais. As quebras visuais de linha no PDF não retiram eventos.')
 p(a,f"Anexos: {uf}_Dados_e_Trechos.zip contém CSVs comprimidos de pares, séries e votações, referências por seção, concentrações, resumo municipal e todos os trechos selecionados. {uf}_Logs_Integrais.zip contém os originais e o texto completo do dia de {n(s['logs_integrais_preservados'])} seções. Os dois pacotes têm SHA-256 por arquivo.")
 p(a,'Os originais correspondem a todas as seções selecionadas por concentração ou ritmo e aos exemplos destacados. Cada trecho começa no desfecho anterior, quando disponível, e termina no desfecho final da série. Não há omissão de linhas intermediárias. As fontes e os scripts ficam congelados na publicação da execução.')
 md=[f'# {NAMES[uf]} - liberações sucessivas e intervalos','']
 for title,items in sections:
  md+=['## '+title,'']
  for item in items:
   if item[0]=='p':md += [item[1],'']
   else:
    _,h,rs,_=item;clean=lambda x:str(x).replace('|',' / ');md+=['| '+' | '.join(h)+' |','| '+' | '.join(['---']*len(h))+' |']+['| '+' | '.join(map(clean,row))+' |' for row in rs]+['']
 (out/f'Relatorio_{uf}.md').write_text('\n'.join(md))
 for name,file in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf'),('Mono','DejaVuSansMono.ttf')]:
  if name not in pdfmetrics.getRegisteredFontNames():pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
 st=getSampleStyleSheet();st.add(ParagraphStyle(name='BodyR',fontName='DV',fontSize=9.2,leading=13,spaceAfter=9));st.add(ParagraphStyle(name='TitleR',fontName='DVB',fontSize=17,leading=22,spaceAfter=13,textColor=colors.HexColor('#173c5c')));st.add(ParagraphStyle(name='CellR',fontName='DV',fontSize=7.2,leading=10));st.add(ParagraphStyle(name='HeadR',fontName='DVB',fontSize=7.2,leading=10,textColor=colors.white));st.add(ParagraphStyle(name='LogR',fontName='Mono',fontSize=6.3,leading=8))
 def par(t,style='BodyR'):return Paragraph(html.escape(str(t)),st[style])
 story=[]
 for title,items in sections:
  if story:story.append(PageBreak())
  story.append(par(title,'TitleR'))
  for item in items:
   if item[0]=='p':story.append(par(item[1]));continue
   _,h,rs,w=item;t=Table([[par(x,'HeadR') for x in h]]+[[par(x,'CellR') for x in row] for row in rs],colWidths=[v*174*mm/sum(w) for v in w],repeatRows=1,hAlign='LEFT');pad=1.4 if len(rs)>30 else 3
   t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#173c5c')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f0f4f7')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),pad),('BOTTOMPADDING',(0,0),(-1,-1),pad)]));story += [t,Spacer(1,10)]
 for c in examples.values():
  story += [PageBreak(),par('Anexo '+c['caso']+' - '+loc(c),'TitleR'),par(label(c['grupo'])+'. Horários: '+c['horarios']+'. Intervalos em segundos: '+c['intervalos_seg']+'.')]
  for line in (out/c['log_trecho']).read_text().splitlines():
   for wrapped in textwrap.wrap(line.expandtabs(2),width=127,replace_whitespace=False,drop_whitespace=False) or [' ']:story.append(Preformatted(wrapped,st['LogR']))
 def footer(c,doc):
  c.setFont('DV',7);c.drawString(18*mm,12*mm,NAMES[uf]+' | Liberações sucessivas');c.drawRightString(192*mm,12*mm,str(doc.page))
 pdf=out/f'Relatorio_{uf}.pdf';SimpleDocTemplate(str(pdf),pagesize=(210*mm,297*mm),leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,title=NAMES[uf]+' - Liberações sucessivas',author='Auditor Eleitoral Independente 2026').build(story,onFirstPage=footer,onLaterPages=footer)
 from pypdf import PdfReader
 pages=PdfReader(pdf).pages;assert len(pages)>=8
 # Character geometry catches clipped glyphs; full-page renders are generated for inspection.
 import pdfplumber
 with pdfplumber.open(pdf) as doc:
  for page in doc.pages:
   assert all(c['x0']>=0 and c['x1']<=page.width+.5 for c in page.chars),'Texto fora da página'
 return {'paginas':len(pages),'exemplos_pdf':len(examples)}
