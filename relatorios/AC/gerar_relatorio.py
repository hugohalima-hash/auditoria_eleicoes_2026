from pathlib import Path
from collections import defaultdict,Counter
from datetime import datetime
import csv,io,json,zipfile,hashlib,sys,html,re
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

base=Path(__file__).parent;data=base/'dados';out=base/'output';out.mkdir(exist_ok=True);ann=out/'anexos';ann.mkdir(exist_ok=True)
s=json.loads((data/'resultados/AC/resumo.json').read_text());tri=json.loads((data/'triagem/resumo.json').read_text());conf=json.loads((data/'conferencias/AC/conferencia.json').read_text());source=json.loads((base/'fonte_publicada.json').read_text());execution=json.loads((data/'conferencias/AC/execucao.json').read_text())
def rows(name):return list(csv.DictReader(open(data/name,encoding='utf-8-sig')))
urnas=rows('resultados/AC/urnas.csv');runs=rows('resultados/AC/sequencias.csv');alerts=rows('triagem/alertas.csv');quar=rows('triagem/quarentena.csv');refs=rows('triagem/referencias_comparacao.csv');warnings=rows('resultados/AC/avisos.csv')
cfg=json.loads((data/'resultados/AC/config_oficial.json').read_text());names={str(m['cd']).zfill(5):m['nm'] for a in cfg['abr'] for m in a.get('mu',[])}
byfile={r['arquivo']:r for r in urnas}
def num(v):return f'{int(v):,}'.replace(',','.')
def pct(a,b):return f'{100*int(a)/int(b):.2f}%'.replace('.',',')
def write_csv(name,rs,fields=None):
 with (ann/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields or list(rs[0]),extrasaction='ignore');w.writeheader();w.writerows(rs)
