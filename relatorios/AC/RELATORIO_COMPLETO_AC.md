# Acre - habilitação por mesário e ano de nascimento

> Relatório de auditoria dos registros de votação. Segundo turno de 25/10/2026. Versão revisada de 01/11/2026.

## 1. Resultado principal

Auditoria dos registros de votação do Acre - segundo turno de 25 de outubro de 2026. Relatório emitido em 1º de novembro de 2026.

Objetivo: dimensionar as votações liberadas por mesário ou com confirmação do ano de nascimento e identificar concentrações e padrões de tempo que justifiquem conferência. A hipótese examinada é o uso indevido desses procedimentos para votar em nome de eleitores que não compareceram.

| Indicador | Resultado |
| --- | --- |
| Votações concluídas no estado | 453.654 |
| Com registros de liberação por mesário | 22.654 (4,99%) |
| Com confirmação do ano de nascimento | 15.325 (3,38%) |
| Total dos dois procedimentos | 37.979 (8,37%) |
| Seções com proporção elevada do conjunto | 41, contendo 2.458 dessas votações |
| Votações do conjunto concluídas em até 10 segundos | 1.620 |
| Dessas, após espera de pelo menos 5 minutos por identificação | 114, distribuídas em 106 seções |

As 37.979 votações constituem o universo de verificação, incluindo ocorrências isoladas e distribuídas ao longo do dia. A seleção não depende de haver uma sequência de liberações. Os dois procedimentos também integram o atendimento regular ao eleitor; sua ocorrência, sozinha, não permite classificar uma votação como fraudulenta.

O principal achado para conferência documental é a concentração dos dois procedimentos em 41 seções. A maior proporção observada nesse grupo foi de 49,51%, em Assis Brasil, zona 0006, seção 0150: 101 de 204 votações concluídas.

Quanto ao ritmo, houve registros curtos e ocorrências após períodos de espera. Entretanto, a duração de até dez segundos também aparece em votações identificadas por biometria. Nas maiores sequências do conjunto, os intervalos médios entre liberações foram superiores a um minuto.

Os logs registram operações, mas não comprovam a presença física de cada eleitor. A apuração de eventual voto em nome de ausente exige confrontar os casos selecionados com os registros de comparecimento, os documentos da seção e as ocorrências técnicas.

## 2. O que está sendo contado

Uma votação concluída é identificada pela mensagem de voto computado após a liberação do eleitor. Trata-se da conclusão do atendimento daquele eleitor, não da soma de votos por cargo. Uma liberação que terminou em suspensão ou interrupção não foi contada como voto concluído.

| Procedimento registrado | Votações concluídas | % do estado |
| --- | --- | --- |
| Autorização explícita de mesário | 15.680 | 3,46% |
| Digital de mesário com indicação de nova gravação | 4.076 | 0,90% |
| Digital de mesário sem associação nominal no log | 2.898 | 0,64% |
| Subtotal com registros de mesário | 22.654 | 4,99% |
| Confirmação do ano de nascimento | 15.325 | 3,38% |
| Total em análise | 37.979 | 8,37% |
| Identificação biométrica | 415.675 | 91,63% |

A confirmação de ano de nascimento foi identificada sem mensagem biométrica reconhecida naquela tentativa. O dado não informa, por si só, se o eleitor tinha biometria cadastrada. Os dois grupos são separados na classificação e podem ser somados sem duplicar votações.

Foram registradas 37.990 liberações com os dois procedimentos, mas onze não terminaram em mensagem de voto computado. Por isso, o total de votos em análise é 37.979, e não 37.990.

Seções com maior quantidade absoluta de votações do conjunto:

| Município | Zona / seção | Mesário | Ano | Total | % da seção |
| --- | --- | --- | --- | --- | --- |
| ASSIS BRASIL | 0006 / 0150 | 22 | 79 | 101 | 49,51% |
| RIO BRANCO | 0009 / 0453 | 5 | 92 | 97 | 35,79% |
| RIO BRANCO | 0001 / 0824 | 4 | 92 | 96 | 38,55% |
| BUJARI | 0009 / 0441 | 15 | 76 | 91 | 36,84% |
| RIO BRANCO | 0001 / 0820 | 5 | 85 | 90 | 35,16% |
| RIO BRANCO | 0009 / 0449 | 9 | 74 | 83 | 32,3% |
| EPITACIOLÂNDIA | 0006 / 0151 | 4 | 73 | 77 | 38,31% |
| RIO BRANCO | 0001 / 0821 | 5 | 67 | 72 | 28,69% |
| TARAUACÁ | 0005 / 0134 | 33 | 38 | 71 | 33,02% |
| RIO BRANCO | 0001 / 0826 | 11 | 59 | 70 | 30,04% |

## 3. Totais dos 22 municípios

| Município | Votações concluídas | Mesário | Ano de nascimento | Conjunto | % |
| --- | --- | --- | --- | --- | --- |
| ACRELÂNDIA | 7.713 | 560 | 148 | 708 | 9,18% |
| ASSIS BRASIL | 5.460 | 397 | 273 | 670 | 12,27% |
| BRASILÉIA | 15.016 | 694 | 661 | 1.355 | 9,02% |
| BUJARI | 7.914 | 398 | 286 | 684 | 8,64% |
| CAPIXABA | 5.785 | 323 | 230 | 553 | 9,56% |
| CRUZEIRO DO SUL | 47.282 | 2.905 | 1.355 | 4.260 | 9,01% |
| EPITACIOLÂNDIA | 10.968 | 530 | 438 | 968 | 8,83% |
| FEIJÓ | 16.190 | 873 | 837 | 1.710 | 10,56% |
| JORDÃO | 3.925 | 392 | 76 | 468 | 11,92% |
| MANOEL URBANO | 6.133 | 383 | 269 | 652 | 10,63% |
| MARECHAL THAUMATURGO | 7.051 | 254 | 453 | 707 | 10,03% |
| MÂNCIO LIMA | 10.732 | 796 | 489 | 1.285 | 11,97% |
| PLÁCIDO DE CASTRO | 8.945 | 453 | 332 | 785 | 8,78% |
| PORTO ACRE | 10.790 | 531 | 408 | 939 | 8,70% |
| PORTO WALTER | 4.792 | 431 | 266 | 697 | 14,55% |
| RIO BRANCO | 209.645 | 8.833 | 5.708 | 14.541 | 6,94% |
| RODRIGUES ALVES | 8.741 | 481 | 340 | 821 | 9,39% |
| SANTA ROSA DO PURUS | 2.820 | 127 | 71 | 198 | 7,02% |
| SENA MADUREIRA | 20.888 | 1.020 | 978 | 1.998 | 9,57% |
| SENADOR GUIOMARD | 14.049 | 634 | 436 | 1.070 | 7,62% |
| TARAUACÁ | 19.112 | 1.195 | 946 | 2.141 | 11,20% |
| XAPURI | 9.703 | 444 | 325 | 769 | 7,93% |

Os totais municipais incluem as ocorrências de todas as seções, inclusive as separadas da comparação estatística por problemas de continuidade dos registros. São quantidades observadas, não estimativas de fraude.

O anexo 08 apresenta os números de cada uma das 2.270 seções. O anexo 09 contém as 37.979 votações do conjunto, com horários, procedimento de liberação e referências ao log de origem.

## 4. Seções com proporção elevada

Foram comparadas 2.200 seções com pelo menos cem votações concluídas e registros adequados à comparação. Cada seção foi confrontada com as do mesmo município e zona. As 41 seções abaixo ultrapassaram a referência local para a soma dos dois procedimentos. Elas reúnem 2.458 votações do conjunto, dentro de 8.702 votações concluídas nessas seções.

