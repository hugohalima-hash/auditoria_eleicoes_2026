# Relatório completo do Acre

> Análise documental dos logs públicos - segundo turno de 25/10/2026. Motor 3.0. Não há certificação de acurácia de 99,9%.

## 1. Síntese executiva

Relatório técnico documental dos logs públicos do Acre, segundo turno de 25/10/2026. Documento datado de 31/10/2026. Motor 3.0, execução GitHub Actions 41263277696. Não é perícia de hardware, certificação de software nem validação da identidade de votantes.

| Indicador | Resultado |
| --- | --- |
| Logs processados / lista principal oficial | 2.270 / 2.270 (100%) |
| Municípios abrangidos | 22 |
| Habilitações / votos computados | 453.714 / 453.654 |
| Erros de leitura / categorias indefinidas | 0 / 0 |
| Comparação estatística com pares | 2.200 seções; nenhum alerta pelos critérios aplicados |
| Conferência independente de contagens | 2.231 logs; nenhuma divergência |
| Interrupções pendentes | 7 ciclos em 7 seções |
| Seções com vários blocos no pacote | 39; quatro com duas origens no dia analisado |
| Quarentena / seções admitidas | 10 / 2.260 |
| Alertas técnicos / seções distintas | 53 itens / 45 seções |

O achado de maior prioridade para conferência técnica é Rodrigues Alves, zona 0004, seção 0368: há erro explícito de voto não registrado e desligamentos sucessivos. Sena Madureira, zona 0003, seção 0084, apresenta um ciclo prolongado com confirmação de cargo, tentativas de suspensão e posterior desligamento. Os outros cinco casos não têm justificativa explícita de desligamento no intervalo examinado; em um deles há tecla indevida pouco antes.

Não foram sinalizadas proporções elevadas de eventos de mesário nem volumes elevados de habilitações entre as seções efetivamente comparadas. Isso não comprova regularidade de todos os aspectos da eleição. Os 53 itens são sinais de registro e contexto, não 53 votos suspeitos ou 53 fraudes. Não há acurácia semântica de 99,9% certificada.

Todos os números se referem ao pacote publicado do AC, e não à execução antiga do motor 2.1. As classificações antigas e os alertas nacionais derivados delas permanecem retirados de uso para conclusões até reprocessamento.

## 2. Escopo, fontes e cobertura efetivamente avaliada

Fonte primária: pacote de arquivos do TSE do segundo turno do Acre; fonte operacional desta análise: AC-tentativa1.zip da Release auditoria-v3-41263277696. O ativo publicado foi baixado novamente para este relatório e conferido contra o digest do GitHub, os 129 itens de SHA256SUMS.txt e os sete arquivos do manifesto estadual. O commit registrado no pacote é 83d6bed1523a4ec20d9a55dce4e7aaa49646023d.

A configuração oficial lista 2.270 seções principais e 141 agregadas. A cobertura de 100% compara os logs com as seções principais; não transforma as agregadas em outras 141 urnas independentes nem certifica o conjunto da eleição. Não há seção principal ausente, seção processada fora da configuração ou erro de leitura registrado.

| Camada de avaliação | Seções / logs | Interpretação |
| --- | --- | --- |
| Leitura e contagens do motor | 2.270 | Inventário completo da lista principal |
| Portão de qualidade | 2.260 aceitas; 10 excluídas | Quarentena não é declaração de fraude |
| Critério de tamanho mínimo | 2.215 aceitas com >=100 habilitações | 45 aceitas têm menos de 100 |
| Comparação entre pares | 2.200 em 22 grupos | 15 elegíveis de Assis Brasil não formam grupo mínimo de 20 |
| Conferência por leitor independente | 2.231 | 39 com múltiplos blocos históricos não foram presumidos comparáveis |

As 70 seções fora da comparação com pares se dividem em dez por qualidade, 45 por tamanho inferior a cem habilitações e 15 por grupo comparável menor que vinte seções. Assim, ausência de alerta estatístico não equivale a teste estatístico individual das 2.270 seções.

Datas e horários são reproduzidos como registrados nos equipamentos, sem normalização de fuso ou demonstração de sincronização externa dos relógios. Um horário isolado não foi tratado como prova de abertura antecipada ou votação fora do período permitido.

## 3. Contagens, categorias e balanços