# Source integrity is checked again against all state result hashes.
with zipfile.ZipFile(base/'AC-publicado.zip') as z:
 manifesto=json.loads(z.read('resultados/AC/manifesto.json'))
 for name,digest in manifesto['arquivos'].items():assert hashlib.sha256(z.read('resultados/AC/'+name)).hexdigest()==digest
 assert execution['commit_fonte']=='83d6bed1523a4ec20d9a55dce4e7aaa49646023d'
 repo=next(p for p in [base.parent/'github_project',base.parent.parent,Path.cwd()] if (p/'motor.py').exists());sys.path.insert(0,str(repo));from motor import read_logs
 block_rows=[]
 for q in quar:
  if 'blocos_distintos=2' not in q['motivo']:continue
  groups=defaultdict(list)
  for src,n,l in read_logs(z.read('originais/AC/'+q['arquivo']))[0]:
   p=l.split('\t')
   if len(p)==6 and p[0].startswith('25/10/2026'):groups[src].append((n,p))
  for src,ls in groups.items():
   block_rows.append(dict(municipio=q['municipio_nome'],zona=q['zona'],secao=q['secao'],arquivo=q['arquivo'],origem=src,
    equipamento=';'.join(sorted({p[2] for _,p in ls})),inicio=ls[0][1][0],fim=ls[-1][1][0],
    habilitacoes=sum(p[4]=='Eleitor foi habilitado' for _,p in ls),votos_computados=sum(p[4]=='O voto do eleitor foi computado' for _,p in ls)))
 # Manually interpreted cases, each linked to original log lines.
 descriptions={
 'o03221ac0102300010608-log.jez':('10:54:30',7598,'Desligamento após habilitação biométrica, sem justificativa explícita no intervalo.','A última habilitação ocorre às 10:54:13; o desligamento aparece 17 segundos depois. Não há evento de voto computado entre esses registros.','10:58:25','Verificar a ata e o atendimento dado ao eleitor após o reinício. O retorno à espera por identificação não identifica quem voltou a votar.'),
 'o03221ac0107400040482-log.jez':('08:25:52',6779,'Desligamento após habilitação biométrica, sem justificativa explícita no intervalo.','O eleitor foi habilitado às 08:25:35 e o desligamento ocorre 17 segundos depois. O trecho não informa a decisão que motivou o acionamento da chave.','08:31:02','Confrontar a ocorrência com a ata e os registros de atendimento técnico, sem atribuir intenção a partir do desligamento.'),
 'o03221ac0108200040368-log.jez':('09:35:06',5264,'Erro explícito informando que o voto não foi registrado, seguido de desligamentos.','Às 09:34:45, há erro 5362 com orientação para desligar e ligar a urna; às 09:34:46 aparece ERROR -44. Após o primeiro desligamento, o histórico registra outros às 09:42:14, 09:50:33 e 10:02:43.','10:11:42','Priorizar a conferência do atendimento ao eleitor e da intervenção técnica. O erro informa falha de registro daquele ciclo; não comprova perda dos votos anteriores.'),
 'o03221ac0139200010554-log.jez':('12:28:19',9284,'Tecla indevida registrada antes do desligamento; causa do acionamento não explicitada.','A habilitação ocorre às 12:28:05, há tecla indevida às 12:28:17 e desligamento às 12:28:19. A proximidade temporal não demonstra que a tecla causou ou justificou a decisão.','12:32:50','Verificar o relato na ata; não converter sequência temporal em causa comprovada.'),
 'o03221ac0139200090053-log.jez':('14:30:25',9508,'Desligamento seis segundos após habilitação biométrica, sem justificativa explícita no intervalo.','A habilitação ocorre às 14:30:19 e a chave é desligada às 14:30:25, sem mensagem de voto computado entre os dois eventos.','14:35:48','Conferir motivo e destino do atendimento ao eleitor. A duração curta não comprova que houve voto registrado ou intenção irregular.'),
 'o03221ac0145700030001-log.jez':('08:55:44',7275,'Desligamento 24 segundos após habilitação biométrica, sem justificativa explícita no intervalo.','O eleitor é habilitado às 08:55:20 e o desligamento é registrado às 08:55:44, sem voto computado associado antes da interrupção.','09:00:58','Confrontar ata, atendimento técnico e retomada do atendimento, preservando o sigilo do voto.'),
 'o03221ac0145700030084-log.jez':('10:10:29',6755,'Interação prolongada, confirmação de um cargo e tentativas de suspensão antes do desligamento.','A habilitação ocorre às 09:39:13; há confirmação de Governador às 09:39:22, teclas indevidas e períodos sem atividade. O log registra retorno à digitação durante tentativas de suspensão às 09:42:26, 09:49:41 e 10:07:51. O desligamento ocorre 31 minutos e 16 segundos após a habilitação.','Não fixado neste relatório','Verificar ata, contingência e reconciliação com BU/RDV. Confirmar um cargo não foi tratado como prova de voto computado do ciclo. A continuidade entre equipamentos não é presumida pelo analisador.')}
 cases=[]
 for w in warnings:
  r=byfile[w['arquivo']];off,offln,reason,detail,resume,nextstep=descriptions[w['arquivo']]
  ls=list(read_logs(z.read('originais/AC/'+w['arquivo']))[0]);target=int(w['linha']);stamp=next(l.split('\t')[0] for src,n,l in ls if src==w['origem'] and n==target)
  elapsed=int((datetime.strptime(off,'%H:%M:%S')-datetime.strptime(stamp[11:],'%H:%M:%S')).total_seconds())
  cases.append(dict(municipio=names[r['municipio']],zona=r['zona'],secao=r['secao'],arquivo=w['arquivo'],origem=w['origem'],habilitacao=stamp[11:],desligamento=off,intervalo_seg=elapsed,linha_habilitacao=target,linha_desligamento=offln,motivo_observado=reason,detalhe=detail,retomada_espera=resume,verificacao_pendente=nextstep))
municipal=defaultdict(Counter)
for r in urnas:
 c=municipal[r['municipio']];c['logs']+=1
 for k in ['habilitacoes','votos_computados','com_evento_mesario','suspensas_sem_voto','ciclos_sem_desfecho_explicado']:c[k]+=int(r[k])
 c['quarentena']+=r['admissivel_estatistica']!='True'
municipal_rows=[dict(municipio=names[k],**dict(c)) for k,c in sorted(municipal.items(),key=lambda x:names[x[0]])]
blocks=[dict(municipio=names[r['municipio']],zona=r['zona'],secao=r['secao'],blocos_pacote=int(r['blocos_log']),origens_no_dia=int(r['blocos_distintos']),quarentena='Sim' if r['admissivel_estatistica']!='True' else 'Não',arquivo=r['arquivo']) for r in urnas if int(r['blocos_log'])>1]
write_csv('01_interrupcoes.csv',cases);write_csv('02_quarentena.csv',quar);write_csv('03_multiplos_blocos.csv',blocks);write_csv('04_blocos_do_dia.csv',block_rows);write_csv('05_resumo_municipal.csv',municipal_rows);write_csv('06_alertas_integrais.csv',alerts);write_csv('07_referencias_comparacao.csv',refs)
assert len(cases)==7 and len(blocks)==39 and len(quar)==10 and len(alerts)==53
assert sum(x['habilitacoes'] for x in municipal_rows)==453714
assert len({x['arquivo'] for x in alerts})==45

