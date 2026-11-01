from pathlib import Path
from collections import defaultdict,Counter
import csv,json,shutil,html,hashlib,zipfile
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

rev=Path(__file__).parent;base=rev.parent;out=base/'output';ann=out/'anexos';ann.mkdir(parents=True,exist_ok=True)
if not (ann/'01_interrupcoes.csv').exists() and (base/'anexos').exists():
 for source_file in (base/'anexos').glob('0[1-7]_*.csv'):shutil.copy(source_file,ann/source_file.name)
def read(path):return list(csv.DictReader(open(path,encoding='utf-8-sig')))
s=json.load(open(base/'dados/resultados/AC/resumo.json'));t=json.load(open(rev/'resumo_tempos.json'));e=json.load(open(rev/'resumo_esperas.json'));f=json.load(open(rev/'indicadores_foco.json'));source=json.load(open(base/'fonte_publicada.json'))
profile=read(rev/'totais_por_secao.csv');cycles=read(rev/'votacoes_verificacao.csv');flags=read(rev/'secoes_proporcao_elevada_combinada.csv');refs=read(rev/'referencias_proporcao_combinada.csv');seq=read(rev/'sequencias_concluidas.csv');idle=read(rev/'ciclos_ate_10_segundos_apos_aguardo_5min.csv');oldcases=read(ann/'01_interrupcoes.csv');quar=read(ann/'02_quarentena.csv')
def n(x):return f'{int(x):,}'.replace(',','.')
def pct(x,y):return f'{100*float(x)/float(y):.2f}%'.replace('.',',')
def dec(x):return f'{float(x):.2f}'.rstrip('0').rstrip('.').replace('.',',')
def typ(x):return 'Mesário' if x=='mesario' else 'Ano de nascimento' if x=='ano_nascimento' else 'Biométrica'
def wcsv(name,rows):
 with (ann/name).open('w',encoding='utf-8-sig',newline='') as file:
  w=csv.DictWriter(file,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
newfiles={'08_totais_por_secao.csv':'totais_por_secao.csv','09_votacoes_mesario_ano_nascimento.csv':'votacoes_verificacao.csv','10_secoes_proporcao_elevada.csv':'secoes_proporcao_elevada_combinada.csv','11_referencias_proporcao_combinada.csv':'referencias_proporcao_combinada.csv','12_votacoes_ate_10_segundos.csv':'ciclos_ate_10_segundos.csv','13_votacoes_apos_pausa_5min_ate10s.csv':'ciclos_ate_10_segundos_apos_pausa_5min.csv','14_votacoes_apos_aguardo_5min_ate10s.csv':'ciclos_ate_10_segundos_apos_aguardo_5min.csv','15_sequencias_concluidas.csv':'sequencias_concluidas.csv'}
for dst,src in newfiles.items():shutil.copy(rev/src,ann/dst)
municipal=defaultdict(Counter)
for r in profile:
 c=municipal[r['municipio']]
 for key in ['votos_computados','votos_com_evento_mesario','votos_com_ano_nascimento','total_verificacao']:c[key]+=int(r[key])
 c['secoes']+=1
municipalrows=[{'municipio':m,**dict(c)} for m,c in sorted(municipal.items())]
wcsv('16_resumo_municipal_por_votos.csv',municipalrows)
fast=sorted([r for r in cycles if int(r['duracao_seg'])<=10],key=lambda r:(int(r['duracao_seg']),r['arquivo'],r['habilitacao']))
shortstarts=[r for r in cycles if r['intervalo_habilitacoes_seg'] and int(r['intervalo_habilitacoes_seg'])<=30]
flagfiles={r['arquivo'] for r in flags};focusedidle=[r for r in idle if r['arquivo'] in flagfiles]
metadata={'data_relatorio':'2026-11-01','escopo':'Acre, segundo turno de 25/10/2026','fonte':source,'motor_sha256':s['sha256_motor'],'totais_votos':{'com_evento_mesario':22654,'com_ano_nascimento':15325,'conjunto':37979,'total_concluidas':453654},'tempos':t,'esperas':e,'indicadores':f,'secoes_concentradas_com_espera_e_votacao_curta':len({r['arquivo'] for r in focusedidle}),'definicao':'Universo de verificação e indicadores descritivos; não contagem de fraudes ou de eleitores ausentes.'}
metadata['sha256_scripts_complementares']={name:hashlib.sha256((rev/name).read_bytes()).hexdigest() for name in ['analisar_tempos.py','complementar_analise.py','conferir_esperas.py','gerar_relatorio_revisado.py']}
(out/'evidencias_relatorio_revisado.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2))
sections=[]
def section(title):
 x={'title':title,'items':[]};sections.append(x);return x['items']
def p(I,text):I.append(('p',text))
def b(I,text):I.append(('b',text))
def tab(I,heads,rows,widths):I.append(('t',heads,rows,widths))
I=section('1. Resultado principal')
p(I,'Auditoria dos registros de votação do Acre - segundo turno de 25 de outubro de 2026. Relatório emitido em 1º de novembro de 2026.')
p(I,'Objetivo: dimensionar as votações liberadas por mesário ou com confirmação do ano de nascimento e identificar concentrações e padrões de tempo que justifiquem conferência. A hipótese examinada é o uso indevido desses procedimentos para votar em nome de eleitores que não compareceram.')
tab(I,['Indicador','Resultado'],[['Votações concluídas no estado','453.654'],['Com registros de liberação por mesário','22.654 (4,99%)'],['Com confirmação do ano de nascimento','15.325 (3,38%)'],['Total dos dois procedimentos','37.979 (8,37%)'],['Seções com proporção elevada do conjunto','41, contendo 2.458 dessas votações'],['Votações do conjunto concluídas em até 10 segundos','1.620'],['Dessas, após espera de pelo menos 5 minutos por identificação','114, distribuídas em 106 seções']],[109,65])
p(I,'As 37.979 votações constituem o universo de verificação, incluindo ocorrências isoladas e distribuídas ao longo do dia. A seleção não depende de haver uma sequência de liberações. Os dois procedimentos também integram o atendimento regular ao eleitor; sua ocorrência, sozinha, não permite classificar uma votação como fraudulenta.')
p(I,'O principal achado para conferência documental é a concentração dos dois procedimentos em 41 seções. A maior proporção observada nesse grupo foi de 49,51%, em Assis Brasil, zona 0006, seção 0150: 101 de 204 votações concluídas.')
p(I,'Quanto ao ritmo, houve registros curtos e ocorrências após períodos de espera. Entretanto, a duração de até dez segundos também aparece em votações identificadas por biometria. Nas maiores sequências do conjunto, os intervalos médios entre liberações foram superiores a um minuto.')
p(I,'Os logs registram operações, mas não comprovam a presença física de cada eleitor. A apuração de eventual voto em nome de ausente exige confrontar os casos selecionados com os registros de comparecimento, os documentos da seção e as ocorrências técnicas.')
I=section('2. O que está sendo contado')
p(I,'Uma votação concluída é identificada pela mensagem de voto computado após a liberação do eleitor. Trata-se da conclusão do atendimento daquele eleitor, não da soma de votos por cargo. Uma liberação que terminou em suspensão ou interrupção não foi contada como voto concluído.')
tab(I,['Procedimento registrado','Votações concluídas','% do estado'],[['Autorização explícita de mesário','15.680',pct(15680,453654)],['Digital de mesário com indicação de nova gravação','4.076',pct(4076,453654)],['Digital de mesário sem associação nominal no log','2.898',pct(2898,453654)],['Subtotal com registros de mesário','22.654',pct(22654,453654)],['Confirmação do ano de nascimento','15.325',pct(15325,453654)],['Total em análise','37.979',pct(37979,453654)],['Identificação biométrica','415.675',pct(415675,453654)]],[108,38,28])
p(I,'A confirmação de ano de nascimento foi identificada sem mensagem biométrica reconhecida naquela tentativa. O dado não informa, por si só, se o eleitor tinha biometria cadastrada. Os dois grupos são separados na classificação e podem ser somados sem duplicar votações.')
p(I,'Foram registradas 37.990 liberações com os dois procedimentos, mas onze não terminaram em mensagem de voto computado. Por isso, o total de votos em análise é 37.979, e não 37.990.')
p(I,'Seções com maior quantidade absoluta de votações do conjunto:')
top=sorted(profile,key=lambda r:(-int(r['total_verificacao']),r['arquivo']))[:10]
tab(I,['Município','Zona / seção','Mesário','Ano','Total','% da seção'],[[r['municipio'],r['zona']+' / '+r['secao'],n(r['votos_com_evento_mesario']),n(r['votos_com_ano_nascimento']),n(r['total_verificacao']),dec(r['percentual_verificacao'])+'%'] for r in top],[50,31,21,19,21,32])
I=section('3. Totais dos 22 municípios')
tab(I,['Município','Votações concluídas','Mesário','Ano de nascimento','Conjunto','%'],[[r['municipio'],n(r['votos_computados']),n(r['votos_com_evento_mesario']),n(r['votos_com_ano_nascimento']),n(r['total_verificacao']),pct(r['total_verificacao'],r['votos_computados'])] for r in municipalrows],[48,30,23,29,24,20])
p(I,'Os totais municipais incluem as ocorrências de todas as seções, inclusive as separadas da comparação estatística por problemas de continuidade dos registros. São quantidades observadas, não estimativas de fraude.')
p(I,'O anexo 08 apresenta os números de cada uma das 2.270 seções. O anexo 09 contém as 37.979 votações do conjunto, com horários, procedimento de liberação e referências ao log de origem.')
I=section('4. Seções com proporção elevada')
p(I,'Foram comparadas 2.200 seções com pelo menos cem votações concluídas e registros adequados à comparação. Cada seção foi confrontada com as do mesmo município e zona. As 41 seções abaixo ultrapassaram a referência local para a soma dos dois procedimentos. Elas reúnem 2.458 votações do conjunto, dentro de 8.702 votações concluídas nessas seções.')
flags=sorted(flags,key=lambda r:(-float(r['percentual_verificacao']),r['arquivo']))
tab(I,['Município','Zona','Seção','Votações','Mesário','Ano','Conjunto','%'],[[r['municipio'],r['zona'],r['secao'],n(r['votos_computados']),n(r['votos_com_evento_mesario']),n(r['votos_com_ano_nascimento']),n(r['total_verificacao']),dec(r['percentual_verificacao'])+'%'] for r in flags],[45,16,16,22,19,18,20,18])
p(I,'A concentração define prioridade de conferência. Diferenças no cadastramento biométrico e problemas de equipamento precisam ser verificados antes de atribuir a proporção elevada a conduta irregular. A relação integral está no anexo 10.')
I=section('5. Tempo entre a liberação e a conclusão')
p(I,'A duração abaixo vai da mensagem de liberação do eleitor à mensagem de voto computado. Não inclui a conferência de documentos e a identificação anteriores à liberação. Os horários têm precisão de um segundo.')
stats=t['distribuicao_duracao'];ct=t['contagens_tempos']
combined_durations=sorted(int(r['duracao_seg']) for r in cycles)
def quant(vals,prob):
 x=(len(vals)-1)*prob;j=int(x);return vals[j]+(vals[min(j+1,len(vals)-1)]-vals[j])*(x-j)
from statistics import median
statrows=[]
for label,g in [('Mesário','mesario'),('Ano de nascimento','ano_nascimento'),('Biométrica','biometrica')]:
 st=stats[g];count=ct[g]['duracao_ate_10'];statrows.append([label,n(st['n']),str(st['minimo'])+' s',dec(st['mediana'])+' s',dec(st['p90'])+' s',n(count),pct(count,st['n'])])
statrows.insert(2,['Conjunto em análise',n(len(cycles)),str(min(combined_durations))+' s',dec(median(combined_durations))+' s',dec(quant(combined_durations,.9))+' s','1.620',pct(1620,37979)])
tab(I,['Identificação','Votações','Mínimo','Mediana','90% até','Até 10 s','% até 10 s'],statrows,[39,24,19,22,22,24,24])
p(I,'Mediana é o valor que divide as durações ao meio. A coluna “90% até” indica a duração que não foi ultrapassada em 90% das ocorrências. O recorte de até dez segundos é descritivo: não representa um tempo mínimo obrigatório de votação.')
p(I,'No conjunto em análise, 4,27% das votações duraram até dez segundos; entre as biométricas, foram 4,67%. Assim, uma duração curta isolada não diferencia, neste recorte, uma votação regular de um possível uso indevido da liberação.')
p(I,'Exemplos de menor duração no conjunto, com desempate por arquivo e horário:')
tab(I,['Município','Zona / seção','Liberação','Forma','Duração'],[[r['municipio'],r['zona']+' / '+r['secao'],r['habilitacao'][11:],typ(r['grupo']),r['duracao_seg']+' s'] for r in fast[:12]],[48,32,28,44,22])
p(I,'Não houve duração de até cinco segundos entre as 37.979 votações do conjunto. A lista completa das 1.620 ocorrências de até dez segundos está no anexo 12, sem limitação às sequências sucessivas.')
I=section('6. Votações sucessivas e intervalo entre liberações')
p(I,'Uma sequência reúne votações concluídas consecutivas do procedimento examinado, sem outra forma de identificação entre elas. A análise também separa o tempo entre duas liberações sucessivas do tempo que cada eleitor levou após ser liberado.')
tab(I,['Conjunto','Sequências com 2 ou mais','Com 3 ou mais','Com 5 ou mais','Maior sequência'],[['Somente mesário','1.316','103','2','6'],['Mesário ou ano de nascimento','3.580','557','31','10']],[58,36,27,27,26])
p(I,'As faixas se sobrepõem e não devem ser somadas. As maiores sequências concluídas foram:')
seqtop=[]
for g in ['mesario','conjunto']:seqtop.extend(sorted([r for r in seq if r['grupo']==g],key=lambda r:(-int(r['votacoes']),r['arquivo'],r['inicio']))[:2])
tab(I,['Município / seção','Procedimento','Votações','Início / última liberação','Intervalo médio'],[[r['municipio']+' / '+r['secao'],'Mesário' if r['grupo']=='mesario' else 'Conjunto',r['votacoes'],r['inicio'][11:]+' / '+r['ultima_habilitacao'][11:],dec(r['intervalo_medio_habilitacoes_seg'])+' s'] for r in seqtop],[52,28,24,43,27])
p(I,'Na sequência de seis liberações por mesário, em Jordão, o menor intervalo entre liberações foi de 125 segundos. Na sequência de dez do conjunto, em Assis Brasil, foi de setenta segundos. As maiores sequências, portanto, não apresentam liberações em intervalos de poucos segundos.')
p(I,'Em toda a análise, o menor intervalo até uma liberação por mesário foi de 64 segundos; até uma liberação por ano de nascimento, 25 segundos. Houve três intervalos de até trinta segundos, todos com ano de nascimento na segunda votação:')
tab(I,['Município / seção','Liberação','Identificação anterior','Intervalo'],[[r['municipio']+' / '+r['secao'],r['habilitacao'][11:],'Biométrica' if r['tipo_anterior']=='biometrica' else 'Ano de nascimento',r['intervalo_habilitacoes_seg']+' s'] for r in shortstarts],[63,32,49,30])
p(I,'Foi possível comparar a liberação com uma votação anterior concluída em 37.783 casos. Os 196 restantes não tinham um par anterior adequado. Não foram unidos registros de equipamentos ou origens diferentes. A lista de sequências concluídas está no anexo 15.')
I=section('7. Ocorrências isoladas após períodos de espera')
p(I,'A verificação de eventos dispersos foi feita em todas as votações do conjunto, e não apenas nas sequências. A informação de espera foi medida entre a mensagem de que o sistema aguardava o identificador e a digitação que precedeu a liberação.')
tab(I,['Recorte observado','Mesário','Ano','Total'],[['Até 10 s após espera de pelo menos 5 minutos por identificação','66','48','114'],['Até 10 s após intervalo de pelo menos 5 minutos desde o voto anterior','136','73','209']],[115,20,19,20])
p(I,'Os dois recortes não devem ser somados. O primeiro localiza esperas antes da identificação; o segundo inclui também o tempo gasto com identificação, conferência e eventuais dificuldades. Nenhum deles comprova, sozinho, que a mesa estava ociosa ou que o eleitor estava ausente.')
p(I,'Os 114 casos do primeiro recorte estão em 106 seções. O limite de cinco minutos serve apenas para organizar a conferência: votações após pausas menores continuam incluídas na relação integral das 37.979 ocorrências.')
p(I,'Exemplos com maior espera por identificação entre os casos concluídos em até dez segundos:')
idle_sorted=sorted(idle,key=lambda r:(-int(r['tempo_aguardando_identificador_seg']),int(r['duracao_seg']),r['arquivo']))
def mins(v):return str(int(v)//60)+'m '+str(int(v)%60).zfill(2)+'s'
tab(I,['Município','Zona / seção','Liberação','Espera','Identificação','Votação'],[[r['municipio'],r['zona']+' / '+r['secao'],r['habilitacao'][11:],mins(r['tempo_aguardando_identificador_seg']),typ(r['grupo']),r['duracao_seg']+' s'] for r in idle_sorted[:10]],[43,30,27,26,31,17])
p(I,'Os tempos de espera puderam ser medidos em 37.977 das 37.979 votações do conjunto. Os dois casos sem os registros necessários não receberam valor presumido. Os anexos 13 e 14 apresentam integralmente os dois recortes, com horários e linhas dos logs.')
I=section('8. Ocorrências operacionais relevantes')
p(I,'Foram encontradas sete liberações interrompidas antes de um registro de voto computado. Elas não integram o total de 37.979 votações concluídas. A ocorrência é relevante para verificar o atendimento ao eleitor afetado, mas não demonstra perda dos votos anteriores da seção.')
shortreason={'0102300010608':'Sem motivo explícito no intervalo','0107400040482':'Sem motivo explícito no intervalo','0108200040368':'Erro de voto não registrado; desligamentos sucessivos','0139200010554':'Tecla indevida antes do desligamento','0139200090053':'Sem motivo explícito no intervalo','0145700030001':'Sem motivo explícito no intervalo','0145700030084':'Interação prolongada e tentativas de suspensão'}
tab(I,['Município','Zona / seção','Desligamento','Registro anterior'],[[r['municipio'],r['zona']+' / '+r['secao'],r['desligamento'],shortreason[r['arquivo'][8:21]]] for r in oldcases],[45,31,27,71])
p(I,'Em Rodrigues Alves, seção 0368, há erro que orienta desligar e ligar a urna. Em Sena Madureira, seção 0084, houve confirmação de um cargo e tentativas de suspensão antes do desligamento. A mensagem de chave desligada não informa quem acionou o mecanismo. As atas e os atendimentos técnicos devem esclarecer esses casos.')
p(I,'Houve 39 seções com múltiplos blocos de histórico. Quatro tinham duas origens com identificadores de equipamento diferentes no dia. Elas são: Bujari 0009/0002; Cruzeiro do Sul 0004/0394; Sena Madureira 0003/0084; Senador Guiomard 0008/0082. Em Bujari, o primeiro bloco não tinha votações registradas.')
p(I,'Dez seções foram separadas da comparação estatística: sete por interrupção e quatro por duas origens no dia, com uma seção comum aos dois grupos. Os totais dessas seções permanecem no universo estadual; a exclusão afeta apenas a comparação com pares. A relação completa e os motivos constam dos anexos 01 a 04.')
p(I,'Não houve erro de leitura, classificação indefinida ou mensagem de voto computado sem liberação associada. A diferença entre as 453.714 liberações e as 453.654 votações concluídas fecha em 53 suspensões explícitas sem voto e sete interrupções.')
I=section('9. Conclusão e conferências recomendadas')
p(I,'O Acre registra 37.979 votações concluídas com liberação por mesário ou confirmação do ano de nascimento. O total é relevante para delimitar a verificação de possível votação em nome de ausentes, inclusive em ocorrências isoladas.')
p(I,'A análise localizou concentração dos dois procedimentos em 41 seções, com 2.458 votações do conjunto. Foram identificadas também 1.620 conclusões em até dez segundos, incluindo 114 após espera de pelo menos cinco minutos por identificação. Esses conjuntos se sobrepõem; não representam números de fraudes a serem somados.')
p(I,'As maiores sequências não mostraram intervalos de poucos segundos entre as liberações. A conclusão curta, isoladamente, também ocorre entre eleitores identificados por biometria. Os dados permitem selecionar ocorrências para conferência, mas não demonstram quem estava fisicamente na seção.')
p(I,'A investigação deve priorizar:')
b(I,'As 41 seções com concentração elevada, confrontando o comparecimento registrado e o perfil de cadastramento biométrico do eleitorado.')
b(I,'Os registros de espera e conclusão curta, verificando se há justificativa operacional e correspondência com o atendimento efetivamente realizado.')
b(I,'As assinaturas nos casos em que são exigidas, as atas e os registros técnicos, para esclarecer utilização de procedimentos complementares e eventuais falhas de leitor.')
b(I,'As sete interrupções e as mudanças de identificador de equipamento, verificando continuidade, motivo da intervenção e destino do atendimento ao eleitor afetado.')
p(I,'A confirmação de fraude por voto em nome de ausente exige demonstrar que uma pessoa registrada como votante não compareceu e que houve uso indevido de sua habilitação. Essa demonstração não pode ser obtida apenas pela quantidade de liberações, pelo tempo ou por sequências anônimas do log.')
I=section('10. Fontes e método')
p(I,'Foram examinados 2.270 logs, correspondentes às 2.270 seções principais da configuração oficial do Acre. A análise de tempos foi refeita sobre o pacote bruto do TSE, conferindo as contagens por seção e preservando a referência de origem e linha de cada votação.')
p(I,'A comparação de proporções utilizou seções do mesmo município e zona, com pelo menos cem votações concluídas e grupo mínimo de vinte seções. O limite foi o terceiro quartil mais três vezes o intervalo interquartil, exigindo também diferença superior a dez pontos percentuais da mediana. É um critério de triagem, sem ajuste individual pelo cadastramento biométrico. Foram comparadas 2.200 seções. Santa Rosa do Purus não atingiu o tamanho mínimo de grupo.')
p(I,'A duração foi calculada entre liberação e voto computado. O intervalo entre liberações e a espera por identificação foram tratados separadamente. Os horários foram reproduzidos como constam nos equipamentos, sem conversão de fuso e sem presumir sincronização externa dos relógios.')
p(I,'Os dados não identificam o candidato escolhido e não foram usados para atribuir voto individual. A análise não realizou perícia de hardware, validação criptográfica de assinaturas nem conferência dos cadernos de votação. Os arquivos de dados permitem reproduzir os recortes sem depender dos exemplos apresentados nas tabelas.')
p(I,'Fonte de resultados e originais selecionados: '+source['asset']['browser_download_url'])
p(I,'Pacote bruto oficial: '+s['url_pacote'])
p(I,'Configuração oficial: '+s['url_config'])
p(I,'Execução e código: https://github.com/hugohalima-hash/auditoria_eleicoes_2026/actions/runs/41263277696. Commit de origem: 83d6bed1523a4ec20d9a55dce4e7aaa49646023d.')
p(I,'Integridade do pacote publicado - SHA-256: '+source['sha256_download'])
p(I,'Anexos: totais das 2.270 seções; registros das 37.979 votações do conjunto; 41 seções com proporção elevada; referências de comparação; votações curtas; ocorrências após pausas e esperas; sequências concluídas; e relações das interrupções e dos históricos múltiplos. Cada linha de votação contém arquivo, origem e linhas do log para conferência.')
# Markdown and PDF share the same narrative and tables.
md=['# Acre - habilitação por mesário e ano de nascimento','','> Relatório de auditoria dos registros de votação. Segundo turno de 25/10/2026. Versão revisada de 01/11/2026.','']
for sec in sections:
 md+=['## '+sec['title'],'']
 for item in sec['items']:
  if item[0]=='p':md += [item[1],'']
  elif item[0]=='b':md += ['- '+item[1],'']
  else:
   _,heads,rs,_=item;clean=lambda x:str(x).replace('|',' / ').replace('\n',' ')
   md+=['| '+' | '.join(map(clean,heads))+' |','| '+' | '.join(['---']*len(heads))+' |']+['| '+' | '.join(map(clean,r))+' |' for r in rs]+['']
(out/'RELATORIO_COMPLETO_AC.md').write_text('\n'.join(md))
# Presentation.
for name,file in [('DV','DejaVuSans.ttf'),('DV-Bold','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='BodyAC2',fontName='DV',fontSize=9.5,leading=13.2,spaceAfter=8,textColor=colors.HexColor('#223549')));styles.add(ParagraphStyle(name='TitleAC2',fontName='DV-Bold',fontSize=18,leading=22,spaceAfter=13,textColor=colors.HexColor('#163c5c')));styles.add(ParagraphStyle(name='CellAC2',fontName='DV',fontSize=7.5,leading=10));styles.add(ParagraphStyle(name='HeadAC2',fontName='DV-Bold',fontSize=7.4,leading=10,textColor=colors.white));styles.add(ParagraphStyle(name='SmallAC2',fontName='DV',fontSize=7.2,leading=10.3,spaceAfter=7,textColor=colors.HexColor('#455c73')))
def par(text,style='BodyAC2'):return Paragraph(html.escape(str(text)),styles[style])
story=[]
for i,sec in enumerate(sections):
 if i:story.append(PageBreak())
 story.append(par(sec['title'],'TitleAC2'))
 for item in sec['items']:
  if item[0] in ('p','b'):
   txt=('• ' if item[0]=='b' else '')+item[1];sty='SmallAC2' if txt.startswith(('Fonte de resultados','Pacote bruto','Configuração oficial','Execução e código','Integridade do pacote')) else 'BodyAC2';story.append(par(txt,sty))
  else:
   _,heads,rs,widths=item;scale=174*mm/sum(widths);widths=[v*scale for v in widths]
   body=[[par(x,'HeadAC2') for x in heads]]+[[par(x,'CellAC2') for x in r] for r in rs];tbl=Table(body,colWidths=widths,repeatRows=1,hAlign='LEFT');padding=1.65 if len(rs)>30 else 3.5
   tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#173c5c')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f0f4f7')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),padding),('BOTTOMPADDING',(0,0),(-1,-1),padding),('LINEBELOW',(0,0),(-1,0),.5,colors.HexColor('#173c5c')),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#d7e0e8'))]));story += [tbl,Spacer(1,10)]
class Numbered(canvas.Canvas):
 def __init__(self,*a,**kw):super().__init__(*a,**kw);self.states=[]
 def showPage(self):self.states.append(dict(self.__dict__));self._startPage()
 def save(self):
  for state in self.states:
   self.__dict__.update(state);self.setStrokeColor(colors.HexColor('#ccd7e1'));self.line(18*mm,17*mm,192*mm,17*mm);self.setFont('DV',7);self.setFillColor(colors.HexColor('#52667b'));self.drawString(18*mm,12*mm,'ACRE | Habilitação por mesário e ano de nascimento');self.drawRightString(192*mm,12*mm,f'{self._pageNumber} / {len(self.states)}');super().showPage()
  super().save()
SimpleDocTemplate(str(out/'Relatorio_Completo_Acre.pdf'),pagesize=(210*mm,297*mm),leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,title='Acre - Habilitação por mesário e ano de nascimento',author='Auditor Eleitoral Independente 2026').build(story,canvasmaker=Numbered)
# The data package includes every target vote, not just table examples.
with zipfile.ZipFile(out/'Dados_Acre_Habilitacoes_e_Tempos.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 checks=[]
 for path in sorted(ann.glob('*.csv'))+[out/'RELATORIO_COMPLETO_AC.md',out/'evidencias_relatorio_revisado.json']:
  name=('anexos/'+path.name) if path.parent==ann else path.name;z.write(path,name);checks.append(hashlib.sha256(path.read_bytes()).hexdigest()+'  '+name)
 z.writestr('SHA256SUMS.txt','\n'.join(checks)+'\n')
print('PDF, Markdown e pacote integral de dados produzidos.')