| Classificação do motor | Habilitações | Com voto vinculado | Sem voto vinculado |
| --- | --- | --- | --- |
| Biométrica | 415.724 | 415.675 | 49 |
| Autorização explícita de mesário | 15.686 | 15.680 | 6 |
| Captura de digital de mesário com indicação de nova gravação | 4.076 | 4.076 | 0 |
| Digital de mesário sem associação nominal no log | 2.899 | 2.898 | 1 |
| Ano de nascimento sem evento biométrico reconhecido | 15.329 | 15.325 | 4 |
| Outros tipos | 0 | 0 | 0 |
| Indefinidas | 0 | 0 | 0 |
| TOTAL | 453.714 | 453.654 | 60 |

Neste relatório, votos computados são mensagens de conclusão do ciclo do eleitor. Não são a soma dos votos por cargo, nem uma contagem de votos de candidatos específicos. Confirmações de cargos e conclusão do ciclo são eventos diferentes.

As categorias são mutuamente exclusivas na classificação. A categoria de nova digital conserva o nome técnico do motor; sua evidência é a captura seguida da mensagem de que a digital será salva, não uma verificação pericial da gravação física. A classificação é feita ao fechar o ciclo, aceitando evidência tardia; conflitos e casos não suportados não são presumidos como mesário.

O grupo com eventos de mesário reúne 22.661 habilitações (4,99% do total), das quais 22.654 têm evento de voto vinculado. O grupo ampliado sem evento biométrico reconhecido soma 37.990 (8,37%), já incluindo as 22.661 e acrescentando 15.329 confirmações de ano de nascimento. Esses dois totais não devem ser somados. O grupo ampliado não informa se havia biometria cadastrada nem equivale ao indicador de biometria não reconhecida do BU.

Balanço das habilitações: 453.714 = 453.654 com voto computado + 53 suspensões explícitas sem voto + 0 cancelamentos explícitos nessa categoria de desfecho + 7 ciclos interrompidos pendentes. O resíduo é zero. Balanço dos votos computados: 453.654 = 453.654 vinculados + 0 sem habilitação associada. O resíduo também é zero.

Há 51 mensagens de suspensão parcial, contabilizadas separadamente; não são outros 51 votos a acrescentar ao total. Há 3.065 eventos de cancelamento antes da habilitação; representam etapas de tentativa, não 3.065 votos computados ou necessariamente 3.065 pessoas diferentes. Cancelamento antes da habilitação e suspensão de eleitor já habilitado são situações distintas.

## 4. Resumo integral dos 22 municípios

| Município | Logs | Habilit. | Votos | Mesário | % mes. | Susp. | Pend. | Quar. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ACRELÂNDIA | 45 | 7.713 | 7.713 | 560 | 7,26% | 0 | 0 | 0 |
| ASSIS BRASIL | 28 | 5.460 | 5.460 | 397 | 7,27% | 0 | 0 | 0 |
| BRASILÉIA | 74 | 15.017 | 15.016 | 694 | 4,62% | 1 | 0 | 0 |
| BUJARI | 41 | 7.915 | 7.914 | 398 | 5,03% | 1 | 0 | 1 |
| CAPIXABA | 34 | 5.785 | 5.785 | 323 | 5,58% | 0 | 0 | 0 |
| CRUZEIRO DO SUL | 256 | 47.291 | 47.282 | 2.906 | 6,14% | 8 | 1 | 2 |
| EPITACIOLÂNDIA | 54 | 10.969 | 10.968 | 530 | 4,83% | 1 | 0 | 0 |
| FEIJÓ | 88 | 16.193 | 16.190 | 873 | 5,39% | 3 | 0 | 0 |
| JORDÃO | 24 | 3.925 | 3.925 | 392 | 9,99% | 0 | 0 | 0 |
| MANOEL URBANO | 31 | 6.134 | 6.133 | 383 | 6,24% | 1 | 0 | 0 |
| MARECHAL THAUMATURGO | 47 | 7.051 | 7.051 | 254 | 3,60% | 0 | 0 | 0 |
| MÂNCIO LIMA | 57 | 10.733 | 10.732 | 797 | 7,43% | 1 | 0 | 0 |
| PLÁCIDO DE CASTRO | 54 | 8.945 | 8.945 | 453 | 5,06% | 0 | 0 | 0 |
| PORTO ACRE | 60 | 10.796 | 10.790 | 533 | 4,94% | 5 | 1 | 1 |
| PORTO WALTER | 34 | 4.792 | 4.792 | 431 | 8,99% | 0 | 0 | 0 |
| RIO BRANCO | 908 | 209.666 | 209.645 | 8.835 | 4,21% | 19 | 2 | 2 |
| RODRIGUES ALVES | 55 | 8.742 | 8.741 | 481 | 5,50% | 0 | 1 | 1 |
| SANTA ROSA DO PURUS | 16 | 2.822 | 2.820 | 128 | 4,54% | 2 | 0 | 0 |
| SENA MADUREIRA | 120 | 20.895 | 20.888 | 1.020 | 4,88% | 5 | 2 | 2 |
| SENADOR GUIOMARD | 81 | 14.051 | 14.049 | 634 | 4,51% | 2 | 0 | 1 |
| TARAUACÁ | 110 | 19.115 | 19.112 | 1.195 | 6,25% | 3 | 0 | 0 |
| XAPURI | 53 | 9.704 | 9.703 | 444 | 4,58% | 1 | 0 | 0 |