# One structured narrative is used for both Markdown and PDF.
sections=[]
def section(title):
 q={'title':title,'items':[]};sections.append(q);return q['items']
def p(items,text):items.append(('p',text))
def table(items,headers,data,widths=None):items.append(('t',headers,data,widths))
def bullet(items,text):items.append(('b',text))
I=section('1. Síntese executiva')
p(I,'Relatório técnico documental dos logs públicos do Acre, segundo turno de 25/10/2026. Documento datado de 31/10/2026. Motor 3.0, execução GitHub Actions 41263277696. Não é perícia de hardware, certificação de software nem validação da identidade de votantes.')
table(I,['Indicador','Resultado'],[['Logs processados / lista principal oficial','2.270 / 2.270 (100%)'],['Municípios abrangidos','22'],['Habilitações / votos computados','453.714 / 453.654'],['Erros de leitura / categorias indefinidas','0 / 0'],['Comparação estatística com pares','2.200 seções; nenhum alerta pelos critérios aplicados'],['Conferência independente de contagens','2.231 logs; nenhuma divergência'],['Interrupções pendentes','7 ciclos em 7 seções'],['Seções com vários blocos no pacote','39; quatro com duas origens no dia analisado'],['Quarentena / seções admitidas','10 / 2.260'],['Alertas técnicos / seções distintas','53 itens / 45 seções']],[92,82])
p(I,'O achado de maior prioridade para conferência técnica é Rodrigues Alves, zona 0004, seção 0368: há erro explícito de voto não registrado e desligamentos sucessivos. Sena Madureira, zona 0003, seção 0084, apresenta um ciclo prolongado com confirmação de cargo, tentativas de suspensão e posterior desligamento. Os outros cinco casos não têm justificativa explícita de desligamento no intervalo examinado; em um deles há tecla indevida pouco antes.')
p(I,'Não foram sinalizadas proporções elevadas de eventos de mesário nem volumes elevados de habilitações entre as seções efetivamente comparadas. Isso não comprova regularidade de todos os aspectos da eleição. Os 53 itens são sinais de registro e contexto, não 53 votos suspeitos ou 53 fraudes. Não há acurácia semântica de 99,9% certificada.')
p(I,'Todos os números se referem ao pacote publicado do AC, e não à execução antiga do motor 2.1. As classificações antigas e os alertas nacionais derivados delas permanecem retirados de uso para conclusões até reprocessamento.')
I=section('2. Escopo, fontes e cobertura efetivamente avaliada')
p(I,'Fonte primária: pacote de arquivos do TSE do segundo turno do Acre; fonte operacional desta análise: AC-tentativa1.zip da Release auditoria-v3-41263277696. O ativo publicado foi baixado novamente para este relatório e conferido contra o digest do GitHub, os 129 itens de SHA256SUMS.txt e os sete arquivos do manifesto estadual. O commit registrado no pacote é 83d6bed1523a4ec20d9a55dce4e7aaa49646023d.')
p(I,'A configuração oficial lista 2.270 seções principais e 141 agregadas. A cobertura de 100% compara os logs com as seções principais; não transforma as agregadas em outras 141 urnas independentes nem certifica o conjunto da eleição. Não há seção principal ausente, seção processada fora da configuração ou erro de leitura registrado.')
table(I,['Camada de avaliação','Seções / logs','Interpretação'],[['Leitura e contagens do motor','2.270','Inventário completo da lista principal'],['Portão de qualidade','2.260 aceitas; 10 excluídas','Quarentena não é declaração de fraude'],['Critério de tamanho mínimo','2.215 aceitas com >=100 habilitações','45 aceitas têm menos de 100'],['Comparação entre pares','2.200 em 22 grupos','15 elegíveis de Assis Brasil não formam grupo mínimo de 20'],['Conferência por leitor independente','2.231','39 com múltiplos blocos históricos não foram presumidos comparáveis']],[47,40,87])
p(I,'As 70 seções fora da comparação com pares se dividem em dez por qualidade, 45 por tamanho inferior a cem habilitações e 15 por grupo comparável menor que vinte seções. Assim, ausência de alerta estatístico não equivale a teste estatístico individual das 2.270 seções.')
p(I,'Datas e horários são reproduzidos como registrados nos equipamentos, sem normalização de fuso ou demonstração de sincronização externa dos relógios. Um horário isolado não foi tratado como prova de abertura antecipada ou votação fora do período permitido.')
I=section('3. Contagens, categorias e balanços')
categories=[('Biométrica','biometrica'),('Autorização explícita de mesário','mesario_explicito'),('Captura de digital de mesário com indicação de nova gravação','digital_mesario_gravada'),('Digital de mesário sem associação nominal no log','digital_mesario_sem_associacao'),('Ano de nascimento sem evento biométrico reconhecido','ano_nascimento_sem_evento_biometrico'),('Outros tipos','tipo_outro'),('Indefinidas','indefinida')]
table(I,['Classificação do motor','Habilitações','Com voto vinculado','Sem voto vinculado'],[[label,num(s[k]),num(s[k+'_com_voto']),num(s[k]-s[k+'_com_voto'])] for label,k in categories]+[['TOTAL','453.714','453.654','60']],[85,29,30,30])
p(I,'Neste relatório, votos computados são mensagens de conclusão do ciclo do eleitor. Não são a soma dos votos por cargo, nem uma contagem de votos de candidatos específicos. Confirmações de cargos e conclusão do ciclo são eventos diferentes.')
p(I,'As categorias são mutuamente exclusivas na classificação. A categoria de nova digital conserva o nome técnico do motor; sua evidência é a captura seguida da mensagem de que a digital será salva, não uma verificação pericial da gravação física. A classificação é feita ao fechar o ciclo, aceitando evidência tardia; conflitos e casos não suportados não são presumidos como mesário.')
p(I,'O grupo com eventos de mesário reúne 22.661 habilitações (4,99% do total), das quais 22.654 têm evento de voto vinculado. O grupo ampliado sem evento biométrico reconhecido soma 37.990 (8,37%), já incluindo as 22.661 e acrescentando 15.329 confirmações de ano de nascimento. Esses dois totais não devem ser somados. O grupo ampliado não informa se havia biometria cadastrada nem equivale ao indicador de biometria não reconhecida do BU.')
p(I,'Balanço das habilitações: 453.714 = 453.654 com voto computado + 53 suspensões explícitas sem voto + 0 cancelamentos explícitos nessa categoria de desfecho + 7 ciclos interrompidos pendentes. O resíduo é zero. Balanço dos votos computados: 453.654 = 453.654 vinculados + 0 sem habilitação associada. O resíduo também é zero.')
p(I,'Há 51 mensagens de suspensão parcial, contabilizadas separadamente; não são outros 51 votos a acrescentar ao total. Há 3.065 eventos de cancelamento antes da habilitação; representam etapas de tentativa, não 3.065 votos computados ou necessariamente 3.065 pessoas diferentes. Cancelamento antes da habilitação e suspensão de eleitor já habilitado são situações distintas.')
I=section('4. Resumo integral dos 22 municípios')
table(I,['Município','Logs','Habilit.','Votos','Mesário','% mes.','Susp.','Pend.','Quar.'],[[r['municipio'],num(r['logs']),num(r['habilitacoes']),num(r['votos_computados']),num(r['com_evento_mesario']),pct(r['com_evento_mesario'],r['habilitacoes']),num(r['suspensas_sem_voto']),num(r['ciclos_sem_desfecho_explicado']),num(r.get('quarentena',0))] for r in municipal_rows],[39,12,22,22,21,17,13,14,14])
p(I,'Mesário: habilitações com eventos do grupo de mesário, não acusação de intervenção irregular. Susp.: suspensões explícitas sem voto. Pend.: ciclos sem desfecho de voto explicado pelo motor. Quar.: seções fora da comparação estatística. Percentuais usam todas as habilitações do município, inclusive as de seções em quarentena; são descritivos, não testes estatísticos municipais.')
I=section('5. As sete interrupções: visão geral')
table(I,['Município','Zona / seção','Habilitação','Desliga','Intervalo'],[[r['municipio'],r['zona']+' / '+r['secao'],r['habilitacao'],r['desligamento'],str(r['intervalo_seg'])+' s'] for r in cases],[49,35,30,30,30])
p(I,'Todos os sete avisos estaduais são do tipo ciclo_interrompida. Isso significa que um ciclo aberto foi interrompido antes de uma mensagem de voto computado associada, não que os votos anteriores da seção foram perdidos. A causa operacional da interrupção e o desfecho do atendimento ao eleitor são questões diferentes: é possível conhecer o desligamento sem saber se o eleitor foi atendido novamente.')
p(I,'A mensagem de desligamento pela chave não identifica a pessoa que acionou o mecanismo. O relatório não atribui autoria nem intenção. Nas seis primeiras ocorrências abaixo, o horário de retomada indica a volta à espera por identificação, não o retorno comprovado do mesmo eleitor.')
p(I,'Prioridade de esclarecimento: (a) Rodrigues Alves 0368, pela falha explícita e reinícios sucessivos; (b) Sena Madureira 0084, pela interação prolongada, confirmação parcial e mudança de identificador de equipamento; (c) os outros cinco, pela necessidade de justificativa e acompanhamento do atendimento na ata. É prioridade documental, não escala de fraude.')
for part,subset in enumerate([cases[:3],cases[3:5],cases[5:]],1):
 I=section(f'6.{part}. Evidências das interrupções')
 for r in subset:
  p(I,r['municipio']+' - zona '+r['zona']+', seção '+r['secao'])
  p(I,'Habilitação '+r['habilitacao']+'; desligamento '+r['desligamento']+'; intervalo '+str(r['intervalo_seg'])+' segundos. '+r['motivo_observado'])
  p(I,r['detalhe'])
  p(I,'Após a intervenção, retorno observado à espera por identificação: '+r['retomada_espera']+'. '+r['verificacao_pendente'])
  p(I,'Referência: '+r['arquivo']+'; origem '+r['origem']+'; habilitação na linha '+str(r['linha_habilitacao'])+' e desligamento na linha '+str(r['linha_desligamento'])+'.')