| Município | Zona | Seção | Votações | Mesário | Ano | Conjunto | % |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ASSIS BRASIL | 0006 | 0150 | 204 | 22 | 79 | 101 | 49,51% |
| PORTO WALTER | 0004 | 0447 | 117 | 2 | 46 | 48 | 41,03% |
| RIO BRANCO | 0001 | 0824 | 249 | 4 | 92 | 96 | 38,55% |
| EPITACIOLÂNDIA | 0006 | 0151 | 201 | 4 | 73 | 77 | 38,31% |
| BUJARI | 0009 | 0441 | 247 | 15 | 76 | 91 | 36,84% |
| RIO BRANCO | 0009 | 0453 | 271 | 5 | 92 | 97 | 35,79% |
| RIO BRANCO | 0001 | 0820 | 256 | 5 | 85 | 90 | 35,16% |
| SENADOR GUIOMARD | 0008 | 0268 | 168 | 11 | 46 | 57 | 33,93% |
| TARAUACÁ | 0005 | 0133 | 146 | 13 | 36 | 49 | 33,56% |
| TARAUACÁ | 0005 | 0134 | 215 | 33 | 38 | 71 | 33,02% |
| RIO BRANCO | 0009 | 0449 | 257 | 9 | 74 | 83 | 32,3% |
| TARAUACÁ | 0005 | 0130 | 205 | 12 | 53 | 65 | 31,71% |
| MANOEL URBANO | 0003 | 0154 | 182 | 16 | 41 | 57 | 31,32% |
| RIO BRANCO | 0001 | 0826 | 233 | 11 | 59 | 70 | 30,04% |
| SENA MADUREIRA | 0003 | 0155 | 167 | 16 | 33 | 49 | 29,34% |
| RIO BRANCO | 0001 | 0821 | 251 | 5 | 67 | 72 | 28,69% |
| RIO BRANCO | 0001 | 0829 | 200 | 6 | 51 | 57 | 28,5% |
| BRASILÉIA | 0006 | 0152 | 224 | 9 | 54 | 63 | 28,12% |
| RIO BRANCO | 0001 | 0822 | 226 | 4 | 59 | 63 | 27,88% |
| RODRIGUES ALVES | 0004 | 0455 | 212 | 27 | 32 | 59 | 27,83% |
| PORTO ACRE | 0001 | 0621 | 166 | 12 | 34 | 46 | 27,71% |
| RIO BRANCO | 0001 | 0823 | 235 | 12 | 53 | 65 | 27,66% |
| RIO BRANCO | 0009 | 0431 | 217 | 11 | 49 | 60 | 27,65% |
| FEIJÓ | 0007 | 0069 | 104 | 12 | 16 | 28 | 26,92% |
| CAPIXABA | 0002 | 0107 | 187 | 17 | 33 | 50 | 26,74% |
| RIO BRANCO | 0009 | 0445 | 251 | 4 | 59 | 63 | 25,1% |
| RIO BRANCO | 0001 | 0813 | 261 | 16 | 48 | 64 | 24,52% |
| RIO BRANCO | 0009 | 0450 | 248 | 6 | 54 | 60 | 24,19% |
| EPITACIOLÂNDIA | 0006 | 0147 | 203 | 7 | 42 | 49 | 24,14% |
| EPITACIOLÂNDIA | 0006 | 0156 | 169 | 17 | 22 | 39 | 23,08% |
| EPITACIOLÂNDIA | 0006 | 0148 | 223 | 4 | 47 | 51 | 22,87% |
| RIO BRANCO | 0001 | 0816 | 180 | 13 | 28 | 41 | 22,78% |
| RIO BRANCO | 0009 | 0443 | 273 | 6 | 54 | 60 | 21,98% |
| RIO BRANCO | 0001 | 0835 | 207 | 4 | 41 | 45 | 21,74% |
| RIO BRANCO | 0009 | 0448 | 253 | 4 | 51 | 55 | 21,74% |
| RIO BRANCO | 0009 | 0432 | 200 | 9 | 34 | 43 | 21,5% |
| RIO BRANCO | 0001 | 0191 | 141 | 20 | 10 | 30 | 21,28% |
| RIO BRANCO | 0009 | 0429 | 243 | 12 | 39 | 51 | 20,99% |
| EPITACIOLÂNDIA | 0006 | 0142 | 167 | 2 | 32 | 34 | 20,36% |
| RIO BRANCO | 0009 | 0456 | 238 | 11 | 37 | 48 | 20,17% |
| RIO BRANCO | 0009 | 0446 | 305 | 6 | 55 | 61 | 20% |