Mesário: habilitações com eventos do grupo de mesário, não acusação de intervenção irregular. Susp.: suspensões explícitas sem voto. Pend.: ciclos sem desfecho de voto explicado pelo motor. Quar.: seções fora da comparação estatística. Percentuais usam todas as habilitações do município, inclusive as de seções em quarentena; são descritivos, não testes estatísticos municipais.

## 5. As sete interrupções: visão geral

| Município | Zona / seção | Habilitação | Desliga | Intervalo |
| --- | --- | --- | --- | --- |
| PORTO ACRE | 0001 / 0608 | 10:54:13 | 10:54:30 | 17 s |
| CRUZEIRO DO SUL | 0004 / 0482 | 08:25:35 | 08:25:52 | 17 s |
| RODRIGUES ALVES | 0004 / 0368 | 09:31:44 | 09:35:06 | 202 s |
| RIO BRANCO | 0001 / 0554 | 12:28:05 | 12:28:19 | 14 s |
| RIO BRANCO | 0009 / 0053 | 14:30:19 | 14:30:25 | 6 s |
| SENA MADUREIRA | 0003 / 0001 | 08:55:20 | 08:55:44 | 24 s |
| SENA MADUREIRA | 0003 / 0084 | 09:39:13 | 10:10:29 | 1876 s |

Todos os sete avisos estaduais são do tipo ciclo_interrompida. Isso significa que um ciclo aberto foi interrompido antes de uma mensagem de voto computado associada, não que os votos anteriores da seção foram perdidos. A causa operacional da interrupção e o desfecho do atendimento ao eleitor são questões diferentes: é possível conhecer o desligamento sem saber se o eleitor foi atendido novamente.

A mensagem de desligamento pela chave não identifica a pessoa que acionou o mecanismo. O relatório não atribui autoria nem intenção. Nas seis primeiras ocorrências abaixo, o horário de retomada indica a volta à espera por identificação, não o retorno comprovado do mesmo eleitor.

Prioridade de esclarecimento: (a) Rodrigues Alves 0368, pela falha explícita e reinícios sucessivos; (b) Sena Madureira 0084, pela interação prolongada, confirmação parcial e mudança de identificador de equipamento; (c) os outros cinco, pela necessidade de justificativa e acompanhamento do atendimento na ata. É prioridade documental, não escala de fraude.

## 6.1. Evidências das interrupções

PORTO ACRE - zona 0001, seção 0608

Habilitação 10:54:13; desligamento 10:54:30; intervalo 17 segundos. Desligamento após habilitação biométrica, sem justificativa explícita no intervalo.

A última habilitação ocorre às 10:54:13; o desligamento aparece 17 segundos depois. Não há evento de voto computado entre esses registros.

Após a intervenção, retorno observado à espera por identificação: 10:58:25. Verificar a ata e o atendimento dado ao eleitor após o reinício. O retorno à espera por identificação não identifica quem voltou a votar.

Referência: o03221ac0102300010608-log.jez; origem raiz!logd.dat; habilitação na linha 7597 e desligamento na linha 7598.

CRUZEIRO DO SUL - zona 0004, seção 0482

Habilitação 08:25:35; desligamento 08:25:52; intervalo 17 segundos. Desligamento após habilitação biométrica, sem justificativa explícita no intervalo.

O eleitor foi habilitado às 08:25:35 e o desligamento ocorre 17 segundos depois. O trecho não informa a decisão que motivou o acionamento da chave.

Após a intervenção, retorno observado à espera por identificação: 08:31:02. Confrontar a ocorrência com a ata e os registros de atendimento técnico, sem atribuir intenção a partir do desligamento.

Referência: o03221ac0107400040482-log.jez; origem raiz!logd.dat; habilitação na linha 6778 e desligamento na linha 6779.