I=section('7. Relação integral das 39 seções com múltiplos blocos')
p(I,'O pacote contém 2.231 logs com um bloco, 36 com dois e três com três. Ter vários blocos não demonstra voto duplicado ou troca de equipamento durante a votação. Em 35 das 39 seções, somente uma origem tem registros do dia analisado; em quatro, há duas. Não foram removidas linhas por deduplicação neste estado.')
table(I,['Município','Zona','Seção','Blocos no pacote','Origens no dia','Quarentena'],[[r['municipio'],r['zona'],r['secao'],r['blocos_pacote'],r['origens_no_dia'],r['quarentena']] for r in blocks],[54,20,20,29,29,22])
I=section('8. Quatro seções com duas origens no dia da votação')
p(I,'A leitura dos originais preservados mostra dois identificadores de equipamento diferentes em cada uma dessas quatro seções. A tabela reproduz registros do dia e contagens literais por bloco. Não pressupõe que o intervalo entre blocos seja a duração exata de uma paralisação.')
table(I,['Município / seção','ID equipamento','Primeiro / último registro','Habilit.','Votos'],[[r['municipio']+' / '+r['secao'],r['equipamento'],r['inicio'][11:]+' / '+r['fim'][11:],num(r['habilitacoes']),num(r['votos_computados'])] for r in block_rows],[53,34,47,20,20])
p(I,'Bujari 0002: o primeiro identificador não tem habilitações nem votos computados; a mudança aparece em registros anteriores ao atendimento de eleitores. Não há base para qualificá-la como substituição durante um voto. Cruzeiro do Sul 0394, Sena Madureira 0084 e Senador Guiomard 0082 têm votos computados nos dois blocos. A ata e os registros de contingência devem explicar as transições.')
p(I,'Em Cruzeiro do Sul 0394, o primeiro bloco tem 208 habilitações e 207 votos computados; essa diferença não gerou ciclo pendente e integra o balanço de suspensões explícitas. Em Sena Madureira 0084, a diferença de uma habilitação no primeiro bloco corresponde ao ciclo interrompido já descrito. Não se presume que uma habilitação do bloco novo seja a continuação do mesmo eleitor.')
p(I,'A existência dos blocos não prova, por si só, que a transferência de votos foi correta ou incorreta. É necessário reconciliar registros de contingência, BU, RDV, configurações e ata. Esta versão não realizou essa reconciliação de conteúdo dos votos.')
I=section('9. As dez seções em quarentena')
table(I,['Município','Zona / seção','Motivo de exclusão'],[[r['municipio_nome'],r['zona']+' / '+r['secao'],r['motivo'].replace('avisos=1; ciclos_sem_desfecho_explicado=1','Um ciclo interrompido').replace('blocos_distintos=2','Duas origens no dia')] for r in quar],[48,34,92])
p(I,'Sete seções têm ciclo interrompido; quatro têm duas origens no dia. Sena Madureira 0084 pertence aos dois grupos. Assim, 7 + 4 - 1 = 10 seções distintas, e não onze. Quarentena é uma barreira de avaliação do programa; não significa voto anulado, seção não apurada ou fraude.')
p(I,'Os 53 itens de alerta se decompõem em 39 registros de múltiplos blocos, sete avisos e sete itens de ciclo pendente. Os últimos dois conjuntos se referem aos mesmos sete casos. Como uma dessas seções também tem múltiplos blocos, são 45 seções distintas com algum item de contexto ou alerta técnico.')
p(I,'O relatório preserva os casos excluídos em vez de transformá-los em zero ou eliminá-los da documentação. O ZIP publicado contém os originais das seções em quarentena e controles determinísticos, acompanhados de hashes. Os identificadores pessoais eventualmente presentes em mensagens não são reproduzidos neste relatório.')
I=section('10. Critérios estatísticos, séries e ausência de alertas')
p(I,'A comparação usa seções do mesmo município e zona: mínimo de vinte seções aceitas, cada uma com pelo menos cem habilitações. O limite exploratório é Q3 + 3 vezes o intervalo interquartil. Exige-se também diferença superior a dez pontos percentuais da mediana para proporção de mesário ou a cinquenta habilitações para volume. A própria seção participa da referência. Não é p-valor, probabilidade de fraude ou ajuste por biometria cadastrada e eleitores aptos.')
table(I,['Grupo','Séries >=2','>=3','>=5','>=10','>=20'],[[g]+[num(sum(x['grupo']==key and int(x['tamanho'])>=n for x in runs)) for n in [2,3,5,10,20]] for g,key in [('Eventos de mesário','mesario'),('Grupo ampliado','sem_biometria')]],[54,24,24,24,24,24])
p(I,'São séries máximas de habilitações; uma série de dez aparece nas faixas de dois, três, cinco e dez. As colunas não podem ser somadas. A maior série de mesário tem seis habilitações, abaixo do limiar fixo de dez da triagem. A maior do grupo ampliado tem dez; esse grupo também inclui confirmação de ano de nascimento, e não apenas intervenção de mesário.')
selected=[]
for group,count in [('mesario',2),('sem_biometria',1)]:
 selected.extend(sorted([r for r in runs if r['grupo']==group],key=lambda x:(-int(x['tamanho']),x['arquivo'],x['inicio']))[:count])