A concentração define prioridade de conferência. Diferenças no cadastramento biométrico e problemas de equipamento precisam ser verificados antes de atribuir a proporção elevada a conduta irregular. A relação integral está no anexo 10.

## 5. Tempo entre a liberação e a conclusão

A duração abaixo vai da mensagem de liberação do eleitor à mensagem de voto computado. Não inclui a conferência de documentos e a identificação anteriores à liberação. Os horários têm precisão de um segundo.

| Identificação | Votações | Mínimo | Mediana | 90% até | Até 10 s | % até 10 s |
| --- | --- | --- | --- | --- | --- | --- |
| Mesário | 22.654 | 6 s | 20 s | 45 s | 965 | 4,26% |
| Ano de nascimento | 15.325 | 6 s | 18 s | 38 s | 655 | 4,27% |
| Conjunto em análise | 37.979 | 6 s | 19 s | 42 s | 1.620 | 4,27% |
| Biométrica | 415.675 | 4 s | 17 s | 32 s | 19.414 | 4,67% |

Mediana é o valor que divide as durações ao meio. A coluna “90% até” indica a duração que não foi ultrapassada em 90% das ocorrências. O recorte de até dez segundos é descritivo: não representa um tempo mínimo obrigatório de votação.

No conjunto em análise, 4,27% das votações duraram até dez segundos; entre as biométricas, foram 4,67%. Assim, uma duração curta isolada não diferencia, neste recorte, uma votação regular de um possível uso indevido da liberação.

Exemplos de menor duração no conjunto, com desempate por arquivo e horário:

| Município | Zona / seção | Liberação | Forma | Duração |
| --- | --- | --- | --- | --- |
| MÂNCIO LIMA | 0004 / 0364 | 08:30:39 | Mesário | 6 s |
| MÂNCIO LIMA | 0004 / 0439 | 09:14:56 | Ano de nascimento | 6 s |
| JORDÃO | 0005 / 0032 | 07:25:37 | Mesário | 6 s |
| RIO BRANCO | 0001 / 0485 | 08:12:46 | Mesário | 6 s |
| RIO BRANCO | 0001 / 0515 | 10:09:23 | Ano de nascimento | 6 s |
| RIO BRANCO | 0001 / 0538 | 12:22:06 | Ano de nascimento | 6 s |
| RIO BRANCO | 0009 / 0417 | 06:26:55 | Mesário | 6 s |
| PLÁCIDO DE CASTRO | 0008 / 0114 | 13:33:40 | Ano de nascimento | 6 s |
| SENADOR GUIOMARD | 0008 / 0268 | 13:04:19 | Ano de nascimento | 6 s |
| MARECHAL THAUMATURGO | 0004 / 0073 | 06:18:36 | Ano de nascimento | 7 s |
| BRASILÉIA | 0006 / 0020 | 09:23:31 | Mesário | 7 s |
| BRASILÉIA | 0006 / 0155 | 12:32:52 | Ano de nascimento | 7 s |

Não houve duração de até cinco segundos entre as 37.979 votações do conjunto. A lista completa das 1.620 ocorrências de até dez segundos está no anexo 12, sem limitação às sequências sucessivas.

## 6. Votações sucessivas e intervalo entre liberações