RODRIGUES ALVES - zona 0004, seção 0368

Habilitação 09:31:44; desligamento 09:35:06; intervalo 202 segundos. Erro explícito informando que o voto não foi registrado, seguido de desligamentos.

Às 09:34:45, há erro 5362 com orientação para desligar e ligar a urna; às 09:34:46 aparece ERROR -44. Após o primeiro desligamento, o histórico registra outros às 09:42:14, 09:50:33 e 10:02:43.

Após a intervenção, retorno observado à espera por identificação: 10:11:42. Priorizar a conferência do atendimento ao eleitor e da intervenção técnica. O erro informa falha de registro daquele ciclo; não comprova perda dos votos anteriores.

Referência: o03221ac0108200040368-log.jez; origem raiz!logd.dat; habilitação na linha 5261 e desligamento na linha 5264.

## 6.2. Evidências das interrupções

RIO BRANCO - zona 0001, seção 0554

Habilitação 12:28:05; desligamento 12:28:19; intervalo 14 segundos. Tecla indevida registrada antes do desligamento; causa do acionamento não explicitada.

A habilitação ocorre às 12:28:05, há tecla indevida às 12:28:17 e desligamento às 12:28:19. A proximidade temporal não demonstra que a tecla causou ou justificou a decisão.

Após a intervenção, retorno observado à espera por identificação: 12:32:50. Verificar o relato na ata; não converter sequência temporal em causa comprovada.

Referência: o03221ac0139200010554-log.jez; origem raiz!logd.dat; habilitação na linha 9282 e desligamento na linha 9284.

RIO BRANCO - zona 0009, seção 0053

Habilitação 14:30:19; desligamento 14:30:25; intervalo 6 segundos. Desligamento seis segundos após habilitação biométrica, sem justificativa explícita no intervalo.

A habilitação ocorre às 14:30:19 e a chave é desligada às 14:30:25, sem mensagem de voto computado entre os dois eventos.

Após a intervenção, retorno observado à espera por identificação: 14:35:48. Conferir motivo e destino do atendimento ao eleitor. A duração curta não comprova que houve voto registrado ou intenção irregular.

Referência: o03221ac0139200090053-log.jez; origem raiz!logd.dat; habilitação na linha 9507 e desligamento na linha 9508.

## 6.3. Evidências das interrupções

SENA MADUREIRA - zona 0003, seção 0001

Habilitação 08:55:20; desligamento 08:55:44; intervalo 24 segundos. Desligamento 24 segundos após habilitação biométrica, sem justificativa explícita no intervalo.

O eleitor é habilitado às 08:55:20 e o desligamento é registrado às 08:55:44, sem voto computado associado antes da interrupção.

Após a intervenção, retorno observado à espera por identificação: 09:00:58. Confrontar ata, atendimento técnico e retomada do atendimento, preservando o sigilo do voto.

Referência: o03221ac0145700030001-log.jez; origem raiz!logd.dat; habilitação na linha 7274 e desligamento na linha 7275.

SENA MADUREIRA - zona 0003, seção 0084

Habilitação 09:39:13; desligamento 10:10:29; intervalo 1876 segundos. Interação prolongada, confirmação de um cargo e tentativas de suspensão antes do desligamento.

A habilitação ocorre às 09:39:13; há confirmação de Governador às 09:39:22, teclas indevidas e períodos sem atividade. O log registra retorno à digitação durante tentativas de suspensão às 09:42:26, 09:49:41 e 10:07:51. O desligamento ocorre 31 minutos e 16 segundos após a habilitação.

Após a intervenção, retorno observado à espera por identificação: Não fixado neste relatório. Verificar ata, contingência e reconciliação com BU/RDV. Confirmar um cargo não foi tratado como prova de voto computado do ciclo. A continuidade entre equipamentos não é presumida pelo analisador.

Referência: o03221ac0145700030084-log.jez; origem raiz!0204652225102026101640-01.jez!logd.dat; habilitação na linha 6719 e desligamento na linha 6755.

## 7. Relação integral das 39 seções com múltiplos blocos

O pacote contém 2.231 logs com um bloco, 36 com dois e três com três. Ter vários blocos não demonstra voto duplicado ou troca de equipamento durante a votação. Em 35 das 39 seções, somente uma origem tem registros do dia analisado; em quatro, há duas. Não foram removidas linhas por deduplicação neste estado.