table(I,['Grupo / município','Zona / seção','Série','Início / fim'],[[('Mesário' if r['grupo']=='mesario' else 'Ampliado')+' / '+names[byfile[r['arquivo']]['municipio']],byfile[r['arquivo']]['zona']+' / '+byfile[r['arquivo']]['secao'],r['tamanho'],r['inicio'][11:]+' / '+r['fim'][11:]] for r in selected],[62,35,20,57])
p(I,'Essas maiores séries são referências descritivas, não novas suspeitas. Não houve alerta de proporção elevada nem de volume elevado entre as 2.200 seções comparadas. O detector de intervalo médio inferior a trinta segundos só examina séries de mesário com dez ou mais habilitações; como nenhuma atingiu esse tamanho, ele não fornece uma avaliação global da velocidade de votação no Acre. Também não houve análise de votação por candidato.')
I=section('11. Referências completas da comparação com pares')
p(I,'As proporções abaixo são expressas em porcentagem; os limites de volume estão em habilitações. Cada linha resume um grupo município/zona. O limiar adicional de diferença da mediana, descrito na seção anterior, também precisa ser satisfeito para gerar alerta.')
paired=defaultdict(dict)
for r in refs:paired[(r['municipio'],r['zona'])][r['metrica']]=r
table(I,['Município / zona','N','Mediana mes.','Limite mes.','Mediana vol.','Limite vol.'],[[names[m]+' / '+zone,ps['proporcao_mesario']['secoes'],f"{100*float(ps['proporcao_mesario']['mediana']):.2f}%".replace('.',','),f"{100*float(ps['proporcao_mesario']['limite_superior']):.2f}%".replace('.',','),f"{float(ps['volume_habilitacoes']['mediana']):.1f}".replace('.',','),f"{float(ps['volume_habilitacoes']['limite_superior']):.1f}".replace('.',',')] for (m,zone),ps in sorted(paired.items(),key=lambda x:(names[x[0][0]],x[0][1]))],[56,12,27,27,26,26])
p(I,'Assis Brasil tem quinze seções elegíveis e não atinge o mínimo de vinte, portanto não entra nessa comparação. Os CSVs anexos preservam as referências com precisão completa; valores da tabela foram arredondados apenas para leitura.')
I=section('12. Conclusões e verificações pendentes')
bullet(I,'A cobertura de leitura da lista principal está completa e não há divergência nas contagens literais dos 2.231 logs comparáveis pelo leitor independente. Isso não certifica a classificação semântica ou a autenticidade criptográfica dos dados.')
bullet(I,'Não foram encontrados alertas pelos critérios de proporção elevada de eventos de mesário ou volume elevado nas 2.200 seções comparadas. Ausência de alerta nesses critérios não certifica todos os aspectos das seções.')
bullet(I,'Sete ciclos foram interrompidos e dez seções ficaram fora da comparação. Os eventos não foram convertidos em votos extras, votos anulados ou fraudes presumidas. O motivo do acionamento da chave e a identidade de quem o acionou não são demonstrados pela mensagem de desligamento.')
bullet(I,'Os votos dos eleitores anteriores não podem ser considerados perdidos apenas por haver desligamento. Por outro lado, este relatório não verificou a persistência nem a transferência de cada voto com BU/RDV e documentos de contingência. A igualdade de contagens de log não substitui essa verificação.')
bullet(I,'Próximo passo documental: obter atas das sete seções com ciclos interrompidos e das quatro com transição de identificador; conferir motivo, equipe responsável, horários, equipamentos e atendimento ao eleitor afetado. Sena Madureira 0084 consta nos dois conjuntos.')
bullet(I,'Próximo passo técnico: reconciliar BU/RDV, relatórios de contingência e dados transmitidos, mantendo a distinção entre voto por cargo, ciclo do eleitor e mensagem de voto computado. Uma mensagem de confirmação de Governador, isoladamente, não resolve essa reconciliação.')
bullet(I,'Não é possível identificar o retorno do mesmo eleitor por mera sequência de horários, nem revelar suas escolhas. Não há base de referência independente suficiente para certificar acurácia de 99,9%. A análise não verifica hardware, software instalado, assinaturas criptográficas ou presença física dos votantes.')
p(I,'Conclusão do escopo: há leitura integral da lista principal, balanços internos fechados e pontos técnicos localizados para esclarecimento. Não há neste material demonstração de fraude, nem demonstração pericial de regularidade integral da eleição do Acre.')
I=section('13. Proveniência, reprodução e anexos')
table(I,['Objeto','Identificador'],[['Motor e executor - SHA-256',s['sha256_motor']],['Commit congelado da execução',execution['commit_fonte']],['Pacote oficial TSE - SHA-256',conf['sha256_pacote']],['Pacote AC publicado - SHA-256',source['sha256_download']],['Contagem independente - SHA-256',conf['sha256_referencia']]],[55,119])
p(I,'Pacote publicado: '+source['asset']['name']+'; ativo GitHub '+str(source['asset']['id'])+'; atualização informada pela fonte: 01/11/2026 02:02:54 UTC, correspondente a 31/10/2026 23:02:54 em Brasília. Todas as contagens do relatório são dessa versão fixada. A verificação de SHA-256 demonstra identidade dos bytes conferidos, não autentica uma assinatura do TSE.')
p(I,'Arquivos do pacote utilizados: resultados/AC/resumo.json, urnas.csv, sequencias.csv, avisos.csv, config_oficial.json e manifesto.json; triagem/resumo.json, alertas.csv, quarentena.csv e referencias_comparacao.csv; conferencias/AC/conferencia.json e execucao.json; originais/AC/*.jez e manifesto_amostras.json. O arquivo urnas.csv contém todas as 2.270 seções. O pacote inclui também a referência de contagem independente e os checksums.')
p(I,'Reprodução: obter o commit congelado; executar o motor para AC e a conferência de contagens com o pacote oficial; verificar o manifesto; executar anomalias.py. O script executar_estado.py automatiza essas etapas. Para uma reprodução exata de bytes, preservar o pacote publicado, pois duração e horário de execução mudam em uma nova rodada.')
references=[('F1 - Pacote publicado e dados completos',source['asset']['browser_download_url']),('F2 - Execução persistente','https://github.com/hugohalima-hash/auditoria_eleicoes_2026/actions/runs/41263277696'),('F3 - Configuração oficial das seções',s['url_config']),('F4 - Pacote bruto oficial do TSE',s['url_pacote']),('F5 - Regras de contingência e recuperação de 2026','https://www.tse.jus.br/legislacao/compilada/res/2026/resolucao-no-23-751-de-26-de-fevereiro-de-2026')]
for label,url in references:p(I,label+': '+url)
p(I,'Anexos estruturados deste relatório: 01_interrupcoes.csv (sete casos e linhas); 02_quarentena.csv (dez seções); 03_multiplos_blocos.csv (39 seções); 04_blocos_do_dia.csv (oito blocos das quatro seções); 05_resumo_municipal.csv (22 municípios); 06_alertas_integrais.csv (53 itens); 07_referencias_comparacao.csv (44 referências para 22 grupos). Eles não substituem os dados completos do pacote F1.')
# Save a compact evidence model so all tabulated claims can be reproduced.
(out/'evidencias_relatorio.json').write_text(json.dumps({'fonte':source,'resumo':s,'triagem':tri,'conferencia':conf,'casos':cases,'blocos_dia':block_rows},ensure_ascii=False,indent=2))
md=['# Relatório completo do Acre','', '> Análise documental dos logs públicos - segundo turno de 25/10/2026. Motor 3.0. Não há certificação de acurácia de 99,9%.','']
for sec in sections:
 md+=['## '+sec['title'],'']
 for item in sec['items']:
  if item[0]=='p':md += [item[1],'']
  elif item[0]=='b':md += ['- '+item[1],'']
  else:
   _,headers,rs,_=item
   def clean(x):return str(x).replace('|',' / ').replace('\n',' ')
   md+=['| '+' | '.join(map(clean,headers))+' |','| '+' | '.join(['---']*len(headers))+' |']
   md+=['| '+' | '.join(map(clean,r))+' |' for r in rs];md+=['']