Uma sequência reúne votações concluídas consecutivas do procedimento examinado, sem outra forma de identificação entre elas. A análise também separa o tempo entre duas liberações sucessivas do tempo que cada eleitor levou após ser liberado.

| Conjunto | Sequências com 2 ou mais | Com 3 ou mais | Com 5 ou mais | Maior sequência |
| --- | --- | --- | --- | --- |
| Somente mesário | 1.316 | 103 | 2 | 6 |
| Mesário ou ano de nascimento | 3.580 | 557 | 31 | 10 |

As faixas se sobrepõem e não devem ser somadas. As maiores sequências concluídas foram:

| Município / seção | Procedimento | Votações | Início / última liberação | Intervalo médio |
| --- | --- | --- | --- | --- |
| JORDÃO / 0122 | Mesário | 6 | 07:04:52 / 07:19:02 | 170 s |
| PLÁCIDO DE CASTRO / 0024 | Mesário | 5 | 09:12:46 / 09:28:31 | 236,25 s |
| ASSIS BRASIL / 0150 | Conjunto | 10 | 11:28:55 / 11:49:58 | 140,33 s |
| RIO BRANCO / 0824 | Conjunto | 8 | 10:51:27 / 11:00:04 | 73,86 s |

Na sequência de seis liberações por mesário, em Jordão, o menor intervalo entre liberações foi de 125 segundos. Na sequência de dez do conjunto, em Assis Brasil, foi de setenta segundos. As maiores sequências, portanto, não apresentam liberações em intervalos de poucos segundos.

Em toda a análise, o menor intervalo até uma liberação por mesário foi de 64 segundos; até uma liberação por ano de nascimento, 25 segundos. Houve três intervalos de até trinta segundos, todos com ano de nascimento na segunda votação:

| Município / seção | Liberação | Identificação anterior | Intervalo |
| --- | --- | --- | --- |
| CRUZEIRO DO SUL / 0360 | 10:55:29 | Biométrica | 29 s |
| RIO BRANCO / 0443 | 13:29:11 | Biométrica | 25 s |
| RIO BRANCO / 0443 | 13:29:41 | Ano de nascimento | 30 s |

Foi possível comparar a liberação com uma votação anterior concluída em 37.783 casos. Os 196 restantes não tinham um par anterior adequado. Não foram unidos registros de equipamentos ou origens diferentes. A lista de sequências concluídas está no anexo 15.

## 7. Ocorrências isoladas após períodos de espera

A verificação de eventos dispersos foi feita em todas as votações do conjunto, e não apenas nas sequências. A informação de espera foi medida entre a mensagem de que o sistema aguardava o identificador e a digitação que precedeu a liberação.

| Recorte observado | Mesário | Ano | Total |
| --- | --- | --- | --- |
| Até 10 s após espera de pelo menos 5 minutos por identificação | 66 | 48 | 114 |
| Até 10 s após intervalo de pelo menos 5 minutos desde o voto anterior | 136 | 73 | 209 |

Os dois recortes não devem ser somados. O primeiro localiza esperas antes da identificação; o segundo inclui também o tempo gasto com identificação, conferência e eventuais dificuldades. Nenhum deles comprova, sozinho, que a mesa estava ociosa ou que o eleitor estava ausente.

Os 114 casos do primeiro recorte estão em 106 seções. O limite de cinco minutos serve apenas para organizar a conferência: votações após pausas menores continuam incluídas na relação integral das 37.979 ocorrências.

Exemplos com maior espera por identificação entre os casos concluídos em até dez segundos:

| Município | Zona / seção | Liberação | Espera | Identificação | Votação |
| --- | --- | --- | --- | --- | --- |
| RIO BRANCO | 0001 / 0529 | 08:52:39 | 30m 42s | Mesário | 10 s |
| PORTO ACRE | 0001 / 0621 | 14:08:18 | 30m 24s | Ano de nascimento | 8 s |
| CRUZEIRO DO SUL | 0004 / 0449 | 12:24:15 | 29m 00s | Mesário | 10 s |
| CRUZEIRO DO SUL | 0004 / 0449 | 10:50:04 | 22m 39s | Ano de nascimento | 9 s |
| CRUZEIRO DO SUL | 0004 / 0167 | 11:46:24 | 22m 22s | Mesário | 9 s |
| CAPIXABA | 0002 / 0087 | 12:57:39 | 20m 14s | Ano de nascimento | 9 s |
| PORTO WALTER | 0004 / 0447 | 12:37:38 | 19m 34s | Ano de nascimento | 10 s |
| SENADOR GUIOMARD | 0008 / 0226 | 14:00:05 | 19m 29s | Ano de nascimento | 9 s |
| XAPURI | 0002 / 0009 | 12:57:05 | 19m 05s | Mesário | 8 s |
| FEIJÓ | 0007 / 0058 | 09:53:55 | 18m 12s | Mesário | 9 s |

Os tempos de espera puderam ser medidos em 37.977 das 37.979 votações do conjunto. Os dois casos sem os registros necessários não receberam valor presumido. Os anexos 13 e 14 apresentam integralmente os dois recortes, com horários e linhas dos logs.

## 8. Ocorrências operacionais relevantes

Foram encontradas sete liberações interrompidas antes de um registro de voto computado. Elas não integram o total de 37.979 votações concluídas. A ocorrência é relevante para verificar o atendimento ao eleitor afetado, mas não demonstra perda dos votos anteriores da seção.

| Município | Zona / seção | Desligamento | Registro anterior |
| --- | --- | --- | --- |
| PORTO ACRE | 0001 / 0608 | 10:54:30 | Sem motivo explícito no intervalo |
| CRUZEIRO DO SUL | 0004 / 0482 | 08:25:52 | Sem motivo explícito no intervalo |
| RODRIGUES ALVES | 0004 / 0368 | 09:35:06 | Erro de voto não registrado; desligamentos sucessivos |
| RIO BRANCO | 0001 / 0554 | 12:28:19 | Tecla indevida antes do desligamento |
| RIO BRANCO | 0009 / 0053 | 14:30:25 | Sem motivo explícito no intervalo |
| SENA MADUREIRA | 0003 / 0001 | 08:55:44 | Sem motivo explícito no intervalo |
| SENA MADUREIRA | 0003 / 0084 | 10:10:29 | Interação prolongada e tentativas de suspensão |

Em Rodrigues Alves, seção 0368, há erro que orienta desligar e ligar a urna. Em Sena Madureira, seção 0084, houve confirmação de um cargo e tentativas de suspensão antes do desligamento. A mensagem de chave desligada não informa quem acionou o mecanismo. As atas e os atendimentos técnicos devem esclarecer esses casos.

Houve 39 seções com múltiplos blocos de histórico. Quatro tinham duas origens com identificadores de equipamento diferentes no dia. Elas são: Bujari 0009/0002; Cruzeiro do Sul 0004/0394; Sena Madureira 0003/0084; Senador Guiomard 0008/0082. Em Bujari, o primeiro bloco não tinha votações registradas.

Dez seções foram separadas da comparação estatística: sete por interrupção e quatro por duas origens no dia, com uma seção comum aos dois grupos. Os totais dessas seções permanecem no universo estadual; a exclusão afeta apenas a comparação com pares. A relação completa e os motivos constam dos anexos 01 a 04.

Não houve erro de leitura, classificação indefinida ou mensagem de voto computado sem liberação associada. A diferença entre as 453.714 liberações e as 453.654 votações concluídas fecha em 53 suspensões explícitas sem voto e sete interrupções.

## 9. Conclusão e conferências recomendadas

O Acre registra 37.979 votações concluídas com liberação por mesário ou confirmação do ano de nascimento. O total é relevante para delimitar a verificação de possível votação em nome de ausentes, inclusive em ocorrências isoladas.