| Município | Zona | Seção | Blocos no pacote | Origens no dia | Quarentena |
| --- | --- | --- | --- | --- | --- |
| BUJARI | 0009 | 0002 | 2 | 2 | Sim |
| BUJARI | 0009 | 0437 | 2 | 1 | Não |
| BUJARI | 0009 | 0476 | 3 | 1 | Não |
| CAPIXABA | 0002 | 0079 | 2 | 1 | Não |
| CAPIXABA | 0002 | 0093 | 2 | 1 | Não |
| PORTO ACRE | 0001 | 0797 | 2 | 1 | Não |
| BRASILÉIA | 0006 | 0033 | 2 | 1 | Não |
| BRASILÉIA | 0006 | 0099 | 2 | 1 | Não |
| CRUZEIRO DO SUL | 0004 | 0198 | 2 | 1 | Não |
| CRUZEIRO DO SUL | 0004 | 0308 | 2 | 1 | Não |
| CRUZEIRO DO SUL | 0004 | 0394 | 2 | 2 | Sim |
| RODRIGUES ALVES | 0004 | 0148 | 2 | 1 | Não |
| RODRIGUES ALVES | 0004 | 0349 | 2 | 1 | Não |
| MÂNCIO LIMA | 0004 | 0090 | 2 | 1 | Não |
| MÂNCIO LIMA | 0004 | 0346 | 3 | 1 | Não |
| JORDÃO | 0005 | 0125 | 2 | 1 | Não |
| ACRELÂNDIA | 0008 | 0072 | 2 | 1 | Não |
| ACRELÂNDIA | 0008 | 0205 | 2 | 1 | Não |
| FEIJÓ | 0007 | 0004 | 2 | 1 | Não |
| FEIJÓ | 0007 | 0075 | 2 | 1 | Não |
| RIO BRANCO | 0001 | 0097 | 2 | 1 | Não |
| RIO BRANCO | 0001 | 0441 | 2 | 1 | Não |
| RIO BRANCO | 0001 | 0500 | 2 | 1 | Não |
| RIO BRANCO | 0001 | 0551 | 2 | 1 | Não |
| RIO BRANCO | 0001 | 0685 | 2 | 1 | Não |
| RIO BRANCO | 0001 | 0770 | 2 | 1 | Não |
| RIO BRANCO | 0001 | 0852 | 2 | 1 | Não |
| RIO BRANCO | 0001 | 0863 | 2 | 1 | Não |
| RIO BRANCO | 0009 | 0082 | 2 | 1 | Não |
| RIO BRANCO | 0009 | 0104 | 2 | 1 | Não |
| RIO BRANCO | 0009 | 0308 | 2 | 1 | Não |
| RIO BRANCO | 0009 | 0403 | 2 | 1 | Não |
| SENA MADUREIRA | 0003 | 0002 | 2 | 1 | Não |
| SENA MADUREIRA | 0003 | 0008 | 2 | 1 | Não |
| SENA MADUREIRA | 0003 | 0084 | 2 | 2 | Sim |
| TARAUACÁ | 0005 | 0010 | 2 | 1 | Não |
| TARAUACÁ | 0005 | 0015 | 2 | 1 | Não |
| SENADOR GUIOMARD | 0008 | 0082 | 3 | 2 | Sim |
| MANOEL URBANO | 0003 | 0126 | 2 | 1 | Não |

## 8. Quatro seções com duas origens no dia da votação

A leitura dos originais preservados mostra dois identificadores de equipamento diferentes em cada uma dessas quatro seções. A tabela reproduz registros do dia e contagens literais por bloco. Não pressupõe que o intervalo entre blocos seja a duração exata de uma paralisação.

| Município / seção | ID equipamento | Primeiro / último registro | Habilit. | Votos |
| --- | --- | --- | --- | --- |
| BUJARI / 0002 | 02257895 | 03:53:51 / 04:31:55 | 0 | 0 |
| BUJARI / 0002 | 02047711 | 04:39:55 / 15:06:10 | 232 | 232 |
| CRUZEIRO DO SUL / 0394 | 02278553 | 05:19:50 / 13:27:43 | 208 | 207 |
| CRUZEIRO DO SUL / 0394 | 02276040 | 13:33:01 / 15:04:04 | 23 | 23 |
| SENA MADUREIRA / 0084 | 02046886 | 05:56:00 / 10:10:38 | 82 | 81 |
| SENA MADUREIRA / 0084 | 02046522 | 10:15:10 / 15:04:32 | 99 | 99 |
| SENADOR GUIOMARD / 0082 | 02019031 | 05:30:34 / 08:43:59 | 67 | 67 |
| SENADOR GUIOMARD / 0082 | 02044974 | 08:48:52 / 15:06:46 | 137 | 137 |