(out/'RELATORIO_COMPLETO_AC.md').write_text('\n'.join(md))
# PDF layout.
pdfmetrics.registerFont(TTFont('DV','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DV-Bold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DV-Bold',italic='DV',boldItalic='DV-Bold')
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='BodyAC',fontName='DV',fontSize=9.2,leading=13,spaceAfter=8,textColor=colors.HexColor('#243346')))
styles.add(ParagraphStyle(name='TitleAC',fontName='DV-Bold',fontSize=18,leading=22,spaceAfter=13,textColor=colors.HexColor('#123453')))
styles.add(ParagraphStyle(name='CellAC',fontName='DV',fontSize=7.4,leading=10))
styles.add(ParagraphStyle(name='HeadAC',fontName='DV-Bold',fontSize=7.4,leading=10,textColor=colors.white))
styles.add(ParagraphStyle(name='SmallAC',fontName='DV',fontSize=7.1,leading=10,spaceAfter=6,textColor=colors.HexColor('#405269')))
def para(t,sty='BodyAC'):
 return Paragraph(html.escape(str(t)).replace('\n','<br/>'),styles[sty])
story=[]
for no,sec in enumerate(sections):
 if no:story.append(PageBreak())
 story.append(para(sec['title'],'TitleAC'))
 for item in sec['items']:
  if item[0] in ('p','b'):
   text=('• '+item[1]) if item[0]=='b' else item[1]
   # Long source paths and hashes use smaller type with wrapping.
   sty='SmallAC' if text.startswith(('Referência:','F1 -','F2 -','F3 -','F4 -','F5 -')) else 'BodyAC'
   story.append(para(text,sty))
  else:
   _,heads,rs,widths=item
   available=174*mm
   if widths:
    scale=available/sum(widths);widths=[w*scale for w in widths]
   else:widths=[available/len(heads)]*len(heads)
   body=[[para(v,'HeadAC') for v in heads]]+[[para(v,'CellAC') for v in row] for row in rs]
   t=Table(body,colWidths=widths,repeatRows=1,hAlign='LEFT')
   t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#173c5c')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),2 if len(rs)>=30 else 4),('BOTTOMPADDING',(0,0),(-1,-1),2 if len(rs)>=30 else 4),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f0f4f7')]),('LINEBELOW',(0,0),(-1,0),0.5,colors.HexColor('#173c5c')),('LINEBELOW',(0,1),(-1,-1),0.25,colors.HexColor('#d7e0e8'))]))
   story.extend([t,Spacer(1,10)])
class Numbered(canvas.Canvas):
 def __init__(self,*a,**kw):super().__init__(*a,**kw);self.states=[]
 def showPage(self):self.states.append(dict(self.__dict__));self._startPage()
 def save(self):
  count=len(self.states)
  for state in self.states:
   self.__dict__.update(state);self.footer(count);super().showPage()
  super().save()
 def footer(self,count):
  self.setStrokeColor(colors.HexColor('#ccd7e1'));self.line(18*mm,17*mm,192*mm,17*mm)
  self.setFont('DV',7);self.setFillColor(colors.HexColor('#52667b'));self.drawString(18*mm,12*mm,'ACRE | Análise documental de logs | Motor 3.0');self.drawRightString(192*mm,12*mm,f'{self._pageNumber} / {count}')
file=out/'Relatorio_Completo_Acre.pdf'
SimpleDocTemplate(str(file),pagesize=(210*mm,297*mm),rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,title='Relatório completo do Acre - Logs eleitorais 2026',author='Auditor Eleitoral Independente 2026',pageCompression=1).build(story,canvasmaker=Numbered)
print('PDF',file,'MD',out/'RELATORIO_COMPLETO_AC.md')