A análise localizou concentração dos dois procedimentos em 41 seções, com 2.458 votações do conjunto. Foram identificadas também 1.620 conclusões em até dez segundos, incluindo 114 após espera de pelo menos cinco minutos por identificação. Esses conjuntos se sobrepõem; não representam números de fraudes a serem somados.

As maiores sequências não mostraram intervalos de poucos segundos entre as liberações. A conclusão curta, isoladamente, também ocorre entre eleitores identificados por biometria. Os dados permitem selecionar ocorrências para conferência, mas não demonstram quem estava fisicamente na seção.

A investigação deve priorizar:

- As 41 seções com concentração elevada, confrontando o comparecimento registrado e o perfil de cadastramento biométrico do eleitorado.

- Os registros de espera e conclusão curta, verificando se há justificativa operacional e correspondência com o atendimento efetivamente realizado.

- As assinaturas nos casos em que são exigidas, as atas e os registros técnicos, para esclarecer utilização de procedimentos complementares e eventuais falhas de leitor.

- As sete interrupções e as mudanças de identificador de equipamento, verificando continuidade, motivo da intervenção e destino do atendimento ao eleitor afetado.

A confirmação de fraude por voto em nome de ausente exige demonstrar que uma pessoa registrada como votante não compareceu e que houve uso indevido de sua habilitação. Essa demonstração não pode ser obtida apenas pela quantidade de liberações, pelo tempo ou por sequências anônimas do log.

## 10. Fontes e método

Foram examinados 2.270 logs, correspondentes às 2.270 seções principais da configuração oficial do Acre. A análise de tempos foi refeita sobre o pacote bruto do TSE, conferindo as contagens por seção e preservando a referência de origem e linha de cada votação.

A comparação de proporções utilizou seções do mesmo município e zona, com pelo menos cem votações concluídas e grupo mínimo de vinte seções. O limite foi o terceiro quartil mais três vezes o intervalo interquartil, exigindo também diferença superior a dez pontos percentuais da mediana. É um critério de triagem, sem ajuste individual pelo cadastramento biométrico. Foram comparadas 2.200 seções. Santa Rosa do Purus não atingiu o tamanho mínimo de grupo.

A duração foi calculada entre liberação e voto computado. O intervalo entre liberações e a espera por identificação foram tratados separadamente. Os horários foram reproduzidos como constam nos equipamentos, sem conversão de fuso e sem presumir sincronização externa dos relógios.

Os dados não identificam o candidato escolhido e não foram usados para atribuir voto individual. A análise não realizou perícia de hardware, validação criptográfica de assinaturas nem conferência dos cadernos de votação. Os arquivos de dados permitem reproduzir os recortes sem depender dos exemplos apresentados nas tabelas.

Fonte de resultados e originais selecionados: https://github.com/hugohalima-hash/auditoria_eleicoes_2026/releases/download/auditoria-v3-41263277696/AC-tentativa1.zip

Pacote bruto oficial: https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2026/arqurnatot/bu_imgbu_logjez_rdv_vscmr_2026_2t_AC.zip

Configuração oficial: https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3221/config/ac/ac-p003221-cs.json

Execução e código: https://github.com/hugohalima-hash/auditoria_eleicoes_2026/actions/runs/41263277696. Commit de origem: 83d6bed1523a4ec20d9a55dce4e7aaa49646023d.

Integridade do pacote publicado - SHA-256: e72a82e0720f62bfc7a682946f4cda37fcbeb94aa22bf94e06d6fb7ed5ab1d95

Anexos: totais das 2.270 seções; registros das 37.979 votações do conjunto; 41 seções com proporção elevada; referências de comparação; votações curtas; ocorrências após pausas e esperas; sequências concluídas; e relações das interrupções e dos históricos múltiplos. Cada linha de votação contém arquivo, origem e linhas do log para conferência.