Bujari 0002: o primeiro identificador não tem habilitações nem votos computados; a mudança aparece em registros anteriores ao atendimento de eleitores. Não há base para qualificá-la como substituição durante um voto. Cruzeiro do Sul 0394, Sena Madureira 0084 e Senador Guiomard 0082 têm votos computados nos dois blocos. A ata e os registros de contingência devem explicar as transições.

Em Cruzeiro do Sul 0394, o primeiro bloco tem 208 habilitações e 207 votos computados; essa diferença não gerou ciclo pendente e integra o balanço de suspensões explícitas. Em Sena Madureira 0084, a diferença de uma habilitação no primeiro bloco corresponde ao ciclo interrompido já descrito. Não se presume que uma habilitação do bloco novo seja a continuação do mesmo eleitor.

A existência dos blocos não prova, por si só, que a transferência de votos foi correta ou incorreta. É necessário reconciliar registros de contingência, BU, RDV, configurações e ata. Esta versão não realizou essa reconciliação de conteúdo dos votos.

## 9. As dez seções em quarentena

| Município | Zona / seção | Motivo de exclusão |
| --- | --- | --- |
| BUJARI | 0009 / 0002 | Duas origens no dia |
| PORTO ACRE | 0001 / 0608 | Um ciclo interrompido |
| CRUZEIRO DO SUL | 0004 / 0394 | Duas origens no dia |
| CRUZEIRO DO SUL | 0004 / 0482 | Um ciclo interrompido |
| RODRIGUES ALVES | 0004 / 0368 | Um ciclo interrompido |
| RIO BRANCO | 0001 / 0554 | Um ciclo interrompido |
| RIO BRANCO | 0009 / 0053 | Um ciclo interrompido |
| SENA MADUREIRA | 0003 / 0001 | Um ciclo interrompido |
| SENA MADUREIRA | 0003 / 0084 | Um ciclo interrompido; Duas origens no dia |
| SENADOR GUIOMARD | 0008 / 0082 | Duas origens no dia |

Sete seções têm ciclo interrompido; quatro têm duas origens no dia. Sena Madureira 0084 pertence aos dois grupos. Assim, 7 + 4 - 1 = 10 seções distintas, e não onze. Quarentena é uma barreira de avaliação do programa; não significa voto anulado, seção não apurada ou fraude.

Os 53 itens de alerta se decompõem em 39 registros de múltiplos blocos, sete avisos e sete itens de ciclo pendente. Os últimos dois conjuntos se referem aos mesmos sete casos. Como uma dessas seções também tem múltiplos blocos, são 45 seções distintas com algum item de contexto ou alerta técnico.

O relatório preserva os casos excluídos em vez de transformá-los em zero ou eliminá-los da documentação. O ZIP publicado contém os originais das seções em quarentena e controles determinísticos, acompanhados de hashes. Os identificadores pessoais eventualmente presentes em mensagens não são reproduzidos neste relatório.

## 10. Critérios estatísticos, séries e ausência de alertas

A comparação usa seções do mesmo município e zona: mínimo de vinte seções aceitas, cada uma com pelo menos cem habilitações. O limite exploratório é Q3 + 3 vezes o intervalo interquartil. Exige-se também diferença superior a dez pontos percentuais da mediana para proporção de mesário ou a cinquenta habilitações para volume. A própria seção participa da referência. Não é p-valor, probabilidade de fraude ou ajuste por biometria cadastrada e eleitores aptos.

| Grupo | Séries >=2 | >=3 | >=5 | >=10 | >=20 |
| --- | --- | --- | --- | --- | --- |
| Eventos de mesário | 1.316 | 104 | 2 | 0 | 0 |
| Grupo ampliado | 3.580 | 558 | 31 | 1 | 0 |

São séries máximas de habilitações; uma série de dez aparece nas faixas de dois, três, cinco e dez. As colunas não podem ser somadas. A maior série de mesário tem seis habilitações, abaixo do limiar fixo de dez da triagem. A maior do grupo ampliado tem dez; esse grupo também inclui confirmação de ano de nascimento, e não apenas intervenção de mesário.

| Grupo / município | Zona / seção | Série | Início / fim |
| --- | --- | --- | --- |
| Mesário / JORDÃO | 0005 / 0122 | 6 | 07:04:52 / 07:19:02 |
| Mesário / PLÁCIDO DE CASTRO | 0008 / 0024 | 5 | 09:12:46 / 09:28:31 |
| Ampliado / ASSIS BRASIL | 0006 / 0150 | 10 | 11:28:55 / 11:49:58 |

Essas maiores séries são referências descritivas, não novas suspeitas. Não houve alerta de proporção elevada nem de volume elevado entre as 2.200 seções comparadas. O detector de intervalo médio inferior a trinta segundos só examina séries de mesário com dez ou mais habilitações; como nenhuma atingiu esse tamanho, ele não fornece uma avaliação global da velocidade de votação no Acre. Também não houve análise de votação por candidato.

## 11. Referências completas da comparação com pares

As proporções abaixo são expressas em porcentagem; os limites de volume estão em habilitações. Cada linha resume um grupo município/zona. O limiar adicional de diferença da mediana, descrito na seção anterior, também precisa ser satisfeito para gerar alerta.

| Município / zona | N | Mediana mes. | Limite mes. | Mediana vol. | Limite vol. |
| --- | --- | --- | --- | --- | --- |
| ACRELÂNDIA / 0008 | 44 | 6,48% | 26,23% | 172,0 | 310,0 |
| ASSIS BRASIL / 0006 | 26 | 5,48% | 29,62% | 205,0 | 312,2 |
| BRASILÉIA / 0006 | 74 | 4,27% | 13,83% | 207,0 | 349,0 |
| BUJARI / 0009 | 40 | 4,82% | 15,00% | 199,0 | 463,0 |
| CAPIXABA / 0002 | 33 | 5,66% | 16,58% | 175,0 | 301,0 |
| CRUZEIRO DO SUL / 0004 | 242 | 5,79% | 17,40% | 195,0 | 326,0 |
| EPITACIOLÂNDIA / 0006 | 54 | 4,54% | 15,34% | 212,0 | 313,2 |
| FEIJÓ / 0007 | 86 | 5,30% | 17,03% | 188,0 | 395,2 |
| JORDÃO / 0005 | 23 | 9,77% | 41,09% | 165,0 | 309,0 |
| MANOEL URBANO / 0003 | 30 | 6,05% | 23,67% | 204,5 | 315,8 |
| MARECHAL THAUMATURGO / 0004 | 46 | 2,60% | 16,07% | 149,5 | 270,5 |
| MÂNCIO LIMA / 0004 | 55 | 6,77% | 27,12% | 199,0 | 310,0 |
| PLÁCIDO DE CASTRO / 0008 | 50 | 4,49% | 14,43% | 172,5 | 280,5 |
| PORTO ACRE / 0001 | 59 | 4,89% | 17,93% | 183,0 | 291,5 |
| PORTO WALTER / 0004 | 28 | 8,12% | 26,07% | 153,5 | 286,0 |
| RIO BRANCO / 0001 | 474 | 4,26% | 15,49% | 229,0 | 432,0 |
| RIO BRANCO / 0009 | 432 | 3,65% | 12,45% | 249,0 | 388,0 |
| RODRIGUES ALVES / 0004 | 52 | 5,08% | 15,23% | 160,0 | 286,8 |
| SENA MADUREIRA / 0003 | 115 | 4,61% | 17,03% | 177,0 | 287,0 |
| SENADOR GUIOMARD / 0008 | 79 | 4,26% | 14,25% | 171,0 | 345,5 |
| TARAUACÁ / 0005 | 106 | 5,90% | 16,16% | 183,0 | 322,0 |
| XAPURI / 0002 | 52 | 4,17% | 14,01% | 188,5 | 280,2 |

Assis Brasil tem quinze seções elegíveis e não atinge o mínimo de vinte, portanto não entra nessa comparação. Os CSVs anexos preservam as referências com precisão completa; valores da tabela foram arredondados apenas para leitura.

## 12. Conclusões e verificações pendentes

- A cobertura de leitura da lista principal está completa e não há divergência nas contagens literais dos 2.231 logs comparáveis pelo leitor independente. Isso não certifica a classificação semântica ou a autenticidade criptográfica dos dados.

- Não foram encontrados alertas pelos critérios de proporção elevada de eventos de mesário ou volume elevado nas 2.200 seções comparadas. Ausência de alerta nesses critérios não certifica todos os aspectos das seções.

- Sete ciclos foram interrompidos e dez seções ficaram fora da comparação. Os eventos não foram convertidos em votos extras, votos anulados ou fraudes presumidas. O motivo do acionamento da chave e a identidade de quem o acionou não são demonstrados pela mensagem de desligamento.

- Os votos dos eleitores anteriores não podem ser considerados perdidos apenas por haver desligamento. Por outro lado, este relatório não verificou a persistência nem a transferência de cada voto com BU/RDV e documentos de contingência. A igualdade de contagens de log não substitui essa verificação.

- Próximo passo documental: obter atas das sete seções com ciclos interrompidos e das quatro com transição de identificador; conferir motivo, equipe responsável, horários, equipamentos e atendimento ao eleitor afetado. Sena Madureira 0084 consta nos dois conjuntos.

- Próximo passo técnico: reconciliar BU/RDV, relatórios de contingência e dados transmitidos, mantendo a distinção entre voto por cargo, ciclo do eleitor e mensagem de voto computado. Uma mensagem de confirmação de Governador, isoladamente, não resolve essa reconciliação.

- Não é possível identificar o retorno do mesmo eleitor por mera sequência de horários, nem revelar suas escolhas. Não há base de referência independente suficiente para certificar acurácia de 99,9%. A análise não verifica hardware, software instalado, assinaturas criptográficas ou presença física dos votantes.

Conclusão do escopo: há leitura integral da lista principal, balanços internos fechados e pontos técnicos localizados para esclarecimento. Não há neste material demonstração de fraude, nem demonstração pericial de regularidade integral da eleição do Acre.

## 13. Proveniência, reprodução e anexos

| Objeto | Identificador |
| --- | --- |
| Motor e executor - SHA-256 | 7c0a3a5dd412d61bedf77aba11c9e4df4a8574b52718e502e9a5d45c7d5a70cb |
| Commit congelado da execução | 83d6bed1523a4ec20d9a55dce4e7aaa49646023d |
| Pacote oficial TSE - SHA-256 | 7e58076367c9a0d8002b7918fe33183a2aee8aaf562d32555cf62ce10d188dc5 |
| Pacote AC publicado - SHA-256 | e72a82e0720f62bfc7a682946f4cda37fcbeb94aa22bf94e06d6fb7ed5ab1d95 |
| Contagem independente - SHA-256 | 7726d5f166909f02dcc928d07343596d59673967536452c375996d9fef540343 |

Pacote publicado: AC-tentativa1.zip; ativo GitHub 697053160; atualização informada pela fonte: 01/11/2026 02:02:54 UTC, correspondente a 31/10/2026 23:02:54 em Brasília. Todas as contagens do relatório são dessa versão fixada. A verificação de SHA-256 demonstra identidade dos bytes conferidos, não autentica uma assinatura do TSE.

Arquivos do pacote utilizados: resultados/AC/resumo.json, urnas.csv, sequencias.csv, avisos.csv, config_oficial.json e manifesto.json; triagem/resumo.json, alertas.csv, quarentena.csv e referencias_comparacao.csv; conferencias/AC/conferencia.json e execucao.json; originais/AC/*.jez e manifesto_amostras.json. O arquivo urnas.csv contém todas as 2.270 seções. O pacote inclui também a referência de contagem independente e os checksums.

Reprodução: obter o commit congelado; executar o motor para AC e a conferência de contagens com o pacote oficial; verificar o manifesto; executar anomalias.py. O script executar_estado.py automatiza essas etapas. Para uma reprodução exata de bytes, preservar o pacote publicado, pois duração e horário de execução mudam em uma nova rodada.

F1 - Pacote publicado e dados completos: https://github.com/hugohalima-hash/auditoria_eleicoes_2026/releases/download/auditoria-v3-41263277696/AC-tentativa1.zip

F2 - Execução persistente: https://github.com/hugohalima-hash/auditoria_eleicoes_2026/actions/runs/41263277696

F3 - Configuração oficial das seções: https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3221/config/ac/ac-p003221-cs.json

F4 - Pacote bruto oficial do TSE: https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2026/arqurnatot/bu_imgbu_logjez_rdv_vscmr_2026_2t_AC.zip

F5 - Regras de contingência e recuperação de 2026: https://www.tse.jus.br/legislacao/compilada/res/2026/resolucao-no-23-751-de-26-de-fevereiro-de-2026

Anexos estruturados deste relatório: 01_interrupcoes.csv (sete casos e linhas); 02_quarentena.csv (dez seções); 03_multiplos_blocos.csv (39 seções); 04_blocos_do_dia.csv (oito blocos das quatro seções); 05_resumo_municipal.csv (22 municípios); 06_alertas_integrais.csv (53 itens); 07_referencias_comparacao.csv (44 referências para 22 grupos). Eles não substituem os dados completos do pacote F1.
