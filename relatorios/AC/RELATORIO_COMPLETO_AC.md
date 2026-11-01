# Acre - liberações sucessivas e intervalo entre eleitores

## 1. Resultado principal

ACRE | Auditoria dos logs do segundo turno de 25/10/2026. Emissão: 01/11/2026. Foco: liberações sucessivas de eleitores e intervalo entre uma liberação e a seguinte.

Sim, houve liberações sucessivas pelo mesário na mesma zona e seção. Uma sequência significa que esses atendimentos ocorreram um após o outro, sem uma liberação de outra categoria no meio.

| Procedimento | Séries com 2+ | Séries com 3+ | Maior série | Séries rápidas* |
| --- | --- | --- | --- | --- |
| Somente mesário | 1.316 | 103 | 6 | 0 |
| Mesário ou ano de nascimento | 3.580 | 557 | 10 | 1 |

* Séries com pelo menos três liberações que terminaram em voto computado e intervalo médio menor que a referência rápida das liberações biométricas na própria seção. O critério e os casos estão detalhados adiante.

A maior série exclusivamente de mesário teve 6 liberações, em JORDÃO - zona 0005, seção 0122. Os intervalos foram 186, 178, 182, 179, 125 segundos. A média foi 170 segundos entre liberações.

A maior série do conjunto teve 10 liberações, em ASSIS BRASIL - zona 0006, seção 0150. Ela mistura os dois procedimentos e não corresponde a dez liberações exclusivamente pelo mesário. Sua média foi 140,33 segundos.

A única série que atingiu a triagem rápida teve três confirmações por ano de nascimento, sem autorização explícita de mesário: Rio Branco, zona 0001, seção 0830, às 10:12:12, 10:12:55 e 10:13:51. Os intervalos foram 43 e 56 segundos, média de 49,5 s. É um resultado limítrofe: apenas 0,5 s abaixo da referência rápida local de 50 s.

Os totais permanecem relevantes, mesmo quando não há sequência: 22.654 votações concluídas com registros de mesário e 15.325 com ano de nascimento, somando 37.979 de 453.654 votações no estado. Quarenta e uma seções apresentam concentração elevada do conjunto.

Os resultados selecionam registros para conferência. Os logs, sozinhos, não demonstram que um eleitor estava ausente ou que outra pessoa votou em seu lugar.

## 2. Como ler os intervalos

O relógio começa na mensagem “Eleitor foi habilitado” e termina na mesma mensagem do eleitor seguinte. Esse é o intervalo entre liberações. Ele abrange a votação anterior e o atendimento necessário até liberar a pessoa seguinte.

| Exemplo ilustrativo | Horário | Intervalo |
| --- | --- | --- |
| Primeira liberação | 10:00:00 | - |
| Segunda liberação | 10:01:20 | 80 segundos |
| Terceira liberação | 10:02:30 | 70 segundos |

Nesse exemplo, há três liberações e dois intervalos. A média é (80 + 70) ÷ 2 = 75 segundos. O tempo que cada pessoa levou para digitar e confirmar não é usado como critério de suspeita neste relatório.

A comparação usa o mesmo marco para todos os procedimentos. Quando há a mensagem específica “Mesário N habilitou o eleitor”, o horário também é preservado no arquivo de pares. Ele não é misturado com o marco comum “Eleitor foi habilitado”.

A referência da própria seção usa pares biométricos consecutivos: uma liberação biométrica seguida de outra biométrica. Assim, compara-se o ritmo de atendimento dentro do mesmo local. A média inclui esperas longas; a mediana representa o valor central e é menos afetada por essas esperas.

Não há um tempo obrigatório presumido para liberar o eleitor. O procedimento por mesário pode exigir etapas adicionais, mas o efeito no intervalo precisa aparecer nos dados. Diferenças de fila, horário, dificuldade de identificação e perfil dos eleitores também podem alterar o ritmo.

As sequências são interrompidas por outro procedimento, por atendimento sem conclusão no recorte de votos concluídos, por mudança de equipamento ou origem e por quebra de continuidade do relógio. Não são unidos atendimentos de zonas ou seções diferentes.

## 3. Houve sucessão? Quantas liberações?

| Procedimento | Séries de liberações 2+ | Maior | Séries concluídas 2+ | Seções com série 2+ | Seções com série 3+ |
| --- | --- | --- | --- | --- | --- |
| Somente mesário | 1.316 | 6 | 1.316 | 869 | 90 |
| Mesário ou ano de nascimento | 3.580 | 10 | 3.580 | 1.490 | 353 |

“Séries de liberações” inclui também as que não terminaram em voto computado. “Séries concluídas” exige conclusão de todos os atendimentos da série. As tabelas de ritmo a seguir usam as concluídas. As duas contagens estão disponíveis nos anexos; não são somadas.

Distribuição dos intervalos de pares consecutivos concluídos, em todo o Acre:

| Par consecutivo | Pares | Média (s) | Mediana (s) | 10% até (s) | Mínimo (s) |
| --- | --- | --- | --- | --- | --- |
| Biométrica → biométrica | 380.028 | 154,13 | 84 | 48 | 23 |
| Mesário → mesário | 1.433 | 203,2 | 153 | 102,2 | 72 |
| Ano → ano | 1.360 | 181,38 | 101 | 61 | 30 |
| Biométrica → mesário | 20.317 | 224,05 | 158 | 103 | 64 |

“10% até” é a referência rápida: dez em cada cem intervalos biométricos ficaram nesse valor ou abaixo. A tabela estadual é descritiva. A seleção de casos rápidos compara cada série com a biometria de sua própria seção, evitando usar uma média estadual como regra para todos os locais.

O anexo de sequências informa todas as séries: município, zona, seção, horários de cada liberação, intervalo de cada par, média, menor e maior intervalo e referência biométrica local. Não há limite de dez ocorrências na relação de dados.

## 4.1. Maiores sequências somente de mesário

C03 | JORDÃO - zona 0005, seção 0122. Somente mesário: 6 liberações; 6 de mesário e 0 de ano de nascimento.

| Ordem | Liberação | Intervalo desde a anterior |
| --- | --- | --- |
| 1 | 07:04:52 | - |
| 2 | 07:07:58 | 186 s |
| 3 | 07:10:56 | 178 s |
| 4 | 07:13:58 | 182 s |
| 5 | 07:16:57 | 179 s |
| 6 | 07:19:02 | 125 s |

Média da série: 170 s. Na mesma seção, 117 pares biométricos tiveram média 180,03 s e mediana 98 s. A média da série equivale a 94,43% da média biométrica.

C07 | PLÁCIDO DE CASTRO - zona 0008, seção 0024. Somente mesário: 5 liberações; 5 de mesário e 0 de ano de nascimento.

| Ordem | Liberação | Intervalo desde a anterior |
| --- | --- | --- |
| 1 | 09:12:46 | - |
| 2 | 09:14:27 | 101 s |
| 3 | 09:18:30 | 243 s |
| 4 | 09:20:43 | 133 s |
| 5 | 09:28:31 | 468 s |

Média da série: 236,25 s. Na mesma seção, 115 pares biométricos tiveram média 176,38 s e mediana 93 s. A média da série equivale a 133,94% da média biométrica.

## 4.2. Maiores sequências do conjunto

C08 | ASSIS BRASIL - zona 0006, seção 0150. Mesário ou ano de nascimento: 10 liberações; 2 de mesário e 8 de ano de nascimento.

| Ordem | Liberação | Intervalo desde a anterior |
| --- | --- | --- |
| 1 | 11:28:55 | - |
| 2 | 11:30:17 | 82 s |
| 3 | 11:31:29 | 72 s |
| 4 | 11:37:04 | 335 s |
| 5 | 11:38:14 | 70 s |
| 6 | 11:39:56 | 102 s |
| 7 | 11:41:06 | 70 s |
| 8 | 11:46:16 | 310 s |
| 9 | 11:47:30 | 74 s |
| 10 | 11:49:58 | 148 s |

Média da série: 140,33 s. Na mesma seção, 53 pares biométricos tiveram média 106,42 s e mediana 72 s. A média da série equivale a 131,87% da média biométrica.

C04 | RIO BRANCO - zona 0001, seção 0824. Mesário ou ano de nascimento: 8 liberações; 1 de mesário e 7 de ano de nascimento.

| Ordem | Liberação | Intervalo desde a anterior |
| --- | --- | --- |
| 1 | 10:51:27 | - |
| 2 | 10:52:30 | 63 s |
| 3 | 10:55:14 | 164 s |
| 4 | 10:56:30 | 76 s |
| 5 | 10:57:14 | 44 s |
| 6 | 10:58:11 | 57 s |
| 7 | 10:59:09 | 58 s |
| 8 | 11:00:04 | 55 s |

Média da série: 73,86 s. Na mesma seção, 101 pares biométricos tiveram média 125,68 s e mediana 72 s. A média da série equivale a 58,76% da média biométrica.

## 5. Sequências mais rápidas e comparação local

Para uma triagem de ritmo, foram selecionadas séries com pelo menos três liberações, todas concluídas, cuja média ficou abaixo da referência rápida biométrica da própria seção. Exigiram-se pelo menos trinta pares biométricos e registros adequados à comparação. O limite é exploratório; não indica uma probabilidade de fraude nem foi ajustado para múltiplas comparações.

Resultado: 0 séries exclusivamente de mesário e 1 séries do conjunto atenderam ao critério. Os grupos podem se sobrepor e não devem ser somados.

Duas séries mais rápidas com pelo menos três liberações: Somente mesário.

C02 | JORDÃO - zona 0005, seção 0056. 3 liberações (3 de mesário; 0 de ano), de 08:34:35 a 08:37:11. Intervalos: 78, 78 s. Média: 78 s; biometria local: média 231,19 s, mediana 85 s, referência rápida 53,6 s (79 pares).

C01 | CAPIXABA - zona 0002, seção 0078. 3 liberações (3 de mesário; 0 de ano), de 07:54:30 a 07:57:25. Intervalos: 81, 94 s. Média: 87,5 s; biometria local: média 220,18 s, mediana 127 s, referência rápida 48 s (120 pares).

Duas séries mais rápidas com pelo menos três liberações: Mesário ou ano de nascimento.

C06 | RIO BRANCO - zona 0009, seção 0443. 3 liberações (0 de mesário; 3 de ano), de 13:29:11 a 13:30:49. Intervalos: 30, 68 s. Média: 49 s; biometria local: média 112,3 s, mediana 70 s, referência rápida 40 s (174 pares).

C05 | RIO BRANCO - zona 0001, seção 0830. 3 liberações (0 de mesário; 3 de ano), de 10:12:12 a 10:13:51. Intervalos: 43, 56 s. Média: 49,5 s; biometria local: média 138,93 s, mediana 84 s, referência rápida 50 s (167 pares).

| Caso / município | Zona / seção | Grupo | Nº | Média (s) | Ref. rápida (s) |
| --- | --- | --- | --- | --- | --- |
| C05 / RIO BRANCO | 0001 / 0830 | Conjunto | 3 | 49,5 | 50 |

O caso C05 é composto por três confirmações de ano de nascimento. Sua média, 49,5 s, está somente 0,5 s abaixo do corte local de 50 s. Uma diferença tão pequena exige cautela: o caso serve para conferência, sem evidência forte de ritmo excepcional. Não há uma sequência de autorização explícita de mesário nesse caso.

Uma série pode ser mais rápida que a média sem estar fora do padrão: aproximadamente metade dos intervalos fica abaixo da mediana. Por isso, a média isolada não basta para rotular um caso como anormal. Os logs integrais dos casos destacados permitem verificar se houve tentativas biométricas, confirmações, cancelamentos ou outros acontecimentos entre as liberações.

## 6. Totais e concentrações por seção

Uma possível utilização indevida não precisa ocorrer em série. O universo de conferência inclui todas as 37.979 votações concluídas do conjunto, distribuídas ao longo do dia. São 22.654 com registro de mesário e 15.325 com confirmação do ano de nascimento. Ano de nascimento não equivale automaticamente a autorização identificada de mesário.

Quarenta e uma seções ultrapassaram a referência local de concentração, reunindo 2.458 votações do conjunto em 8.702 votações concluídas nessas seções. A concentração e o ritmo são critérios diferentes e não devem ser somados como se contassem fraudes distintas.

| Município | Zona / seção | Mesário | Ano | Total | % |
| --- | --- | --- | --- | --- | --- |
| BUJARI | 0009 / 0441 | 15 | 76 | 91 | 36,84% |
| CAPIXABA | 0002 / 0107 | 17 | 33 | 50 | 26,74% |
| PORTO ACRE | 0001 / 0621 | 12 | 34 | 46 | 27,71% |
| BRASILÉIA | 0006 / 0152 | 9 | 54 | 63 | 28,12% |
| PORTO WALTER | 0004 / 0447 | 2 | 46 | 48 | 41,03% |
| RODRIGUES ALVES | 0004 / 0455 | 27 | 32 | 59 | 27,83% |
| EPITACIOLÂNDIA | 0006 / 0142 | 2 | 32 | 34 | 20,36% |
| EPITACIOLÂNDIA | 0006 / 0147 | 7 | 42 | 49 | 24,14% |
| EPITACIOLÂNDIA | 0006 / 0148 | 4 | 47 | 51 | 22,87% |
| EPITACIOLÂNDIA | 0006 / 0151 | 4 | 73 | 77 | 38,31% |
| EPITACIOLÂNDIA | 0006 / 0156 | 17 | 22 | 39 | 23,08% |
| FEIJÓ | 0007 / 0069 | 12 | 16 | 28 | 26,92% |
| RIO BRANCO | 0001 / 0191 | 20 | 10 | 30 | 21,28% |
| RIO BRANCO | 0001 / 0813 | 16 | 48 | 64 | 24,52% |
| RIO BRANCO | 0001 / 0816 | 13 | 28 | 41 | 22,78% |
| RIO BRANCO | 0001 / 0820 | 5 | 85 | 90 | 35,16% |
| RIO BRANCO | 0001 / 0821 | 5 | 67 | 72 | 28,69% |
| RIO BRANCO | 0001 / 0822 | 4 | 59 | 63 | 27,88% |
| RIO BRANCO | 0001 / 0823 | 12 | 53 | 65 | 27,66% |
| RIO BRANCO | 0001 / 0824 | 4 | 92 | 96 | 38,55% |
| RIO BRANCO | 0001 / 0826 | 11 | 59 | 70 | 30,04% |
| RIO BRANCO | 0001 / 0829 | 6 | 51 | 57 | 28,5% |
| RIO BRANCO | 0001 / 0835 | 4 | 41 | 45 | 21,74% |
| RIO BRANCO | 0009 / 0429 | 12 | 39 | 51 | 20,99% |
| RIO BRANCO | 0009 / 0431 | 11 | 49 | 60 | 27,65% |
| RIO BRANCO | 0009 / 0432 | 9 | 34 | 43 | 21,5% |
| RIO BRANCO | 0009 / 0443 | 6 | 54 | 60 | 21,98% |
| RIO BRANCO | 0009 / 0445 | 4 | 59 | 63 | 25,1% |
| RIO BRANCO | 0009 / 0446 | 6 | 55 | 61 | 20% |
| RIO BRANCO | 0009 / 0448 | 4 | 51 | 55 | 21,74% |
| RIO BRANCO | 0009 / 0449 | 9 | 74 | 83 | 32,3% |
| RIO BRANCO | 0009 / 0450 | 6 | 54 | 60 | 24,19% |
| RIO BRANCO | 0009 / 0453 | 5 | 92 | 97 | 35,79% |
| RIO BRANCO | 0009 / 0456 | 11 | 37 | 48 | 20,17% |
| SENA MADUREIRA | 0003 / 0155 | 16 | 33 | 49 | 29,34% |
| TARAUACÁ | 0005 / 0130 | 12 | 53 | 65 | 31,71% |
| TARAUACÁ | 0005 / 0133 | 13 | 36 | 49 | 33,56% |
| TARAUACÁ | 0005 / 0134 | 33 | 38 | 71 | 33,02% |
| SENADOR GUIOMARD | 0008 / 0268 | 11 | 46 | 57 | 33,93% |
| MANOEL URBANO | 0003 / 0154 | 16 | 41 | 57 | 31,32% |
| ASSIS BRASIL | 0006 / 0150 | 22 | 79 | 101 | 49,51% |

## 7. Ocorrências técnicas e conclusão

Os 2.270 logs foram lidos e as contagens por seção reconciliadas com o pacote publicado. Houve 453.714 liberações e 453.654 votações concluídas: a diferença corresponde a 53 suspensões explícitas sem voto e sete interrupções. Não houve voto computado sem habilitação associada, classificação indefinida ou erro de leitura.

Sete atendimentos foram interrompidos por desligamento antes de uma conclusão vinculada. Quatro seções tinham registros de equipamentos diferentes no dia; uma delas também estava entre as sete interrupções. Essas dez seções não foram usadas para selecionar anormalidades estatísticas. Os históricos e motivos estão nos anexos técnicos.

Houve sucessão de liberações pelo mesário. O relatório identifica onde ocorreu, quantas liberações compõem cada série e qual foi o intervalo de cada par. A rapidez é avaliada diante do atendimento biométrico da própria seção, sem utilizar a velocidade de digitação do voto como sinal de fraude.

A prioridade de conferência são as séries selecionadas pelo ritmo e as 41 seções com concentração elevada. Devem ser confrontadas com os registros de comparecimento, as atas e os documentos de atendimento técnico. As séries maiores e as mais rápidas também são apresentadas, mesmo quando não atingem o critério de triagem, para permitir leitura direta das evidências.

Uma suspeita de voto em nome de faltante exige confirmar que o eleitor registrado não compareceu e que sua habilitação foi usada indevidamente. A sequência temporal permite orientar essa verificação; não identifica quem estava diante da urna.

## 8. Fontes e anexos de conferência

Comparação de concentração: mesma zona e município; pelo menos cem votações concluídas; grupo de vinte ou mais seções. O limite é o maior entre terceiro quartil + três intervalos interquartis e mediana + dez pontos percentuais. Foram comparadas 2.200 seções. O perfil de cadastramento biométrico individual não foi ajustado.

Fonte: pacote oficial do TSE do Acre, segundo turno de 2026. Os horários foram mantidos como gravados no equipamento, sem conversão de fuso. Cada sequência preserva a origem, o equipamento e as linhas do log. Não se presume sincronização externa entre urnas.

Resultado publicado: https://github.com/hugohalima-hash/auditoria_eleicoes_2026/releases/tag/auditoria-v3-41263277696. Arquivo de referência: AC-tentativa1.zip. SHA-256: e72a82e0720f62bfc7a682946f4cda37fcbeb94aa22bf94e06d6fb7ed5ab1d95.

Pacote bruto: https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2026/arqurnatot/bu_imgbu_logjez_rdv_vscmr_2026_2t_AC.zip. SHA-256: 7e58076367c9a0d8002b7918fe33183a2aee8aaf562d32555cf62ce10d188dc5.

Anexos digitais: Acre_Sequencias_e_Logs.zip contém todos os pares consecutivos, todas as séries com dois ou mais atendimentos, referências biométricas por seção, casos destacados e trechos cronológicos sem cortes internos. Acre_Logs_Integrais.zip contém os arquivos originais e os logs do dia inteiro de 46 seções: as 41 com concentração elevada e as demais dos exemplos destacados, sem duplicar seções. Os dois pacotes incluem SHA-256.

Nas páginas seguintes estão os trechos integrais dos casos de ritmo e dos exemplos destacados. O trecho começa no encerramento do atendimento anterior e vai até a conclusão do último da série. Quando não há atendimento anterior no mesmo bloco, inclui o contexto disponível antes da primeira liberação. Todas as linhas intermediárias são preservadas; quebras visuais de linha não alteram a ordem. O arquivo original completo está no anexo digital.

A análise não realizou conferência de cadernos, perícia do equipamento, validação criptográfica de assinaturas ou conciliação individual por candidato. A comparação de ritmo é exploratória e não controla, individualmente, fila e perfil dos eleitores. Os dados são públicos e a reprodução está no repositório auditoria_eleicoes_2026, em relatorios/AC/ritmo/.

## Anexo C01 - CAPIXABA - zona 0002, seção 0078

Somente mesário. Horários: 07:54:30 | 07:55:51 | 07:57:25. Intervalos em segundos: 81 | 94.

```text
C01 | CAPIXABA | Zona 0002 | Seção 0078
Arquivo: o03221ac0101500020078-log.jez
Origem: raiz!logd.dat
Linhas 5297-5381, sem omitir eventos intermediários. Prefixo numérico = linha original.

005297	25/10/2026 07:48:21	INFO	02268447	VOTA	O voto do eleitor foi computado	D58A0442419A1287
005298	25/10/2026 07:48:22	INFO	02268447	VOTA	Aguardando digitação do identificador do eleitor	2D673A2D0089B265
005299	25/10/2026 07:53:39	INFO	02268447	VOTA	Identificador do eleitor digitado pelo mesário	7BA6EA27A7ACE01B
005300	25/10/2026 07:53:39	INFO	02268447	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	410A5AADFE1190B3
005301	25/10/2026 07:53:39	INFO	02268447	VOTA	Foto do eleitor apresentada	AA84589D853C8B7D
005302	25/10/2026 07:53:41	INFO	02268447	VOTA	Solicita digital. Tentativa [1] de [4]	17B394530D035DC1
005303	25/10/2026 07:53:47	INFO	02268447	VOTA	Capturada a digital. Tentativa [1] de [4]	0E7568B7DF8E5EDE
005304	25/10/2026 07:53:49	INFO	02268447	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [1] de [4]	4AF70CD3BDAB93C4
005305	25/10/2026 07:53:52	INFO	02268447	VOTA	Solicita digital. Tentativa [2] de [4]	8C95EA53A33BC528
005306	25/10/2026 07:53:54	INFO	02268447	VOTA	Capturada a digital. Tentativa [2] de [4]	E48D754F4E70113D
005307	25/10/2026 07:53:57	INFO	02268447	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [2] de [4]	9C90DBBFCE3A0AD7
005308	25/10/2026 07:53:58	INFO	02268447	VOTA	Solicita digital. Tentativa [3] de [4]	4051D0DAFA9FE13A
005309	25/10/2026 07:54:02	INFO	02268447	VOTA	Capturada a digital. Tentativa [3] de [4]	6DD7C81ADE55EBA1
005310	25/10/2026 07:54:04	INFO	02268447	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [3] de [4]	A2871F7A93B9EA81
005311	25/10/2026 07:54:05	INFO	02268447	VOTA	Solicita digital. Tentativa [4] de [4]	DC2172786681169F
005312	25/10/2026 07:54:11	INFO	02268447	VOTA	Capturada a digital. Tentativa [4] de [4]	3D462474136D79CE
005313	25/10/2026 07:54:13	INFO	02268447	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [4] de [4]	21EA5FF5C3EDF5C4
005314	25/10/2026 07:54:17	INFO	02268447	VOTA	Solicitação de dado pessoal do eleitor para habilitação manual	DA2FCD0414A24EF0
005315	25/10/2026 07:54:23	INFO	02268447	VOTA	Dado digitado confere	AE24C7E24D010F88
005316	25/10/2026 07:54:23	INFO	02268447	VOTA	Solicita digital do mesário	BC6385A8DAD20548
005317	25/10/2026 07:54:27	INFO	02268447	VOTA	Biometria do mesário 005153452402 encontrada em eleitores	A047A6F37C630E64
005318	25/10/2026 07:54:27	INFO	02268447	VOTA	Mesário 005153452402 habilitou o eleitor	BA98E97BFAA59347
005319	25/10/2026 07:54:30	INFO	02268447	VOTA	Eleitor foi habilitado	0C0817D760A86E0B
005320	25/10/2026 07:54:38	INFO	02268447	VOTA	Voto confirmado para [Governador]	D1E33B10809CA1A6
005321	25/10/2026 07:54:43	INFO	02268447	VOTA	Voto confirmado para [Presidente]	695835FD3908CB54
005322	25/10/2026 07:54:44	INFO	02268447	VOTA	O voto do eleitor foi computado	A58FCD3A22F9D06F
005323	25/10/2026 07:54:45	INFO	02268447	VOTA	Aguardando digitação do identificador do eleitor	8B9AA178EFAC9772
005324	25/10/2026 07:55:06	INFO	02268447	VOTA	Identificador do eleitor digitado pelo mesário	672F37B36709A60A
005325	25/10/2026 07:55:06	INFO	02268447	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	58FE4182C7F4DE2F
005326	25/10/2026 07:55:06	INFO	02268447	VOTA	Foto do eleitor apresentada	F6391E8620C8B895
005327	25/10/2026 07:55:08	INFO	02268447	VOTA	Solicita digital. Tentativa [1] de [4]	D40D67474B813190
005328	25/10/2026 07:55:14	INFO	02268447	VOTA	Capturada a digital. Tentativa [1] de [4]	BE0276C467F3795F
005329	25/10/2026 07:55:16	INFO	02268447	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [1] de [4]	4F4DDCC32F6EF864
005330	25/10/2026 07:55:17	INFO	02268447	VOTA	Solicita digital. Tentativa [2] de [4]	B0F6D8DAFC808393
005331	25/10/2026 07:55:20	INFO	02268447	VOTA	Capturada a digital. Tentativa [2] de [4]	DB36B24C10657E6E
005332	25/10/2026 07:55:22	INFO	02268447	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [2] de [4]	A80D058990A15940
005333	25/10/2026 07:55:23	INFO	02268447	VOTA	Solicita digital. Tentativa [3] de [4]	33895157DC57559D
005334	25/10/2026 07:55:27	INFO	02268447	VOTA	Capturada a digital. Tentativa [3] de [4]	91766C32E4CCD553
005335	25/10/2026 07:55:29	INFO	02268447	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [3] de [4]	C99C386F8A059FC6
005336	25/10/2026 07:55:31	INFO	02268447	VOTA	Solicita digital. Tentativa [4] de [4]	462EE0CCAE751DB4
005337	25/10/2026 07:55:33	INFO	02268447	VOTA	Espaço livre na MI [3.4 GB]	35C200887166ED19
005338	25/10/2026 07:55:33	INFO	02268447	VOTA	Espaço livre na MV [360.1 MB]	D8633300CCE7EE42
005339	25/10/2026 07:55:33	INFO	02268447	VOTA	Espaço utilizado na MI [16.8 MB]	F16C8AFA1BEE2AA9
005340	25/10/2026 07:55:33	INFO	02268447	VOTA	Espaço utilizado na MV [17.2 MB]	1B59B57DE5F3B609
005341	25/10/2026 07:55:33	INFO	02268447	VOTA	Quantidade de memória total [3.7 GB]	E0E0239A30B4089B
005342	25/10/2026 07:55:33	INFO	02268447	VOTA	Quantidade de memória livre [3.3 GB]	C13E0635850F25F4
005343	25/10/2026 07:55:33	INFO	02268447	VOTA	Quantidade de memória usada [385.3 MB]	9C1E98841D0F977B
005344	25/10/2026 07:55:33	INFO	02268447	VOTA	Urna ligada conectada na rede CA em [132.47V] e na Bateria Interna com [13.43V/0A]	8B9AA44A30157411
005345	25/10/2026 07:55:36	INFO	02268447	VOTA	Capturada a digital. Tentativa [4] de [4]	E577FBDA9B22B6FB
005346	25/10/2026 07:55:38	INFO	02268447	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [4] de [4]	6021EC9571A7862D
005347	25/10/2026 07:55:41	INFO	02268447	VOTA	Solicitação de dado pessoal do eleitor para habilitação manual	319BEBFDF2ED6E3B
005348	25/10/2026 07:55:44	INFO	02268447	VOTA	Dado digitado confere	3D595873221D6DCB
005349	25/10/2026 07:55:44	INFO	02268447	VOTA	Solicita digital do mesário	EA5B9D610E2E36EA
005350	25/10/2026 07:55:48	INFO	02268447	VOTA	Biometria do mesário 005153452402 encontrada em eleitores	45AC4359B5311E5A
005351	25/10/2026 07:55:48	INFO	02268447	VOTA	Mesário 005153452402 habilitou o eleitor	287ACE9D8DCEBE51
005352	25/10/2026 07:55:51	INFO	02268447	VOTA	Eleitor foi habilitado	15667DFFCAD1220E
005353	25/10/2026 07:55:58	INFO	02268447	VOTA	Tecla indevida pressionada	B1DE5E245376FAD7
005354	25/10/2026 07:56:06	INFO	02268447	VOTA	Voto confirmado para [Governador]	C445433F7236EC18
005355	25/10/2026 07:56:14	INFO	02268447	VOTA	Voto confirmado para [Presidente]	2253352F5BE84164
005356	25/10/2026 07:56:14	INFO	02268447	VOTA	O voto do eleitor foi computado	1D9948B993EE8ED0
005357	25/10/2026 07:56:15	INFO	02268447	VOTA	Aguardando digitação do identificador do eleitor	078216DE44B0C0BF
005358	25/10/2026 07:56:33	INFO	02268447	VOTA	Identificador do eleitor digitado pelo mesário	548EB767EBF9EC7C
005359	25/10/2026 07:56:33	INFO	02268447	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	B7E96DD8800FCC33
005360	25/10/2026 07:56:33	INFO	02268447	VOTA	Foto do eleitor apresentada	9DEE540A3F4021FB
005361	25/10/2026 07:56:34	INFO	02268447	VOTA	Solicita digital. Tentativa [1] de [4]	CB8E3A90681F40D8
005362	25/10/2026 07:56:42	INFO	02268447	VOTA	Capturada a digital. Tentativa [1] de [4]	079D61AE2D4CE957
005363	25/10/2026 07:56:44	INFO	02268447	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [1] de [4]	F678E5745DD45A73
005364	25/10/2026 07:56:45	INFO	02268447	VOTA	Solicita digital. Tentativa [2] de [4]	BF5EB5CCF7209463
005365	25/10/2026 07:56:53	INFO	02268447	VOTA	Capturada a digital. Tentativa [2] de [4]	9709D126EE94C2FC
005366	25/10/2026 07:56:55	INFO	02268447	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [2] de [4]	A3B672C5718E3A1C
005367	25/10/2026 07:56:55	INFO	02268447	VOTA	Solicita digital. Tentativa [3] de [4]	A68F68C1A2E34B0E
005368	25/10/2026 07:57:03	INFO	02268447	VOTA	Capturada a digital. Tentativa [3] de [4]	FA9937797C4FE3BA
005369	25/10/2026 07:57:05	INFO	02268447	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [3] de [4]	AABDD520ECE24735
005370	25/10/2026 07:57:07	INFO	02268447	VOTA	Solicita digital. Tentativa [4] de [4]	B4DA3E5D9E991C30
005371	25/10/2026 07:57:09	INFO	02268447	VOTA	Capturada a digital. Tentativa [4] de [4]	ABC1E163B009B7F9
005372	25/10/2026 07:57:12	INFO	02268447	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [4] de [4]	ADDACB35B535DE70
005373	25/10/2026 07:57:15	INFO	02268447	VOTA	Solicitação de dado pessoal do eleitor para habilitação manual	E70A714E070F01D5
005374	25/10/2026 07:57:19	INFO	02268447	VOTA	Dado digitado confere	A6022CB9F49B04F2
005375	25/10/2026 07:57:19	INFO	02268447	VOTA	Solicita digital do mesário	48B68AF89BAC41C2
005376	25/10/2026 07:57:23	INFO	02268447	VOTA	Biometria do mesário 005153452402 encontrada em eleitores	49216C58BAB933C4
005377	25/10/2026 07:57:23	INFO	02268447	VOTA	Mesário 005153452402 habilitou o eleitor	9C3E5AB1050EF478
005378	25/10/2026 07:57:25	INFO	02268447	VOTA	Eleitor foi habilitado	C27FC82C9348A3D6
005379	25/10/2026 07:57:33	INFO	02268447	VOTA	Voto confirmado para [Governador]	CCD69EA7E8B6AA23
005380	25/10/2026 07:57:36	INFO	02268447	VOTA	Voto confirmado para [Presidente]	2544B20F816347E0
005381	25/10/2026 07:57:37	INFO	02268447	VOTA	O voto do eleitor foi computado	81580E44BD53DC7D

```

## Anexo C02 - JORDÃO - zona 0005, seção 0056

Somente mesário. Horários: 08:34:35 | 08:35:53 | 08:37:11. Intervalos em segundos: 78 | 78.

```text
C02 | JORDÃO | Zona 0005 | Seção 0056
Arquivo: o03221ac0110400050056-log.jez
Origem: raiz!logd.dat
Linhas 7215-7290, sem omitir eventos intermediários. Prefixo numérico = linha original.

007215	25/10/2026 08:32:58	INFO	02269515	VOTA	O voto do eleitor foi computado	8B0377090F99BA80
007216	25/10/2026 08:33:00	INFO	02269515	VOTA	Aguardando digitação do identificador do eleitor	C6050548AB439665
007217	25/10/2026 08:33:47	INFO	02269515	VOTA	Identificador do eleitor digitado pelo mesário	902159EF236F1E1F
007218	25/10/2026 08:33:47	INFO	02269515	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	D49E925EBA137421
007219	25/10/2026 08:33:47	INFO	02269515	VOTA	Foto do eleitor apresentada	C290F0953228CB63
007220	25/10/2026 08:33:50	INFO	02269515	VOTA	Solicita digital. Tentativa [1] de [4]	6F6CD83B7CCC16CF
007221	25/10/2026 08:33:57	INFO	02269515	VOTA	Capturada a digital. Tentativa [1] de [4]	D4B368F31E80D834
007222	25/10/2026 08:33:59	INFO	02269515	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [1] de [4]	67BF7D9AD02D4A63
007223	25/10/2026 08:34:01	INFO	02269515	VOTA	Solicita digital. Tentativa [2] de [4]	3B106F1B4502EAD0
007224	25/10/2026 08:34:06	INFO	02269515	VOTA	Capturada a digital. Tentativa [2] de [4]	6ECB8FDEE5A97C54
007225	25/10/2026 08:34:08	INFO	02269515	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [2] de [4]	5DB0A925E51E4888
007226	25/10/2026 08:34:10	INFO	02269515	VOTA	Solicita digital. Tentativa [3] de [4]	7BB401AD86512A5E
007227	25/10/2026 08:34:12	INFO	02269515	VOTA	Capturada a digital. Tentativa [3] de [4]	022C08FEA22DD70C
007228	25/10/2026 08:34:14	INFO	02269515	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [3] de [4]	4BFA017DC7F77E47
007229	25/10/2026 08:34:15	INFO	02269515	VOTA	Solicita digital. Tentativa [4] de [4]	19A1F70D8AB992EC
007230	25/10/2026 08:34:18	INFO	02269515	VOTA	Capturada a digital. Tentativa [4] de [4]	BF67EE7376D53F7F
007231	25/10/2026 08:34:20	INFO	02269515	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [4] de [4]	BD7FF2F1AA59D14B
007232	25/10/2026 08:34:21	INFO	02269515	VOTA	Solicitação de dado pessoal do eleitor para habilitação manual	2C17F6FA7282A13F
007233	25/10/2026 08:34:28	INFO	02269515	VOTA	Dado digitado confere	C06E5B8414A930C8
007234	25/10/2026 08:34:28	INFO	02269515	VOTA	Solicita digital do mesário	4A7787C489CE9CA1
007235	25/10/2026 08:34:32	INFO	02269515	VOTA	Biometria do mesário 005376352410 encontrada em eleitores	DBC1790B7DF0D1FE
007236	25/10/2026 08:34:32	INFO	02269515	VOTA	Mesário 005376352410 habilitou o eleitor	F3FC280F143BD852
007237	25/10/2026 08:34:35	INFO	02269515	VOTA	Eleitor foi habilitado	0CFEC91FF9697754
007238	25/10/2026 08:34:51	INFO	02269515	VOTA	Voto confirmado para [Governador]	8E21F377FAB0ED6F
007239	25/10/2026 08:34:57	INFO	02269515	VOTA	Voto confirmado para [Presidente]	BA326CA74500EA97
007240	25/10/2026 08:34:57	INFO	02269515	VOTA	O voto do eleitor foi computado	F357C990431DF419
007241	25/10/2026 08:34:58	INFO	02269515	VOTA	Aguardando digitação do identificador do eleitor	4D1EF5635591E5D5
007242	25/10/2026 08:35:08	INFO	02269515	VOTA	Identificador do eleitor digitado pelo mesário	7E82D350CADC5339
007243	25/10/2026 08:35:08	INFO	02269515	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	A1EB02136077157C
007244	25/10/2026 08:35:08	INFO	02269515	VOTA	Foto do eleitor apresentada	AC9CB15226D42587
007245	25/10/2026 08:35:11	INFO	02269515	VOTA	Solicita digital. Tentativa [1] de [4]	739C430C1C86B22D
007246	25/10/2026 08:35:18	INFO	02269515	VOTA	Capturada a digital. Tentativa [1] de [4]	CC8B7DFE29B198AF
007247	25/10/2026 08:35:20	INFO	02269515	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [1] de [4]	58CED520E2303DD8
007248	25/10/2026 08:35:21	INFO	02269515	VOTA	Solicita digital. Tentativa [2] de [4]	FE7B0110BBE38F3F
007249	25/10/2026 08:35:24	INFO	02269515	VOTA	Capturada a digital. Tentativa [2] de [4]	F58C99A32F4F1E36
007250	25/10/2026 08:35:26	INFO	02269515	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [2] de [4]	A17957FE529D37B6
007251	25/10/2026 08:35:27	INFO	02269515	VOTA	Solicita digital. Tentativa [3] de [4]	5CAFD56821F05D83
007252	25/10/2026 08:35:33	INFO	02269515	VOTA	Capturada a digital. Tentativa [3] de [4]	8FCDA33B0A063B83
007253	25/10/2026 08:35:35	INFO	02269515	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [3] de [4]	CF30B1EAF9B7D2C9
007254	25/10/2026 08:35:37	INFO	02269515	VOTA	Solicita digital. Tentativa [4] de [4]	0775B98934641CCE
007255	25/10/2026 08:35:39	INFO	02269515	VOTA	Capturada a digital. Tentativa [4] de [4]	2AE33811A0AF1177
007256	25/10/2026 08:35:41	INFO	02269515	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [4] de [4]	4593BC0535DB6E07
007257	25/10/2026 08:35:42	INFO	02269515	VOTA	Solicitação de dado pessoal do eleitor para habilitação manual	62A106D960E93CA1
007258	25/10/2026 08:35:47	INFO	02269515	VOTA	Dado digitado confere	9E0CC8FE62578581
007259	25/10/2026 08:35:47	INFO	02269515	VOTA	Solicita digital do mesário	211884FFC503AA16
007260	25/10/2026 08:35:51	INFO	02269515	VOTA	Biometria do mesário 005376352410 encontrada em eleitores	D3C171FDC18D23A9
007261	25/10/2026 08:35:51	INFO	02269515	VOTA	Mesário 005376352410 habilitou o eleitor	93C5C15FCEFBA69A
007262	25/10/2026 08:35:53	INFO	02269515	VOTA	Eleitor foi habilitado	EDCA84406A88C4B2
007263	25/10/2026 08:36:13	INFO	02269515	VOTA	Voto confirmado para [Governador]	ECE97EAA03EC3EBC
007264	25/10/2026 08:36:18	INFO	02269515	VOTA	Voto confirmado para [Presidente]	99A50E9D734ACAA3
007265	25/10/2026 08:36:18	INFO	02269515	VOTA	O voto do eleitor foi computado	1B727F86C0478AA6
007266	25/10/2026 08:36:19	INFO	02269515	VOTA	Aguardando digitação do identificador do eleitor	3C21BBB7156C881D
007267	25/10/2026 08:36:29	INFO	02269515	VOTA	Identificador do eleitor digitado pelo mesário	95C43C3A54834D85
007268	25/10/2026 08:36:29	INFO	02269515	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	B80970870A06F3CB
007269	25/10/2026 08:36:29	INFO	02269515	VOTA	Foto do eleitor apresentada	DEBD75B963F43C4E
007270	25/10/2026 08:36:33	INFO	02269515	VOTA	Solicita digital. Tentativa [1] de [4]	C965D36E7399AD80
007271	25/10/2026 08:36:39	INFO	02269515	VOTA	Capturada a digital. Tentativa [1] de [4]	F51613EB94CC734C
007272	25/10/2026 08:36:41	INFO	02269515	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [1] de [4]	E55C5E15FB3C964B
007273	25/10/2026 08:36:42	INFO	02269515	VOTA	Solicita digital. Tentativa [2] de [4]	8E084D69AD268C8E
007274	25/10/2026 08:36:45	INFO	02269515	VOTA	Capturada a digital. Tentativa [2] de [4]	FFB7213DDFECF43B
007275	25/10/2026 08:36:47	INFO	02269515	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [2] de [4]	E11B529B87FEE895
007276	25/10/2026 08:36:49	INFO	02269515	VOTA	Solicita digital. Tentativa [3] de [4]	30631978912A463D
007277	25/10/2026 08:36:51	INFO	02269515	VOTA	Capturada a digital. Tentativa [3] de [4]	0C87E29483E41242
007278	25/10/2026 08:36:53	INFO	02269515	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [3] de [4]	0B73AB87EF90DA13
007279	25/10/2026 08:36:54	INFO	02269515	VOTA	Solicita digital. Tentativa [4] de [4]	0E1B0D07233357ED
007280	25/10/2026 08:36:56	INFO	02269515	VOTA	Capturada a digital. Tentativa [4] de [4]	A8DCC40C3F54ED1A
007281	25/10/2026 08:36:59	INFO	02269515	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [4] de [4]	DFC1AAB82F700AF6
007282	25/10/2026 08:37:00	INFO	02269515	VOTA	Solicitação de dado pessoal do eleitor para habilitação manual	FDF43024F9708327
007283	25/10/2026 08:37:05	INFO	02269515	VOTA	Dado digitado confere	66D978720C083C05
007284	25/10/2026 08:37:05	INFO	02269515	VOTA	Solicita digital do mesário	07B626976002A71D
007285	25/10/2026 08:37:09	INFO	02269515	VOTA	Biometria do mesário 005376352410 encontrada em eleitores	DF1A774F1A54CDEF
007286	25/10/2026 08:37:09	INFO	02269515	VOTA	Mesário 005376352410 habilitou o eleitor	DECA76F4AFFE78FA
007287	25/10/2026 08:37:11	INFO	02269515	VOTA	Eleitor foi habilitado	C8C0974D72C6A66D
007288	25/10/2026 08:37:26	INFO	02269515	VOTA	Voto confirmado para [Governador]	162F6FD976F76D13
007289	25/10/2026 08:37:36	INFO	02269515	VOTA	Voto confirmado para [Presidente]	5163D8E144F19C8C
007290	25/10/2026 08:37:37	INFO	02269515	VOTA	O voto do eleitor foi computado	FB368AF28AD0BF45

```

## Anexo C03 - JORDÃO - zona 0005, seção 0122

Somente mesário. Horários: 07:04:52 | 07:07:58 | 07:10:56 | 07:13:58 | 07:16:57 | 07:19:02. Intervalos em segundos: 186 | 178 | 182 | 179 | 125.

```text
C03 | JORDÃO | Zona 0005 | Seção 0122
Arquivo: o03221ac0110400050122-log.jez
Origem: raiz!logd.dat
Linhas 6919-7101, sem omitir eventos intermediários. Prefixo numérico = linha original.

006919	25/10/2026 07:03:02	INFO	02250531	VOTA	O voto do eleitor foi computado	01EEA68308C8AA3A
006920	25/10/2026 07:03:03	INFO	02250531	VOTA	Aguardando digitação do identificador do eleitor	60D56E3F822E201D
006921	25/10/2026 07:03:24	INFO	02250531	VOTA	Identificador do eleitor digitado pelo mesário	CC75A5770FC19071
006922	25/10/2026 07:03:24	INFO	02250531	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	5CBC7A488B303A93
006923	25/10/2026 07:03:24	INFO	02250531	VOTA	Foto do eleitor apresentada	05D263ED2F20C523
006924	25/10/2026 07:03:30	INFO	02250531	VOTA	Solicita digital. Tentativa [1] de [4]	5272964CE375DB91
006925	25/10/2026 07:03:36	INFO	02250531	VOTA	Capturada a digital. Tentativa [1] de [4]	9958B7F1636E6E68
006926	25/10/2026 07:03:39	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [1] de [4]	CA947F2739A71E0A
006927	25/10/2026 07:03:43	INFO	02250531	VOTA	Solicita digital. Tentativa [2] de [4]	8E98D913FCE7AE72
006928	25/10/2026 07:03:48	INFO	02250531	VOTA	Capturada a digital. Tentativa [2] de [4]	89986EEE812604A3
006929	25/10/2026 07:03:50	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [2] de [4]	BC7AC3B815D6C6FB
006930	25/10/2026 07:03:50	INFO	02250531	VOTA	Solicita digital. Tentativa [3] de [4]	332C2B3A3CA57333
006931	25/10/2026 07:03:58	INFO	02250531	VOTA	Capturada a digital. Tentativa [3] de [4]	D62A38238C180811
006932	25/10/2026 07:04:01	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [3] de [4]	B625F732FDA17B2E
006933	25/10/2026 07:04:02	INFO	02250531	VOTA	Solicita digital. Tentativa [4] de [4]	833815EF65AABA8A
006934	25/10/2026 07:04:07	INFO	02250531	VOTA	Capturada a digital. Tentativa [4] de [4]	80F98DEA3C232BD8
006935	25/10/2026 07:04:09	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [4] de [4]	CF072FF523B11672
006936	25/10/2026 07:04:14	INFO	02250531	VOTA	Solicitação de dado pessoal do eleitor para habilitação manual	45DB9F89DCFC16A8
006937	25/10/2026 07:04:18	INFO	02250531	VOTA	Dado digitado confere	E03D3B6B9D004D15
006938	25/10/2026 07:04:18	INFO	02250531	VOTA	Solicita digital do mesário	702019D05701369E
006939	25/10/2026 07:04:23	INFO	02250531	VOTA	Batimento de digitais retornou o score 10	06152ECC56007C00
006940	25/10/2026 07:04:23	INFO	02250531	VOTA	Biometria coletada não é do mesário 002226012445 (60658)	F3D43D4B1A9434E0
006941	25/10/2026 07:04:24	INFO	02250531	VOTA	Batimento de digitais retornou o score 189	988BE564A60B8A4F
006942	25/10/2026 07:04:24	INFO	02250531	VOTA	Biometria do mesário 003778002429 encontrada nos arquivos coletados (829248)	70931E9351592105
006943	25/10/2026 07:04:24	INFO	02250531	VOTA	Mesário 003778002429 habilitou o eleitor	DA937364DD87980A
006944	25/10/2026 07:04:52	INFO	02250531	VOTA	Eleitor foi habilitado	0B8227C96805BFA4
006945	25/10/2026 07:05:02	INFO	02250531	VOTA	Voto confirmado para [Governador]	AEF26F79712D626D
006946	25/10/2026 07:05:07	INFO	02250531	VOTA	Voto confirmado para [Presidente]	123A6659B0CC8948
006947	25/10/2026 07:05:07	INFO	02250531	VOTA	O voto do eleitor foi computado	674E01A3F5382FAA
006948	25/10/2026 07:05:08	INFO	02250531	VOTA	Aguardando digitação do identificador do eleitor	27F506DDA2080FCE
006949	25/10/2026 07:05:15	INFO	02250531	VOTA	Inspeção da urna iniciada	A46B609F9AC7C732
006950	25/10/2026 07:05:36	INFO	02250531	VOTA	Inspeção da urna confirmada	259B254FCD547DCF
006951	25/10/2026 07:05:46	INFO	02250531	VOTA	Inspeção da urna terminada	9EA6B019BFF3FAF3
006952	25/10/2026 07:05:46	INFO	02250531	VOTA	Aguardando digitação do identificador do eleitor	D76EC0DE903BF929
006953	25/10/2026 07:06:05	INFO	02250531	VOTA	Identificador do eleitor digitado pelo mesário	248601724F0EB5F2
006954	25/10/2026 07:06:05	INFO	02250531	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	29E9CF3986CE8032
006955	25/10/2026 07:06:05	INFO	02250531	VOTA	Foto do eleitor apresentada	D87C03C5E1F4B0B3
006956	25/10/2026 07:06:11	INFO	02250531	VOTA	Solicita digital. Tentativa [1] de [4]	1C8BB415BF1FCF2D
006957	25/10/2026 07:06:15	INFO	02250531	VOTA	Capturada a digital. Tentativa [1] de [4]	8DF59CD3227223A7
006958	25/10/2026 07:06:17	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [1] de [4]	B5613A4F73FA4402
006959	25/10/2026 07:06:27	INFO	02250531	VOTA	Solicita digital. Tentativa [2] de [4]	6D23EDBEAAB047F7
006960	25/10/2026 07:06:30	INFO	02250531	VOTA	Capturada a digital. Tentativa [2] de [4]	026F58CE07359F4F
006961	25/10/2026 07:06:32	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [2] de [4]	B6486761F19DF69C
006962	25/10/2026 07:06:35	INFO	02250531	VOTA	Solicita digital. Tentativa [3] de [4]	3BEDBEC3F3C199A1
006963	25/10/2026 07:06:39	INFO	02250531	VOTA	Capturada a digital. Tentativa [3] de [4]	9FC49780CFE0B6DD
006964	25/10/2026 07:06:41	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [3] de [4]	5308B832D4A4A406
006965	25/10/2026 07:06:44	INFO	02250531	VOTA	Solicita digital. Tentativa [4] de [4]	6574B855D8113323
006966	25/10/2026 07:06:47	INFO	02250531	VOTA	Capturada a digital. Tentativa [4] de [4]	19FE0ABC676A72F9
006967	25/10/2026 07:06:49	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [4] de [4]	BDAEC66E644D665A
006968	25/10/2026 07:06:50	INFO	02250531	VOTA	Solicitação de dado pessoal do eleitor para habilitação manual	FB579B350AD96936
006969	25/10/2026 07:07:00	INFO	02250531	VOTA	Dado digitado confere	1616CF5D007514F8
006970	25/10/2026 07:07:00	INFO	02250531	VOTA	Solicita digital do mesário	B1330A4A34279F57
006971	25/10/2026 07:07:06	INFO	02250531	VOTA	Batimento de digitais retornou o score 4	B91AE02CD9026568
006972	25/10/2026 07:07:06	INFO	02250531	VOTA	Biometria coletada não é do mesário 002226012445 (60658)	F87270FE4B1D608F
006973	25/10/2026 07:07:08	INFO	02250531	VOTA	Batimento de digitais retornou o score 131	950192423C873C44
006974	25/10/2026 07:07:08	INFO	02250531	VOTA	Biometria do mesário 003778002429 encontrada nos arquivos coletados (829248)	E58D471F0FACF9F1
006975	25/10/2026 07:07:08	INFO	02250531	VOTA	Mesário 003778002429 habilitou o eleitor	D6F817557113FB09
006976	25/10/2026 07:07:20	INFO	02250531	VOTA	Espaço livre na MI [3.4 GB]	2FD06551867276B1
006977	25/10/2026 07:07:20	INFO	02250531	VOTA	Espaço livre na MV [355.9 MB]	622EBEE5E177C971
006978	25/10/2026 07:07:20	INFO	02250531	VOTA	Espaço utilizado na MI [20.9 MB]	0BCA521459E01E5D
006979	25/10/2026 07:07:20	INFO	02250531	VOTA	Espaço utilizado na MV [21.3 MB]	D7F1DC04DA3C3DF6
006980	25/10/2026 07:07:20	INFO	02250531	VOTA	Quantidade de memória total [3.7 GB]	CAD3127F8F373647
006981	25/10/2026 07:07:20	INFO	02250531	VOTA	Quantidade de memória livre [3.3 GB]	53028970B57713DD
006982	25/10/2026 07:07:20	INFO	02250531	VOTA	Quantidade de memória usada [393.5 MB]	98A0B46DC6F80E7C
006983	25/10/2026 07:07:20	INFO	02250531	VOTA	Urna ligada conectada na rede CA em [137.86V] e na Bateria Interna com [13.54V/0A]	351ED670FFC393AA
006984	25/10/2026 07:07:58	INFO	02250531	VOTA	Eleitor foi habilitado	C7FE795C158EFB59
006985	25/10/2026 07:08:04	INFO	02250531	VOTA	Voto confirmado para [Governador]	50E590B9A5C0F50D
006986	25/10/2026 07:08:09	INFO	02250531	VOTA	Voto confirmado para [Presidente]	B538B4DD61DECF20
006987	25/10/2026 07:08:09	INFO	02250531	VOTA	O voto do eleitor foi computado	8591597DFD9B6863
006988	25/10/2026 07:08:11	INFO	02250531	VOTA	Aguardando digitação do identificador do eleitor	7660B6E5CCAF7874
006989	25/10/2026 07:08:33	INFO	02250531	VOTA	Identificador do eleitor digitado pelo mesário	3A8F11B5C851CE4F
006990	25/10/2026 07:08:33	INFO	02250531	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	6C300F613EB69820
006991	25/10/2026 07:08:33	INFO	02250531	VOTA	Foto do eleitor apresentada	6403ABC22990F026
006992	25/10/2026 07:08:41	INFO	02250531	VOTA	Solicita digital. Tentativa [1] de [4]	696A99F210F75BF9
006993	25/10/2026 07:08:44	INFO	02250531	VOTA	Capturada a digital. Tentativa [1] de [4]	F3FE41B348719AEE
006994	25/10/2026 07:08:46	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [1] de [4]	7889FC90156E6A66
006995	25/10/2026 07:08:55	INFO	02250531	VOTA	Solicita digital. Tentativa [2] de [4]	746FF035C2E9D550
006996	25/10/2026 07:09:00	INFO	02250531	VOTA	Capturada a digital. Tentativa [2] de [4]	FDF726FA039F53BB
006997	25/10/2026 07:09:02	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [2] de [4]	C532E739E620D35B
006998	25/10/2026 07:09:03	INFO	02250531	VOTA	Solicita digital. Tentativa [3] de [4]	103ED108A8D11134
006999	25/10/2026 07:09:08	INFO	02250531	VOTA	Capturada a digital. Tentativa [3] de [4]	5EB539C41601C14B
007000	25/10/2026 07:09:10	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [3] de [4]	916AC6C687EA1481
007001	25/10/2026 07:09:13	INFO	02250531	VOTA	Solicita digital. Tentativa [4] de [4]	EFCE2495DB50B218
007002	25/10/2026 07:09:15	INFO	02250531	VOTA	Capturada a digital. Tentativa [4] de [4]	CF832C1CE59F83E0
007003	25/10/2026 07:09:17	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [4] de [4]	913D5AD24A80DF57
007004	25/10/2026 07:09:19	INFO	02250531	VOTA	Solicitação de dado pessoal do eleitor para habilitação manual	0D577AA92B4E087F
007005	25/10/2026 07:09:28	INFO	02250531	VOTA	Dado digitado confere	A9EA9565CAD99135
007006	25/10/2026 07:09:28	INFO	02250531	VOTA	Solicita digital do mesário	D325F48A5C643C68
007007	25/10/2026 07:09:35	INFO	02250531	VOTA	Batimento de digitais retornou o score 6	FCEF88526D662C19
007008	25/10/2026 07:09:35	INFO	02250531	VOTA	Biometria coletada não é do mesário 002226012445 (60658)	670129FBA2696321
007009	25/10/2026 07:09:36	INFO	02250531	VOTA	Batimento de digitais retornou o score 147	BA739E75749C51B5
007010	25/10/2026 07:09:36	INFO	02250531	VOTA	Biometria do mesário 003778002429 encontrada nos arquivos coletados (829248)	9CB2CF978586FDBB
007011	25/10/2026 07:09:36	INFO	02250531	VOTA	Mesário 003778002429 habilitou o eleitor	31ECD3455AFEB349
007012	25/10/2026 07:10:56	INFO	02250531	VOTA	Eleitor foi habilitado	FE1164EDD507B6AF
007013	25/10/2026 07:11:10	INFO	02250531	VOTA	Voto confirmado para [Governador]	1ECFCF32139E9DDD
007014	25/10/2026 07:11:13	INFO	02250531	VOTA	Tecla indevida pressionada	5B3C7F69A2667F95
007015	25/10/2026 07:11:14	INFO	02250531	VOTA	Voto confirmado para [Presidente]	FDC645F8764B37FF
007016	25/10/2026 07:11:15	INFO	02250531	VOTA	O voto do eleitor foi computado	0C288798BF4B7D72
007017	25/10/2026 07:11:16	INFO	02250531	VOTA	Aguardando digitação do identificador do eleitor	82B85F52513FDC32
007018	25/10/2026 07:11:44	INFO	02250531	VOTA	Identificador do eleitor digitado pelo mesário	A0D3AE1326D96C7B
007019	25/10/2026 07:11:44	INFO	02250531	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	E59E7429FA7F3905
007020	25/10/2026 07:11:44	INFO	02250531	VOTA	Foto do eleitor apresentada	04B0DDDE7E3AF3AC
007021	25/10/2026 07:11:53	INFO	02250531	VOTA	Solicita digital. Tentativa [1] de [4]	374FA93FB3BAA061
007022	25/10/2026 07:11:57	INFO	02250531	VOTA	Capturada a digital. Tentativa [1] de [4]	1B7E4F83C55621A8
007023	25/10/2026 07:11:59	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [1] de [4]	3BFEC61404ADBB2D
007024	25/10/2026 07:12:13	INFO	02250531	VOTA	Solicita digital. Tentativa [2] de [4]	A3CB1ED01A6524F5
007025	25/10/2026 07:12:16	INFO	02250531	VOTA	Capturada a digital. Tentativa [2] de [4]	BF6F2B6DD7CEC538
007026	25/10/2026 07:12:18	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [2] de [4]	C76924BE15161F4D
007027	25/10/2026 07:12:19	INFO	02250531	VOTA	Solicita digital. Tentativa [3] de [4]	4732C29FD62C657B
007028	25/10/2026 07:12:28	INFO	02250531	VOTA	Capturada a digital. Tentativa [3] de [4]	B031999161D62EFD
007029	25/10/2026 07:12:30	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [3] de [4]	E182E2F1A979C6E3
007030	25/10/2026 07:12:31	INFO	02250531	VOTA	Solicita digital. Tentativa [4] de [4]	6902353F09378D74
007031	25/10/2026 07:12:37	INFO	02250531	VOTA	Capturada a digital. Tentativa [4] de [4]	07ED96CEBDD08584
007032	25/10/2026 07:12:39	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [4] de [4]	C292DFD94C37B96F
007033	25/10/2026 07:12:40	INFO	02250531	VOTA	Solicitação de dado pessoal do eleitor para habilitação manual	73369CBA28038CDD
007034	25/10/2026 07:12:50	INFO	02250531	VOTA	Dado digitado confere	D41521ACD5DEA871
007035	25/10/2026 07:12:50	INFO	02250531	VOTA	Solicita digital do mesário	636282AB90922427
007036	25/10/2026 07:12:55	INFO	02250531	VOTA	Batimento de digitais retornou o score 7	84C78CE34F4689BE
007037	25/10/2026 07:12:55	INFO	02250531	VOTA	Biometria coletada não é do mesário 002226012445 (60658)	5D8A97BC3BB804BB
007038	25/10/2026 07:12:57	INFO	02250531	VOTA	Batimento de digitais retornou o score 192	ACE168975041E696
007039	25/10/2026 07:12:57	INFO	02250531	VOTA	Biometria do mesário 003778002429 encontrada nos arquivos coletados (829248)	E1C7AA3FC0F0C15C
007040	25/10/2026 07:12:57	INFO	02250531	VOTA	Mesário 003778002429 habilitou o eleitor	5A5AC76D1AC3D8FE
007041	25/10/2026 07:13:58	INFO	02250531	VOTA	Eleitor foi habilitado	FE0301A20CD5E3F3
007042	25/10/2026 07:14:08	INFO	02250531	VOTA	Voto confirmado para [Governador]	7273A0643F756E70
007043	25/10/2026 07:14:13	INFO	02250531	VOTA	Voto confirmado para [Presidente]	C5073A6BA5FEA6ED
007044	25/10/2026 07:14:14	INFO	02250531	VOTA	O voto do eleitor foi computado	4164C06F4362C350
007045	25/10/2026 07:14:15	INFO	02250531	VOTA	Aguardando digitação do identificador do eleitor	6AC2269F0BE481AF
007046	25/10/2026 07:14:34	INFO	02250531	VOTA	Identificador do eleitor digitado pelo mesário	724C505AEA872ECC
007047	25/10/2026 07:14:34	INFO	02250531	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	315CB603EEAE1CF4
007048	25/10/2026 07:14:34	INFO	02250531	VOTA	Foto do eleitor apresentada	D91875E072D8F673
007049	25/10/2026 07:14:43	INFO	02250531	VOTA	Solicita digital. Tentativa [1] de [4]	AEE055005977C2C6
007050	25/10/2026 07:14:48	INFO	02250531	VOTA	Capturada a digital. Tentativa [1] de [4]	7890749B2DCA6504
007051	25/10/2026 07:14:50	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [1] de [4]	8D827583CDAC24E3
007052	25/10/2026 07:14:51	INFO	02250531	VOTA	Solicita digital. Tentativa [2] de [4]	22442262E7C6E80B
007053	25/10/2026 07:15:02	INFO	02250531	VOTA	Capturada a digital. Tentativa [2] de [4]	CA60429EE5F71505
007054	25/10/2026 07:15:05	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [2] de [4]	E50C2C07FED1FBBD
007055	25/10/2026 07:15:07	INFO	02250531	VOTA	Solicita digital. Tentativa [3] de [4]	7C33FC6E097361AB
007056	25/10/2026 07:15:10	INFO	02250531	VOTA	Capturada a digital. Tentativa [3] de [4]	1D8169FED0B9F7E7
007057	25/10/2026 07:15:12	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [3] de [4]	D5FF29BC0892C4AE
007058	25/10/2026 07:15:17	INFO	02250531	VOTA	Solicita digital. Tentativa [4] de [4]	9322F389C372E382
007059	25/10/2026 07:15:29	INFO	02250531	VOTA	Capturada a digital. Tentativa [4] de [4]	ADBB04CD3372766F
007060	25/10/2026 07:15:32	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [4] de [4]	966AD2F8B0865FED
007061	25/10/2026 07:15:39	INFO	02250531	VOTA	Solicitação de dado pessoal do eleitor para habilitação manual	0811A972C95A0084
007062	25/10/2026 07:15:52	INFO	02250531	VOTA	Dado digitado confere	9AFEAF6A0E696DCC
007063	25/10/2026 07:15:52	INFO	02250531	VOTA	Solicita digital do mesário	E977FFC7EF2C07BE
007064	25/10/2026 07:16:49	INFO	02250531	VOTA	Solicita digital do mesário	9A64942B18BC52EF
007065	25/10/2026 07:16:54	INFO	02250531	VOTA	Batimento de digitais retornou o score 4	53A2DB954C7A23CC
007066	25/10/2026 07:16:54	INFO	02250531	VOTA	Biometria coletada não é do mesário 002226012445 (60658)	FF4CB3AD04E36001
007067	25/10/2026 07:16:55	INFO	02250531	VOTA	Batimento de digitais retornou o score 161	3C9F4EAEE519134A
007068	25/10/2026 07:16:56	INFO	02250531	VOTA	Biometria do mesário 003778002429 encontrada nos arquivos coletados (829248)	D51E5A50BDBC59E1
007069	25/10/2026 07:16:56	INFO	02250531	VOTA	Mesário 003778002429 habilitou o eleitor	6832AD7636BC2DC6
007070	25/10/2026 07:16:57	INFO	02250531	VOTA	Eleitor foi habilitado	D2E061BF02AF7947
007071	25/10/2026 07:17:05	INFO	02250531	VOTA	Voto confirmado para [Governador]	EE1C02C4E07C80B0
007072	25/10/2026 07:17:16	INFO	02250531	VOTA	Voto confirmado para [Presidente]	0C5189AA07B7ED15
007073	25/10/2026 07:17:17	INFO	02250531	VOTA	O voto do eleitor foi computado	F276D0E429D023F0
007074	25/10/2026 07:17:18	INFO	02250531	VOTA	Aguardando digitação do identificador do eleitor	DFEE58D05714D982
007075	25/10/2026 07:17:45	INFO	02250531	VOTA	Identificador do eleitor digitado pelo mesário	136A4CD7F82EAB16
007076	25/10/2026 07:17:45	INFO	02250531	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	8A5171D623C38412
007077	25/10/2026 07:17:45	INFO	02250531	VOTA	Foto do eleitor apresentada	5A7C5E422FADCF2A
007078	25/10/2026 07:17:50	INFO	02250531	VOTA	Solicita digital. Tentativa [1] de [4]	DA5C20824E7692DC
007079	25/10/2026 07:17:53	INFO	02250531	VOTA	Capturada a digital. Tentativa [1] de [4]	630BCB26B06F8E00
007080	25/10/2026 07:17:56	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [1] de [4]	D4F568A9CB286BFB
007081	25/10/2026 07:18:01	INFO	02250531	VOTA	Solicita digital. Tentativa [2] de [4]	19DD2849035308F5
007082	25/10/2026 07:18:05	INFO	02250531	VOTA	Capturada a digital. Tentativa [2] de [4]	A84E27CDFE614D50
007083	25/10/2026 07:18:07	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [2] de [4]	2225F58701050FF3
007084	25/10/2026 07:18:13	INFO	02250531	VOTA	Solicita digital. Tentativa [3] de [4]	EAB0B867B809EBEC
007085	25/10/2026 07:18:15	INFO	02250531	VOTA	Capturada a digital. Tentativa [3] de [4]	BA010ABD213497D2
007086	25/10/2026 07:18:18	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [3] de [4]	F90E71E5268BF230
007087	25/10/2026 07:18:19	INFO	02250531	VOTA	Solicita digital. Tentativa [4] de [4]	0FE6035CE03B59FF
007088	25/10/2026 07:18:23	INFO	02250531	VOTA	Capturada a digital. Tentativa [4] de [4]	72B6CAEF0D7486DD
007089	25/10/2026 07:18:25	INFO	02250531	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [4] de [4]	D45A63BB4EAC9206
007090	25/10/2026 07:18:27	INFO	02250531	VOTA	Solicitação de dado pessoal do eleitor para habilitação manual	1BE4337AB9BF88FC
007091	25/10/2026 07:18:37	INFO	02250531	VOTA	Dado digitado confere	3669F91DF46B6139
007092	25/10/2026 07:18:37	INFO	02250531	VOTA	Solicita digital do mesário	10256CBBFAA24D95
007093	25/10/2026 07:18:42	INFO	02250531	VOTA	Batimento de digitais retornou o score 3	AD0761D69DA56D7B
007094	25/10/2026 07:18:42	INFO	02250531	VOTA	Biometria coletada não é do mesário 002226012445 (60658)	F303CD9A85349A78
007095	25/10/2026 07:18:44	INFO	02250531	VOTA	Batimento de digitais retornou o score 141	AFD70D17D3FE123B
007096	25/10/2026 07:18:44	INFO	02250531	VOTA	Biometria do mesário 003778002429 encontrada nos arquivos coletados (829248)	7E74F7717E24A304
007097	25/10/2026 07:18:44	INFO	02250531	VOTA	Mesário 003778002429 habilitou o eleitor	A8E414E52B98412D
007098	25/10/2026 07:19:02	INFO	02250531	VOTA	Eleitor foi habilitado	A510A32F61900F02
007099	25/10/2026 07:19:09	INFO	02250531	VOTA	Voto confirmado para [Governador]	9EBFA2F1B3115ED5
007100	25/10/2026 07:19:13	INFO	02250531	VOTA	Voto confirmado para [Presidente]	A423A1D88248AD07
007101	25/10/2026 07:19:13	INFO	02250531	VOTA	O voto do eleitor foi computado	607C41C964432426

```

## Anexo C04 - RIO BRANCO - zona 0001, seção 0824

Mesário ou ano de nascimento. Horários: 10:51:27 | 10:52:30 | 10:55:14 | 10:56:30 | 10:57:14 | 10:58:11 | 10:59:09 | 11:00:04. Intervalos em segundos: 63 | 164 | 76 | 44 | 57 | 58 | 55.

```text
C04 | RIO BRANCO | Zona 0001 | Seção 0824
Arquivo: o03221ac0139200010824-log.jez
Origem: raiz!logd.dat
Linhas 8028-8125, sem omitir eventos intermediários. Prefixo numérico = linha original.

008028	25/10/2026 10:50:48	INFO	02045176	VOTA	O voto do eleitor foi computado	D90CE0DFE4955E68
008029	25/10/2026 10:50:50	INFO	02045176	VOTA	Aguardando digitação do identificador do eleitor	F2B26030C378E2E9
008030	25/10/2026 10:51:20	INFO	02045176	VOTA	Identificador do eleitor digitado pelo mesário	CE3C84D15119707B
008031	25/10/2026 10:51:20	INFO	02045176	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	664CBA3A357B5B5F
008032	25/10/2026 10:51:25	INFO	02045176	VOTA	Ano de nascimento digitado é igual ao do cadastro	CB7A0926AB368BFF
008033	25/10/2026 10:51:27	INFO	02045176	VOTA	Eleitor foi habilitado	143DDBCB4F25B3C2
008034	25/10/2026 10:51:39	INFO	02045176	VOTA	Voto confirmado para [Governador]	6B8EFF18A14E65CA
008035	25/10/2026 10:51:42	INFO	02045176	VOTA	Voto confirmado para [Presidente]	344DC2DF0F6322BA
008036	25/10/2026 10:51:43	INFO	02045176	VOTA	O voto do eleitor foi computado	3B8C297B87262007
008037	25/10/2026 10:51:44	INFO	02045176	VOTA	Aguardando digitação do identificador do eleitor	191804602BFE9ECF
008038	25/10/2026 10:52:17	INFO	02045176	VOTA	Identificador do eleitor digitado pelo mesário	706B0E6983CE1FCD
008039	25/10/2026 10:52:17	INFO	02045176	VOTA	Identificador digitado pelo mesário foi: (CPF)	BDCE5D66BAC791B2
008040	25/10/2026 10:52:28	INFO	02045176	VOTA	Ano de nascimento digitado é igual ao do cadastro	3D7AA3763A4900BF
008041	25/10/2026 10:52:30	INFO	02045176	VOTA	Eleitor foi habilitado	989064B0586F5EC3
008042	25/10/2026 10:52:37	INFO	02045176	VOTA	Tecla indevida pressionada	C93EDD9B68F9B3E7
008043	25/10/2026 10:52:43	INFO	02045176	VOTA	Voto confirmado para [Governador]	E52128052C5AD0EB
008044	25/10/2026 10:52:48	INFO	02045176	VOTA	Voto confirmado para [Presidente]	4076B7B2723404A8
008045	25/10/2026 10:52:48	INFO	02045176	VOTA	O voto do eleitor foi computado	EAAE14FDBF1D3DAD
008046	25/10/2026 10:52:49	INFO	02045176	VOTA	Aguardando digitação do identificador do eleitor	3ACB48737726A8D9
008047	25/10/2026 10:53:18	INFO	02045176	VOTA	Identificador do eleitor digitado pelo mesário	3C25987DBE43B565
008048	25/10/2026 10:53:18	INFO	02045176	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	C0951D15C7C01AAC
008049	25/10/2026 10:53:18	INFO	02045176	VOTA	Foto do eleitor apresentada	73A674567247641D
008050	25/10/2026 10:53:20	INFO	02045176	VOTA	Solicita digital. Tentativa [1] de [4]	469D1076E5666EEC
008051	25/10/2026 10:53:52	INFO	02045176	VOTA	Timeout de reconhecimento do dedo. Tentativa [1] de [4]	D8A2BEA8DC4FB622
008052	25/10/2026 10:54:12	INFO	02045176	VOTA	Solicita digital. Tentativa [2] de [4]	97D2103A20F62229
008053	25/10/2026 10:54:30	INFO	02045176	VOTA	Timeout de reconhecimento do dedo. Tentativa [2] de [4]	ECA8058600DE124F
008054	25/10/2026 10:54:33	INFO	02045176	VOTA	Solicita digital. Tentativa [3] de [4]	DAEF6C2F47BF79E6
008055	25/10/2026 10:54:37	INFO	02045176	VOTA	Capturada a digital. Tentativa [3] de [4]	E57DAB4E68D8B7DC
008056	25/10/2026 10:54:39	INFO	02045176	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [3] de [4]	9A3442AEF32348A7
008057	25/10/2026 10:54:40	INFO	02045176	VOTA	Solicita digital. Tentativa [4] de [4]	05A10B5F17169FD1
008058	25/10/2026 10:54:52	INFO	02045176	VOTA	Capturada a digital. Tentativa [4] de [4]	0187EC5530B1D035
008059	25/10/2026 10:54:55	INFO	02045176	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [4] de [4]	23527A5F014C7939
008060	25/10/2026 10:54:57	INFO	02045176	VOTA	Solicitação de dado pessoal do eleitor para habilitação manual	425456D4B0B6A21F
008061	25/10/2026 10:55:02	INFO	02045176	VOTA	Dado digitado confere	98D961AAB5721CD1
008062	25/10/2026 10:55:02	INFO	02045176	VOTA	Solicita digital do mesário	E699FA730186ECA7
008063	25/10/2026 10:55:06	INFO	02045176	VOTA	Biometria coletada não é do mesário 007660912402	819D58E5EDD4DF5B
008064	25/10/2026 10:55:07	INFO	02045176	VOTA	Batimento de digitais retornou o score 4	C0CF4F7AF6FA27F9
008065	25/10/2026 10:55:07	INFO	02045176	VOTA	Biometria coletada não é do mesário 001900442470 (222904)	3B88FC7F30E37A15
008066	25/10/2026 10:55:09	INFO	02045176	VOTA	Batimento de digitais retornou o score 4	BBEC15126CFB9028
008067	25/10/2026 10:55:09	INFO	02045176	VOTA	Biometria coletada não é do mesário 006922392429 (751645)	E0B686265DA6D8AF
008068	25/10/2026 10:55:10	INFO	02045176	VOTA	Batimento de digitais retornou o score 4	73EB4C41A2F90726
008069	25/10/2026 10:55:10	INFO	02045176	VOTA	Biometria coletada não é do mesário 007909832470 (142428)	8042137F7FC33E6F
008070	25/10/2026 10:55:10	INFO	02045176	VOTA	Capturada a digital do mesário	3539A9250F7922DA
008071	25/10/2026 10:55:10	INFO	02045176	VOTA	Não encontrou digital coletada em nenhum dos arquivos, vai salvar a digital em novo arquivo.	4D4DBFD499E5556E
008072	25/10/2026 10:55:14	INFO	02045176	VOTA	Eleitor foi habilitado	2E7DC4B7A77276F5
008073	25/10/2026 10:55:25	INFO	02045176	VOTA	Tecla indevida pressionada	94D3ED01DD2B2D47
008074	25/10/2026 10:55:28	INFO	02045176	VOTA	Voto confirmado para [Governador]	72060C025EA73594
008075	25/10/2026 10:55:33	INFO	02045176	VOTA	Voto confirmado para [Presidente]	7E4D6EC4C10C4526
008076	25/10/2026 10:55:33	INFO	02045176	VOTA	O voto do eleitor foi computado	8B5A398CECD219D1
008077	25/10/2026 10:55:34	INFO	02045176	VOTA	Aguardando digitação do identificador do eleitor	C45FDDFFEE26FEDC
008078	25/10/2026 10:55:41	INFO	02045176	VOTA	Inspeção da urna iniciada	9D75D8EA3F693352
008079	25/10/2026 10:55:52	INFO	02045176	VOTA	Inspeção da urna confirmada	F44CE7342897ACA6
008080	25/10/2026 10:56:03	INFO	02045176	VOTA	Inspeção da urna terminada	FA635C306739462B
008081	25/10/2026 10:56:03	INFO	02045176	VOTA	Aguardando digitação do identificador do eleitor	106A48FA0301531C
008082	25/10/2026 10:56:16	INFO	02045176	VOTA	Identificador do eleitor digitado pelo mesário	322E3816DBB875B5
008083	25/10/2026 10:56:16	INFO	02045176	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	56D528AE43CAD9C7
008084	25/10/2026 10:56:28	INFO	02045176	VOTA	Ano de nascimento digitado é igual ao do cadastro	6A8D4D085C15E9E0
008085	25/10/2026 10:56:30	INFO	02045176	VOTA	Eleitor foi habilitado	BBEB19C8543208D8
008086	25/10/2026 10:56:36	INFO	02045176	VOTA	Tecla indevida pressionada	0CD2E3DEE3746AEF
008087	25/10/2026 10:56:38	INFO	02045176	VOTA	Voto confirmado para [Governador]	DF74AEBD0A3F385A
008088	25/10/2026 10:56:41	INFO	02045176	VOTA	Voto confirmado para [Presidente]	0D6FEDB6302DEB9F
008089	25/10/2026 10:56:41	INFO	02045176	VOTA	O voto do eleitor foi computado	AE6FEE1182CB56E3
008090	25/10/2026 10:56:42	INFO	02045176	VOTA	Aguardando digitação do identificador do eleitor	48A25BFEF0B805B0
008091	25/10/2026 10:57:05	INFO	02045176	VOTA	Identificador do eleitor digitado pelo mesário	DFCD71148FB3C4E3
008092	25/10/2026 10:57:05	INFO	02045176	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	BA45695AB7FA6B0E
008093	25/10/2026 10:57:12	INFO	02045176	VOTA	Ano de nascimento digitado é igual ao do cadastro	8ADC14CBDDD97B0A
008094	25/10/2026 10:57:14	INFO	02045176	VOTA	Eleitor foi habilitado	F6863C25AFBAA150
008095	25/10/2026 10:57:28	INFO	02045176	VOTA	Voto confirmado para [Governador]	50925BDDFECE7EB2
008096	25/10/2026 10:57:31	INFO	02045176	VOTA	Voto confirmado para [Presidente]	C361A47E550309BE
008097	25/10/2026 10:57:32	INFO	02045176	VOTA	O voto do eleitor foi computado	87560E57955C134F
008098	25/10/2026 10:57:33	INFO	02045176	VOTA	Aguardando digitação do identificador do eleitor	A16D1AD43DDB2267
008099	25/10/2026 10:58:02	INFO	02045176	VOTA	Identificador do eleitor digitado pelo mesário	0CA235F35857C685
008100	25/10/2026 10:58:02	INFO	02045176	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	3D37AB0F3344588F
008101	25/10/2026 10:58:07	INFO	02045176	VOTA	Ano de nascimento digitado é igual ao do cadastro	E4EDF4543C602950
008102	25/10/2026 10:58:11	INFO	02045176	VOTA	Eleitor foi habilitado	404332838AAFA8DD
008103	25/10/2026 10:58:20	INFO	02045176	VOTA	Tecla indevida pressionada	EF990C47478C6C82
008104	25/10/2026 10:58:21	INFO	02045176	VOTA	Voto confirmado para [Governador]	0507BC315BAB3B96
008105	25/10/2026 10:58:24	INFO	02045176	VOTA	Tecla indevida pressionada	CF6B781EE2C83E4C
008106	25/10/2026 10:58:25	INFO	02045176	VOTA	Voto confirmado para [Presidente]	40938370931698C8
008107	25/10/2026 10:58:25	INFO	02045176	VOTA	O voto do eleitor foi computado	6F41C8DB098E408D
008108	25/10/2026 10:58:26	INFO	02045176	VOTA	Aguardando digitação do identificador do eleitor	94FF52D260C01D7C
008109	25/10/2026 10:58:54	INFO	02045176	VOTA	Identificador do eleitor digitado pelo mesário	9C2ECBB49D82AFCA
008110	25/10/2026 10:59:00	INFO	02045176	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	943BF84B86DCA1F8
008111	25/10/2026 10:59:07	INFO	02045176	VOTA	Ano de nascimento digitado é igual ao do cadastro	540C7A4278D4BB64
008112	25/10/2026 10:59:09	INFO	02045176	VOTA	Eleitor foi habilitado	2C55D230F23ECA5D
008113	25/10/2026 10:59:20	INFO	02045176	VOTA	Voto confirmado para [Governador]	9927798A036244EA
008114	25/10/2026 10:59:24	INFO	02045176	VOTA	Voto confirmado para [Presidente]	96B619589FF2E3EB
008115	25/10/2026 10:59:25	INFO	02045176	VOTA	O voto do eleitor foi computado	7D40D66DBA01AB0F
008116	25/10/2026 10:59:26	INFO	02045176	VOTA	Aguardando digitação do identificador do eleitor	C647BF7427345139
008117	25/10/2026 10:59:55	INFO	02045176	VOTA	Identificador do eleitor digitado pelo mesário	59AFA6A2D83C6C87
008118	25/10/2026 10:59:55	INFO	02045176	VOTA	Identificador digitado pelo mesário foi: (CPF)	E6F6C2CC1197DD99
008119	25/10/2026 11:00:02	INFO	02045176	VOTA	Ano de nascimento digitado é igual ao do cadastro	9B32A04AB841B4A3
008120	25/10/2026 11:00:04	INFO	02045176	VOTA	Eleitor foi habilitado	69CD25BD78BCCFE2
008121	25/10/2026 11:00:16	INFO	02045176	VOTA	Tecla indevida pressionada	C16424B129108F21
008122	25/10/2026 11:00:17	INFO	02045176	VOTA	Voto confirmado para [Governador]	5215FC2503121866
008123	25/10/2026 11:00:21	INFO	02045176	VOTA	Tecla indevida pressionada	9166BCD93095A06F
008124	25/10/2026 11:00:22	INFO	02045176	VOTA	Voto confirmado para [Presidente]	802F324FC571A376
008125	25/10/2026 11:00:22	INFO	02045176	VOTA	O voto do eleitor foi computado	D63678AB6D8FA584

```

## Anexo C05 - RIO BRANCO - zona 0001, seção 0830

Mesário ou ano de nascimento. Horários: 10:12:12 | 10:12:55 | 10:13:51. Intervalos em segundos: 43 | 56.

```text
C05 | RIO BRANCO | Zona 0001 | Seção 0830
Arquivo: o03221ac0139200010830-log.jez
Origem: raiz!logd.dat
Linhas 7790-7816, sem omitir eventos intermediários. Prefixo numérico = linha original.

007790	25/10/2026 10:11:43	INFO	02037108	VOTA	O voto do eleitor foi computado	D644FDC3EB4D704E
007791	25/10/2026 10:11:45	INFO	02037108	VOTA	Aguardando digitação do identificador do eleitor	F7A93E43CB94DF02
007792	25/10/2026 10:12:00	INFO	02037108	VOTA	Identificador do eleitor digitado pelo mesário	976EBFB0BFD021EB
007793	25/10/2026 10:12:00	INFO	02037108	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	D55B47512BD01A41
007794	25/10/2026 10:12:09	INFO	02037108	VOTA	Ano de nascimento digitado é igual ao do cadastro	43E793B24E9231C7
007795	25/10/2026 10:12:12	INFO	02037108	VOTA	Eleitor foi habilitado	571BC3311E18F739
007796	25/10/2026 10:12:19	INFO	02037108	VOTA	Tecla indevida pressionada	BEF9E6B398AFF7D4
007797	25/10/2026 10:12:19	INFO	02037108	VOTA	Voto confirmado para [Governador]	15B06229D962C593
007798	25/10/2026 10:12:23	INFO	02037108	VOTA	Voto confirmado para [Presidente]	B13C45BCE6F2B5F0
007799	25/10/2026 10:12:23	INFO	02037108	VOTA	O voto do eleitor foi computado	D8E7D3B757CAA7E2
007800	25/10/2026 10:12:24	INFO	02037108	VOTA	Aguardando digitação do identificador do eleitor	27B715E844D20CBE
007801	25/10/2026 10:12:45	INFO	02037108	VOTA	Identificador do eleitor digitado pelo mesário	50F23082E41AE0C8
007802	25/10/2026 10:12:45	INFO	02037108	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	3793138A6ADE9BD6
007803	25/10/2026 10:12:51	INFO	02037108	VOTA	Ano de nascimento digitado é igual ao do cadastro	43FF29696C851E44
007804	25/10/2026 10:12:55	INFO	02037108	VOTA	Eleitor foi habilitado	A89C459A5FDAA9E1
007805	25/10/2026 10:13:03	INFO	02037108	VOTA	Tecla indevida pressionada	D1435263DEEA3A6D
007806	25/10/2026 10:13:07	INFO	02037108	VOTA	Voto confirmado para [Governador]	D60C86EFA292D861
007807	25/10/2026 10:13:12	INFO	02037108	VOTA	Voto confirmado para [Presidente]	46451D936CE48018
007808	25/10/2026 10:13:13	INFO	02037108	VOTA	O voto do eleitor foi computado	129EEEA64A1B0B5C
007809	25/10/2026 10:13:14	INFO	02037108	VOTA	Aguardando digitação do identificador do eleitor	F9BCF6BF2C579E50
007810	25/10/2026 10:13:41	INFO	02037108	VOTA	Identificador do eleitor digitado pelo mesário	F997450E8956929B
007811	25/10/2026 10:13:41	INFO	02037108	VOTA	Identificador digitado pelo mesário foi: (CPF)	810BC6EA1BCB4358
007812	25/10/2026 10:13:49	INFO	02037108	VOTA	Ano de nascimento digitado é igual ao do cadastro	2A097530767921A1
007813	25/10/2026 10:13:51	INFO	02037108	VOTA	Eleitor foi habilitado	636EE55E77F3C385
007814	25/10/2026 10:14:02	INFO	02037108	VOTA	Voto confirmado para [Governador]	DC85DB2D80DDE40D
007815	25/10/2026 10:14:06	INFO	02037108	VOTA	Voto confirmado para [Presidente]	FA79E923D38C8838
007816	25/10/2026 10:14:06	INFO	02037108	VOTA	O voto do eleitor foi computado	F4B824792A7A1B00

```

## Anexo C06 - RIO BRANCO - zona 0009, seção 0443

Mesário ou ano de nascimento. Horários: 13:29:11 | 13:29:41 | 13:30:49. Intervalos em segundos: 30 | 68.

```text
C06 | RIO BRANCO | Zona 0009 | Seção 0443
Arquivo: o03221ac0139200090443-log.jez
Origem: raiz!logd.dat
Linhas 9808-9832, sem omitir eventos intermediários. Prefixo numérico = linha original.

009808	25/10/2026 13:28:55	INFO	02286933	VOTA	O voto do eleitor foi computado	7ECCAA3012996260
009809	25/10/2026 13:28:56	INFO	02286933	VOTA	Aguardando digitação do identificador do eleitor	727E49DD4D807C6F
009810	25/10/2026 13:29:04	INFO	02286933	VOTA	Identificador do eleitor digitado pelo mesário	6EC4591CD7E48618
009811	25/10/2026 13:29:04	INFO	02286933	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	2424D7565CAC3EAE
009812	25/10/2026 13:29:10	INFO	02286933	VOTA	Ano de nascimento digitado é igual ao do cadastro	721D14756057E680
009813	25/10/2026 13:29:11	INFO	02286933	VOTA	Eleitor foi habilitado	33210B65E49FE265
009814	25/10/2026 13:29:16	INFO	02286933	VOTA	Voto confirmado para [Governador]	41364CE751A87C0E
009815	25/10/2026 13:29:20	INFO	02286933	VOTA	Voto confirmado para [Presidente]	81CBC9274E8213B4
009816	25/10/2026 13:29:21	INFO	02286933	VOTA	O voto do eleitor foi computado	028567514995196E
009817	25/10/2026 13:29:22	INFO	02286933	VOTA	Aguardando digitação do identificador do eleitor	58FCFC309168DA56
009818	25/10/2026 13:29:35	INFO	02286933	VOTA	Identificador do eleitor digitado pelo mesário	2A87D62A1D955676
009819	25/10/2026 13:29:35	INFO	02286933	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	FA88C94843003E3F
009820	25/10/2026 13:29:40	INFO	02286933	VOTA	Ano de nascimento digitado é igual ao do cadastro	7BAEF66F3BF468C9
009821	25/10/2026 13:29:41	INFO	02286933	VOTA	Eleitor foi habilitado	2094C0E6E3178627
009822	25/10/2026 13:30:16	INFO	02286933	VOTA	Voto confirmado para [Governador]	1B130AB59DEA4AAF
009823	25/10/2026 13:30:19	INFO	02286933	VOTA	Voto confirmado para [Presidente]	DF94FDC07050FCBA
009824	25/10/2026 13:30:20	INFO	02286933	VOTA	O voto do eleitor foi computado	4FE2D722D5B51FE8
009825	25/10/2026 13:30:21	INFO	02286933	VOTA	Aguardando digitação do identificador do eleitor	3F0F6008635AF899
009826	25/10/2026 13:30:42	INFO	02286933	VOTA	Identificador do eleitor digitado pelo mesário	BF4E74039FCC22EE
009827	25/10/2026 13:30:42	INFO	02286933	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	E8AF19E84DA31E29
009828	25/10/2026 13:30:48	INFO	02286933	VOTA	Ano de nascimento digitado é igual ao do cadastro	7473970B23A1105B
009829	25/10/2026 13:30:49	INFO	02286933	VOTA	Eleitor foi habilitado	B9A62D4981910C3F
009830	25/10/2026 13:31:17	INFO	02286933	VOTA	Voto confirmado para [Governador]	2CD3919A69FD74AD
009831	25/10/2026 13:31:21	INFO	02286933	VOTA	Voto confirmado para [Presidente]	2EBD252BD2E001E5
009832	25/10/2026 13:31:22	INFO	02286933	VOTA	O voto do eleitor foi computado	D43510B7FA221665

```

## Anexo C07 - PLÁCIDO DE CASTRO - zona 0008, seção 0024

Somente mesário. Horários: 09:12:46 | 09:14:27 | 09:18:30 | 09:20:43 | 09:28:31. Intervalos em segundos: 101 | 243 | 133 | 468.

```text
C07 | PLÁCIDO DE CASTRO | Zona 0008 | Seção 0024
Arquivo: o03221ac0151100080024-log.jez
Origem: raiz!logd.dat
Linhas 6874-7014, sem omitir eventos intermediários. Prefixo numérico = linha original.

006874	25/10/2026 09:10:38	INFO	02048061	VOTA	O voto do eleitor foi computado	4E5444422FFE3463
006875	25/10/2026 09:10:39	INFO	02048061	VOTA	Aguardando digitação do identificador do eleitor	44506E6AB066850C
006876	25/10/2026 09:11:57	INFO	02048061	VOTA	Identificador do eleitor digitado pelo mesário	2CBB4CF68B5F1EDE
006877	25/10/2026 09:11:57	INFO	02048061	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	9E96129BD54B1CB9
006878	25/10/2026 09:11:57	INFO	02048061	VOTA	Solicita digital. Tentativa [1] de [4]	2911092F794CA3DC
006879	25/10/2026 09:12:11	INFO	02048061	VOTA	Capturada a digital. Tentativa [1] de [4]	02A1CB9F06395A61
006880	25/10/2026 09:12:13	INFO	02048061	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [1] de [4]	E71F67B898D89704
006881	25/10/2026 09:12:15	INFO	02048061	VOTA	Solicita digital. Tentativa [2] de [4]	648F123C581A0FE7
006882	25/10/2026 09:12:19	INFO	02048061	VOTA	Capturada a digital. Tentativa [2] de [4]	FBC94066AF66DD17
006883	25/10/2026 09:12:21	INFO	02048061	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [2] de [4]	AA75BA3A3897855C
006884	25/10/2026 09:12:23	INFO	02048061	VOTA	Solicita digital. Tentativa [3] de [4]	A3B5D7BE9955BBE8
006885	25/10/2026 09:12:26	INFO	02048061	VOTA	Capturada a digital. Tentativa [3] de [4]	9C8F8C306531E2D8
006886	25/10/2026 09:12:28	INFO	02048061	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [3] de [4]	499C69239A57DDB9
006887	25/10/2026 09:12:29	INFO	02048061	VOTA	Solicita digital. Tentativa [4] de [4]	1FB8B82CDD0B3353
006888	25/10/2026 09:12:32	INFO	02048061	VOTA	Capturada a digital. Tentativa [4] de [4]	FD48258BDF2C3AAC
006889	25/10/2026 09:12:34	INFO	02048061	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [4] de [4]	C0C5F9C9009DA927
006890	25/10/2026 09:12:35	INFO	02048061	VOTA	Solicitação de dado pessoal do eleitor para habilitação manual	202643840DCCB073
006891	25/10/2026 09:12:39	INFO	02048061	VOTA	Dado digitado confere	B61A3B1540786152
006892	25/10/2026 09:12:39	INFO	02048061	VOTA	Solicita digital do mesário	215F79EB06F24946
006893	25/10/2026 09:12:44	INFO	02048061	VOTA	Batimento de digitais retornou o score 83	DCFF10E6826EC17D
006894	25/10/2026 09:12:44	INFO	02048061	VOTA	Biometria do mesário 004837732488 encontrada nos arquivos coletados (700013)	A9EA34A1306E89B6
006895	25/10/2026 09:12:44	INFO	02048061	VOTA	Mesário 004837732488 habilitou o eleitor	F6C33CEDBC1E3237
006896	25/10/2026 09:12:46	INFO	02048061	VOTA	Eleitor foi habilitado	2F66B5FC6E8B899F
006897	25/10/2026 09:12:49	INFO	02048061	VOTA	Tecla indevida pressionada	6F7BCECF146205DB
006898	25/10/2026 09:12:51	INFO	02048061	VOTA	Voto confirmado para [Governador]	E00293D59EE5D174
006899	25/10/2026 09:12:54	INFO	02048061	VOTA	Voto confirmado para [Presidente]	C61C794D129FB17D
006900	25/10/2026 09:12:55	INFO	02048061	VOTA	O voto do eleitor foi computado	15F34FBCC45BFEA1
006901	25/10/2026 09:12:56	INFO	02048061	VOTA	Aguardando digitação do identificador do eleitor	E013679CFEEFB83D
006902	25/10/2026 09:13:34	INFO	02048061	VOTA	Identificador do eleitor digitado pelo mesário	D495DB41AC138B78
006903	25/10/2026 09:13:34	INFO	02048061	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	02CF106AEC973860
006904	25/10/2026 09:13:35	INFO	02048061	VOTA	Foto do eleitor apresentada	BD6A9D48327BF487
006905	25/10/2026 09:13:36	INFO	02048061	VOTA	Solicita digital. Tentativa [1] de [4]	8D8ABAB0D383DCE8
006906	25/10/2026 09:13:41	INFO	02048061	VOTA	Capturada a digital. Tentativa [1] de [4]	F8C1AC0DBEE53E6B
006907	25/10/2026 09:13:43	INFO	02048061	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [1] de [4]	8AE6FC45AABD54EC
006908	25/10/2026 09:13:45	INFO	02048061	VOTA	Solicita digital. Tentativa [2] de [4]	D3A7CFA14836435E
006909	25/10/2026 09:13:52	INFO	02048061	VOTA	Capturada a digital. Tentativa [2] de [4]	3E187E73E6F29242
006910	25/10/2026 09:13:54	INFO	02048061	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [2] de [4]	7D95C31C0FD81ACD
006911	25/10/2026 09:13:55	INFO	02048061	VOTA	Solicita digital. Tentativa [3] de [4]	5A42906D993D20D7
006912	25/10/2026 09:14:02	INFO	02048061	VOTA	Capturada a digital. Tentativa [3] de [4]	D0216D9F499D8408
006913	25/10/2026 09:14:05	INFO	02048061	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [3] de [4]	43F793516AEC42C9
006914	25/10/2026 09:14:06	INFO	02048061	VOTA	Solicita digital. Tentativa [4] de [4]	78788CDBC68BD193
006915	25/10/2026 09:14:11	INFO	02048061	VOTA	Capturada a digital. Tentativa [4] de [4]	676F8B1A8B5CAD97
006916	25/10/2026 09:14:13	INFO	02048061	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [4] de [4]	CB12819672680986
006917	25/10/2026 09:14:15	INFO	02048061	VOTA	Solicitação de dado pessoal do eleitor para habilitação manual	2498C46DC59B3433
006918	25/10/2026 09:14:20	INFO	02048061	VOTA	Dado digitado confere	F14A77FF550C7EC3
006919	25/10/2026 09:14:20	INFO	02048061	VOTA	Solicita digital do mesário	05D2AA57971BDC83
006920	25/10/2026 09:14:25	INFO	02048061	VOTA	Batimento de digitais retornou o score 44	0C569C2962E70723
006921	25/10/2026 09:14:25	INFO	02048061	VOTA	Biometria do mesário 004837732488 encontrada nos arquivos coletados (700013)	35364D50D76D8F04
006922	25/10/2026 09:14:25	INFO	02048061	VOTA	Mesário 004837732488 habilitou o eleitor	39FC0526E60AFBE1
006923	25/10/2026 09:14:27	INFO	02048061	VOTA	Eleitor foi habilitado	0C1D37731E1D95E9
006924	25/10/2026 09:14:38	INFO	02048061	VOTA	Voto confirmado para [Governador]	82FDEA6C8439204E
006925	25/10/2026 09:14:47	INFO	02048061	VOTA	Voto confirmado para [Presidente]	0D41829E9E21D0BE
006926	25/10/2026 09:14:48	INFO	02048061	VOTA	O voto do eleitor foi computado	262150C4C58E415E
006927	25/10/2026 09:14:49	INFO	02048061	VOTA	Aguardando digitação do identificador do eleitor	AF7634DDAC3A0FA5
006928	25/10/2026 09:16:05	INFO	02048061	VOTA	Espaço livre na MI [3.4 GB]	1626A7E79596F12A
006929	25/10/2026 09:16:05	INFO	02048061	VOTA	Espaço livre na MV [353.3 MB]	35BBFE76DB1BB3FB
006930	25/10/2026 09:16:05	INFO	02048061	VOTA	Espaço utilizado na MI [23.6 MB]	2F3DA4A97E33D417
006931	25/10/2026 09:16:05	INFO	02048061	VOTA	Espaço utilizado na MV [24.0 MB]	224A35A6878FFC5D
006932	25/10/2026 09:16:05	INFO	02048061	VOTA	Quantidade de memória total [3.7 GB]	2B46A21173E6E252
006933	25/10/2026 09:16:05	INFO	02048061	VOTA	Quantidade de memória livre [3.3 GB]	824B1AF48D6F9B18
006934	25/10/2026 09:16:05	INFO	02048061	VOTA	Quantidade de memória usada [406.7 MB]	AF5F3809FC01CD28
006935	25/10/2026 09:16:05	INFO	02048061	VOTA	Urna ligada conectada na rede CA em [125.59V] e na Bateria Interna com [13.46V/0A]	8E45AC913E2E59CD
006936	25/10/2026 09:16:27	INFO	02048061	VOTA	Identificador do eleitor digitado pelo mesário	8C27FAE7A133E89D
006937	25/10/2026 09:16:27	INFO	02048061	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	37459E26D852CF1C
006938	25/10/2026 09:16:28	INFO	02048061	VOTA	Foto do eleitor apresentada	7763E44F0C39F735
006939	25/10/2026 09:16:30	INFO	02048061	VOTA	Solicita digital. Tentativa [1] de [4]	37D50201AF2C9AF4
006940	25/10/2026 09:17:01	INFO	02048061	VOTA	Timeout de reconhecimento do dedo. Tentativa [1] de [4]	58AF6D23AABFF525
006941	25/10/2026 09:17:05	INFO	02048061	VOTA	Solicita digital. Tentativa [2] de [4]	C341D668ABA60CE7
006942	25/10/2026 09:17:23	INFO	02048061	VOTA	Timeout de reconhecimento do dedo. Tentativa [2] de [4]	CBE1AB02F8F807D1
006943	25/10/2026 09:17:25	INFO	02048061	VOTA	Solicita digital. Tentativa [3] de [4]	AF2128D8ADA58578
006944	25/10/2026 09:17:42	INFO	02048061	VOTA	Timeout de reconhecimento do dedo. Tentativa [3] de [4]	25595AF7093E6820
006945	25/10/2026 09:17:44	INFO	02048061	VOTA	Solicita digital. Tentativa [4] de [4]	7AA3D6DDD89AD9A5
006946	25/10/2026 09:18:04	INFO	02048061	VOTA	Timeout de reconhecimento do dedo. Tentativa [4] de [4]	3C77A1D9558AF115
006947	25/10/2026 09:18:06	INFO	02048061	VOTA	Solicitação de dado pessoal do eleitor para habilitação manual	7557233570835B3F
006948	25/10/2026 09:18:21	INFO	02048061	VOTA	Dado digitado confere	340C9BBCCFF2080A
006949	25/10/2026 09:18:21	INFO	02048061	VOTA	Solicita digital do mesário	EA6D1C0EB2149E28
006950	25/10/2026 09:18:26	INFO	02048061	VOTA	Batimento de digitais retornou o score 62	7E780ADC004B608B
006951	25/10/2026 09:18:26	INFO	02048061	VOTA	Biometria do mesário 004837732488 encontrada nos arquivos coletados (700013)	285FBD2EEA70521B
006952	25/10/2026 09:18:26	INFO	02048061	VOTA	Mesário 004837732488 habilitou o eleitor	E51C813353B91B3C
006953	25/10/2026 09:18:30	INFO	02048061	VOTA	Eleitor foi habilitado	58054CBD6F8DE513
006954	25/10/2026 09:18:57	INFO	02048061	VOTA	Voto confirmado para [Governador]	578BF2BBDCCE83D6
006955	25/10/2026 09:19:11	INFO	02048061	VOTA	Voto confirmado para [Presidente]	9D5BB8424CD04A33
006956	25/10/2026 09:19:12	INFO	02048061	VOTA	O voto do eleitor foi computado	BF7A052013B38FA7
006957	25/10/2026 09:19:13	INFO	02048061	VOTA	Aguardando digitação do identificador do eleitor	FA6388B9577A7EC3
006958	25/10/2026 09:20:01	INFO	02048061	VOTA	Identificador do eleitor digitado pelo mesário	DDC61600E2B43A52
006959	25/10/2026 09:20:01	INFO	02048061	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	FAF1540D55B03C75
006960	25/10/2026 09:20:01	INFO	02048061	VOTA	Foto do eleitor apresentada	7F607F71B448FC90
006961	25/10/2026 09:20:02	INFO	02048061	VOTA	Solicita digital. Tentativa [1] de [4]	510DCA2F4F60F7DC
006962	25/10/2026 09:20:06	INFO	02048061	VOTA	Capturada a digital. Tentativa [1] de [4]	B32E07ACE5B947E4
006963	25/10/2026 09:20:08	INFO	02048061	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [1] de [4]	85D1CA4B40B133ED
006964	25/10/2026 09:20:12	INFO	02048061	VOTA	Solicita digital. Tentativa [2] de [4]	FF0860978F7FC8CE
006965	25/10/2026 09:20:14	INFO	02048061	VOTA	Capturada a digital. Tentativa [2] de [4]	27298922DA9C7101
006966	25/10/2026 09:20:17	INFO	02048061	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [2] de [4]	D8C1D6DFCC1F2E52
006967	25/10/2026 09:20:18	INFO	02048061	VOTA	Solicita digital. Tentativa [3] de [4]	9EC4CB1CE0C7BAC4
006968	25/10/2026 09:20:21	INFO	02048061	VOTA	Capturada a digital. Tentativa [3] de [4]	748882EA5197A388
006969	25/10/2026 09:20:23	INFO	02048061	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [3] de [4]	2E72CB54D422AA79
006970	25/10/2026 09:20:24	INFO	02048061	VOTA	Solicita digital. Tentativa [4] de [4]	D231984574F9B386
006971	25/10/2026 09:20:26	INFO	02048061	VOTA	Capturada a digital. Tentativa [4] de [4]	E4FF545E23B0D7FF
006972	25/10/2026 09:20:29	INFO	02048061	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [4] de [4]	433FE99415D562C1
006973	25/10/2026 09:20:30	INFO	02048061	VOTA	Solicitação de dado pessoal do eleitor para habilitação manual	BE6B479FF900156B
006974	25/10/2026 09:20:37	INFO	02048061	VOTA	Dado digitado confere	BA6261E7C6F1D770
006975	25/10/2026 09:20:37	INFO	02048061	VOTA	Solicita digital do mesário	E53A88249D89D313
006976	25/10/2026 09:20:42	INFO	02048061	VOTA	Batimento de digitais retornou o score 38	03AE47758DF08429
006977	25/10/2026 09:20:42	INFO	02048061	VOTA	Biometria do mesário 004837732488 encontrada nos arquivos coletados (700013)	194D72FBD452656B
006978	25/10/2026 09:20:42	INFO	02048061	VOTA	Mesário 004837732488 habilitou o eleitor	3B295581E15AEB0A
006979	25/10/2026 09:20:43	INFO	02048061	VOTA	Eleitor foi habilitado	928EC9636ADC693C
006980	25/10/2026 09:20:53	INFO	02048061	VOTA	Tecla indevida pressionada	908D85548E784D62
006981	25/10/2026 09:20:56	INFO	02048061	VOTA	Voto confirmado para [Governador]	BE2F11F6CBC7723C
006982	25/10/2026 09:20:59	INFO	02048061	VOTA	Tecla indevida pressionada	90C336AD550CD764
006983	25/10/2026 09:21:01	INFO	02048061	VOTA	Voto confirmado para [Presidente]	9A883418153ADD5A
006984	25/10/2026 09:21:01	INFO	02048061	VOTA	O voto do eleitor foi computado	85FB4C5F9FF22E83
006985	25/10/2026 09:21:02	INFO	02048061	VOTA	Aguardando digitação do identificador do eleitor	022EB65E784D4759
006986	25/10/2026 09:27:41	INFO	02048061	VOTA	Identificador do eleitor digitado pelo mesário	106D93E24DF8A2F9
006987	25/10/2026 09:27:41	INFO	02048061	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	3742D030C6783117
006988	25/10/2026 09:27:41	INFO	02048061	VOTA	Foto do eleitor apresentada	08FC2BB06BBAEFA2
006989	25/10/2026 09:27:42	INFO	02048061	VOTA	Solicita digital. Tentativa [1] de [4]	F8FF34FA37229018
006990	25/10/2026 09:27:47	INFO	02048061	VOTA	Capturada a digital. Tentativa [1] de [4]	3175CACC9179A817
006991	25/10/2026 09:27:49	INFO	02048061	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [1] de [4]	CB0FB461E489345B
006992	25/10/2026 09:27:51	INFO	02048061	VOTA	Solicita digital. Tentativa [2] de [4]	AE3891E76BF38F1D
006993	25/10/2026 09:27:56	INFO	02048061	VOTA	Capturada a digital. Tentativa [2] de [4]	BB1C9B4F80C8F09A
006994	25/10/2026 09:27:59	INFO	02048061	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [2] de [4]	5FEE50E9A4F9CBF5
006995	25/10/2026 09:28:00	INFO	02048061	VOTA	Solicita digital. Tentativa [3] de [4]	3F88D5C773B418B3
006996	25/10/2026 09:28:04	INFO	02048061	VOTA	Capturada a digital. Tentativa [3] de [4]	8163A7F4E865355A
006997	25/10/2026 09:28:06	INFO	02048061	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [3] de [4]	09D2F56BFFA7D687
006998	25/10/2026 09:28:07	INFO	02048061	VOTA	Solicita digital. Tentativa [4] de [4]	73368AE18F813D10
006999	25/10/2026 09:28:12	INFO	02048061	VOTA	Capturada a digital. Tentativa [4] de [4]	A6FB24BFE40277A0
007000	25/10/2026 09:28:15	INFO	02048061	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [4] de [4]	249428FBA31D6691
007001	25/10/2026 09:28:16	INFO	02048061	VOTA	Solicitação de dado pessoal do eleitor para habilitação manual	6692EC9C256934CE
007002	25/10/2026 09:28:21	INFO	02048061	VOTA	Dado digitado confere	7F27A5B24A2FB63F
007003	25/10/2026 09:28:21	INFO	02048061	VOTA	Solicita digital do mesário	842D20C7A9440458
007004	25/10/2026 09:28:26	INFO	02048061	VOTA	Batimento de digitais retornou o score 60	EF0C6327BA776D07
007005	25/10/2026 09:28:26	INFO	02048061	VOTA	Biometria do mesário 004837732488 encontrada nos arquivos coletados (700013)	A8E34D4C93224BB3
007006	25/10/2026 09:28:26	INFO	02048061	VOTA	Mesário 004837732488 habilitou o eleitor	6CAB0A3F9331699A
007007	25/10/2026 09:28:31	INFO	02048061	VOTA	Eleitor foi habilitado	0BF8BC56DF153A9B
007008	25/10/2026 09:28:40	INFO	02048061	VOTA	Tecla indevida pressionada	43B79DDA48316066
007009	25/10/2026 09:28:51	INFO	02048061	VOTA	Tecla indevida pressionada	3A9DC261DA53F3B4
007010	25/10/2026 09:28:52	INFO	02048061	VOTA	Voto confirmado para [Governador]	0ECC8FEF53FD53E0
007011	25/10/2026 09:29:37	INFO	02048061	VOTA	Eleitor sem atividade por 45 segundos	A8ED6303331DD864
007012	25/10/2026 09:30:08	INFO	02048061	VOTA	Eleitor voltou a digitar enquanto estava sendo suspenso	B239098FF6C21653
007013	25/10/2026 09:30:29	INFO	02048061	VOTA	Voto confirmado para [Presidente]	9995AE4155F8FD13
007014	25/10/2026 09:30:30	INFO	02048061	VOTA	O voto do eleitor foi computado	8AA8FD7EC04E7971

```

## Anexo C08 - ASSIS BRASIL - zona 0006, seção 0150

Mesário ou ano de nascimento. Horários: 11:28:55 | 11:30:17 | 11:31:29 | 11:37:04 | 11:38:14 | 11:39:56 | 11:41:06 | 11:46:16 | 11:47:30 | 11:49:58. Intervalos em segundos: 82 | 72 | 335 | 70 | 102 | 70 | 310 | 74 | 148.

```text
C08 | ASSIS BRASIL | Zona 0006 | Seção 0150
Arquivo: o03221ac0157000060150-log.jez
Origem: raiz!logd.dat
Linhas 7692-7819, sem omitir eventos intermediários. Prefixo numérico = linha original.

007692	25/10/2026 11:26:03	INFO	02266388	VOTA	O voto do eleitor foi computado	747E578E9B48391A
007693	25/10/2026 11:26:04	INFO	02266388	VOTA	Aguardando digitação do identificador do eleitor	B9079CEF7630A16E
007694	25/10/2026 11:28:35	INFO	02266388	VOTA	Identificador do eleitor digitado pelo mesário	DA001A3ACB3907F1
007695	25/10/2026 11:28:35	INFO	02266388	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	F0DE5617D8130939
007696	25/10/2026 11:28:40	INFO	02266388	VOTA	Ano de nascimento digitado é igual ao do cadastro	4F3FB308823B26BB
007697	25/10/2026 11:28:55	INFO	02266388	VOTA	Eleitor foi habilitado	5A624484FAA175EF
007698	25/10/2026 11:29:07	INFO	02266388	VOTA	Voto confirmado para [Governador]	8264E9EA96889F3F
007699	25/10/2026 11:29:12	INFO	02266388	VOTA	Voto confirmado para [Presidente]	176B244F396EF2EA
007700	25/10/2026 11:29:12	INFO	02266388	VOTA	O voto do eleitor foi computado	D222274A059D4EE1
007701	25/10/2026 11:29:14	INFO	02266388	VOTA	Aguardando digitação do identificador do eleitor	48EA0C7F266A561B
007702	25/10/2026 11:29:30	INFO	02266388	VOTA	Identificador do eleitor digitado pelo mesário	F80B078B669A2461
007703	25/10/2026 11:29:30	INFO	02266388	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	893349474C331BB3
007704	25/10/2026 11:29:38	INFO	02266388	VOTA	Ano de nascimento digitado é igual ao do cadastro	C9663FC1582FC456
007705	25/10/2026 11:30:17	INFO	02266388	VOTA	Eleitor foi habilitado	360093742359803E
007706	25/10/2026 11:30:22	INFO	02266388	VOTA	Tecla indevida pressionada	17A2F2BE0FB64612
007707	25/10/2026 11:30:23	INFO	02266388	VOTA	Voto confirmado para [Governador]	8D9C431B46412955
007708	25/10/2026 11:30:26	INFO	02266388	VOTA	Tecla indevida pressionada	8440A90EFB52A1EB
007709	25/10/2026 11:30:27	INFO	02266388	VOTA	Voto confirmado para [Presidente]	C390FBDDBAB8F761
007710	25/10/2026 11:30:27	INFO	02266388	VOTA	O voto do eleitor foi computado	CD5953CD74986D93
007711	25/10/2026 11:30:28	INFO	02266388	VOTA	Aguardando digitação do identificador do eleitor	881D674B81AC9B5A
007712	25/10/2026 11:30:50	INFO	02266388	VOTA	Identificador do eleitor digitado pelo mesário	E20B08983D4AF312
007713	25/10/2026 11:30:50	INFO	02266388	VOTA	Identificador digitado pelo mesário foi: (CPF)	6C6FF40B7A6E6551
007714	25/10/2026 11:30:57	INFO	02266388	VOTA	Ano de nascimento digitado é igual ao do cadastro	B06C15F5B4EAA71A
007715	25/10/2026 11:31:29	INFO	02266388	VOTA	Eleitor foi habilitado	E4D155488BB2EF24
007716	25/10/2026 11:31:38	INFO	02266388	VOTA	Voto confirmado para [Governador]	16019A8BF697EE9A
007717	25/10/2026 11:31:42	INFO	02266388	VOTA	Voto confirmado para [Presidente]	342FDB7A27700717
007718	25/10/2026 11:31:43	INFO	02266388	VOTA	O voto do eleitor foi computado	5B4B1A9DBAB0F572
007719	25/10/2026 11:31:44	INFO	02266388	VOTA	Aguardando digitação do identificador do eleitor	5FE94A9FEFE8A655
007720	25/10/2026 11:36:13	INFO	02266388	VOTA	Identificador do eleitor digitado pelo mesário	D0AD51BA36443006
007721	25/10/2026 11:36:13	INFO	02266388	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	86CDABAFE6B446E0
007722	25/10/2026 11:36:15	INFO	02266388	VOTA	Solicita digital. Tentativa [1] de [4]	BB9D36B7205566DD
007723	25/10/2026 11:36:22	INFO	02266388	VOTA	Capturada a digital. Tentativa [1] de [4]	462F7785439C5B6A
007724	25/10/2026 11:36:24	INFO	02266388	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [1] de [4]	1AF8B46A50931FB4
007725	25/10/2026 11:36:26	INFO	02266388	VOTA	Solicita digital. Tentativa [2] de [4]	E0E8420593FB46A8
007726	25/10/2026 11:36:29	INFO	02266388	VOTA	Capturada a digital. Tentativa [2] de [4]	7F443E0E9E91DF6A
007727	25/10/2026 11:36:31	INFO	02266388	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [2] de [4]	99E55A654C372146
007728	25/10/2026 11:36:33	INFO	02266388	VOTA	Solicita digital. Tentativa [3] de [4]	EA7705A55AE37400
007729	25/10/2026 11:36:36	INFO	02266388	VOTA	Capturada a digital. Tentativa [3] de [4]	9E54B3977C3191CF
007730	25/10/2026 11:36:38	INFO	02266388	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [3] de [4]	9BFF6714E18290A7
007731	25/10/2026 11:36:39	INFO	02266388	VOTA	Solicita digital. Tentativa [4] de [4]	831C8D10BFA7DC79
007732	25/10/2026 11:36:43	INFO	02266388	VOTA	Capturada a digital. Tentativa [4] de [4]	E1726F3643C7887A
007733	25/10/2026 11:36:45	INFO	02266388	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [4] de [4]	B9252D37D1D390ED
007734	25/10/2026 11:36:47	INFO	02266388	VOTA	Solicitação de dado pessoal do eleitor para habilitação manual	7941C968C128008D
007735	25/10/2026 11:36:52	INFO	02266388	VOTA	Dado digitado confere	57CDD25B809CBE15
007736	25/10/2026 11:36:52	INFO	02266388	VOTA	Solicita digital do mesário	7F761F8D7C6548A6
007737	25/10/2026 11:36:57	INFO	02266388	VOTA	Biometria coletada não é do mesário 003520362461	A744851BF72B2510
007738	25/10/2026 11:36:58	INFO	02266388	VOTA	Batimento de digitais retornou o score 18	82501FC44B9907E9
007739	25/10/2026 11:36:58	INFO	02266388	VOTA	Biometria coletada não é do mesário 005703232496 (923470)	87B7D2379A6583FB
007740	25/10/2026 11:36:59	INFO	02266388	VOTA	Biometria coletada não é do mesário 005793582402	0C9316953EE75FCB
007741	25/10/2026 11:37:00	INFO	02266388	VOTA	Batimento de digitais retornou o score 18	C81F93E078DC9094
007742	25/10/2026 11:37:00	INFO	02266388	VOTA	Biometria coletada não é do mesário 008297482470 (923470)	DBA44B1EC348AB4A
007743	25/10/2026 11:37:01	INFO	02266388	VOTA	Batimento de digitais retornou o score 35	79E7EACCA9606B1B
007744	25/10/2026 11:37:01	INFO	02266388	VOTA	Digital coletada bate com uma digital gravada após o registro inicial de mesário. Não é possível associar a habilitação a um mesário.	D6E8D9C207DA9D04
007745	25/10/2026 11:37:04	INFO	02266388	VOTA	Eleitor foi habilitado	A4F8E27A95D24D29
007746	25/10/2026 11:37:15	INFO	02266388	VOTA	Voto confirmado para [Governador]	C4F1B73EF326703B
007747	25/10/2026 11:37:21	INFO	02266388	VOTA	Voto confirmado para [Presidente]	BFCF0E1AEE5C1ABC
007748	25/10/2026 11:37:22	INFO	02266388	VOTA	O voto do eleitor foi computado	D0264129816F0F73
007749	25/10/2026 11:37:23	INFO	02266388	VOTA	Aguardando digitação do identificador do eleitor	DE2B60ADD221C4C5
007750	25/10/2026 11:37:30	INFO	02266388	VOTA	Identificador do eleitor digitado pelo mesário	9B54E729B2464C24
007751	25/10/2026 11:37:30	INFO	02266388	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	0D1CDD87D2FA200F
007752	25/10/2026 11:37:37	INFO	02266388	VOTA	Ano de nascimento digitado é igual ao do cadastro	7C3C6D05C2776F01
007753	25/10/2026 11:38:14	INFO	02266388	VOTA	Eleitor foi habilitado	4E67F1FDF09706F3
007754	25/10/2026 11:38:27	INFO	02266388	VOTA	Voto confirmado para [Governador]	5F0FDB11DBBD4536
007755	25/10/2026 11:38:36	INFO	02266388	VOTA	Voto confirmado para [Presidente]	763CB44519C2BD5D
007756	25/10/2026 11:38:36	INFO	02266388	VOTA	O voto do eleitor foi computado	E0EF2E14C2528D86
007757	25/10/2026 11:38:37	INFO	02266388	VOTA	Aguardando digitação do identificador do eleitor	160311D1A0D84180
007758	25/10/2026 11:38:45	INFO	02266388	VOTA	Identificador do eleitor digitado pelo mesário	2F93E539BB45C951
007759	25/10/2026 11:38:45	INFO	02266388	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	1F6646DBD1DBC8FC
007760	25/10/2026 11:38:45	INFO	02266388	VOTA	Foto do eleitor apresentada	918196EF0746C5EA
007761	25/10/2026 11:38:46	INFO	02266388	VOTA	Solicita digital. Tentativa [1] de [4]	4F42BCD997EF60D6
007762	25/10/2026 11:38:56	INFO	02266388	VOTA	Capturada a digital. Tentativa [1] de [4]	28A6C41166AB5D5C
007763	25/10/2026 11:38:58	INFO	02266388	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [1] de [4]	E40283E939ACF136
007764	25/10/2026 11:39:00	INFO	02266388	VOTA	Solicita digital. Tentativa [2] de [4]	634DC686C426450F
007765	25/10/2026 11:39:04	INFO	02266388	VOTA	Capturada a digital. Tentativa [2] de [4]	96A2BED0406E1F0E
007766	25/10/2026 11:39:06	INFO	02266388	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [2] de [4]	FD27821713E06084
007767	25/10/2026 11:39:08	INFO	02266388	VOTA	Solicita digital. Tentativa [3] de [4]	1AEDC7875B66BDF0
007768	25/10/2026 11:39:13	INFO	02266388	VOTA	Capturada a digital. Tentativa [3] de [4]	C2B2DBDF3E9332CF
007769	25/10/2026 11:39:15	INFO	02266388	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [3] de [4]	0C1DC7BBD09C3ACA
007770	25/10/2026 11:39:17	INFO	02266388	VOTA	Solicita digital. Tentativa [4] de [4]	10CECAE0CB0A3BE6
007771	25/10/2026 11:39:19	INFO	02266388	VOTA	Capturada a digital. Tentativa [4] de [4]	0D3F7D8C4C1DDC23
007772	25/10/2026 11:39:22	INFO	02266388	VOTA	Número de tentativas de reconhecimento do dedo. Tentativa [4] de [4]	9CCDCDFF51B94493
007773	25/10/2026 11:39:23	INFO	02266388	VOTA	Solicitação de dado pessoal do eleitor para habilitação manual	29B763FE03EA0C2F
007774	25/10/2026 11:39:28	INFO	02266388	VOTA	Dado digitado confere	C2676696913A92B4
007775	25/10/2026 11:39:28	INFO	02266388	VOTA	Solicita digital do mesário	B24AAEF63930F74A
007776	25/10/2026 11:39:33	INFO	02266388	VOTA	Biometria coletada não é do mesário 003520362461	25B63BB0914A29B2
007777	25/10/2026 11:39:34	INFO	02266388	VOTA	Batimento de digitais retornou o score 52	3BDFC4419E433A37
007778	25/10/2026 11:39:34	INFO	02266388	VOTA	Biometria do mesário 005703232496 encontrada nos arquivos coletados (923470)	D684DDD7E4333149
007779	25/10/2026 11:39:34	INFO	02266388	VOTA	Mesário 005703232496 habilitou o eleitor	D9F34CB923D15DA8
007780	25/10/2026 11:39:56	INFO	02266388	VOTA	Eleitor foi habilitado	E70B058339B3F483
007781	25/10/2026 11:40:06	INFO	02266388	VOTA	Voto confirmado para [Governador]	DBA75BE1956F936F
007782	25/10/2026 11:40:11	INFO	02266388	VOTA	Voto confirmado para [Presidente]	CC888D17909468DF
007783	25/10/2026 11:40:11	INFO	02266388	VOTA	O voto do eleitor foi computado	A1335BDA9908BEEE
007784	25/10/2026 11:40:12	INFO	02266388	VOTA	Aguardando digitação do identificador do eleitor	5ABC23AD8BBCBD6A
007785	25/10/2026 11:40:24	INFO	02266388	VOTA	Identificador do eleitor digitado pelo mesário	CDA58165674C203A
007786	25/10/2026 11:40:24	INFO	02266388	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	797E68C5811DF702
007787	25/10/2026 11:40:32	INFO	02266388	VOTA	Ano de nascimento digitado é igual ao do cadastro	26083392BBBBB8F6
007788	25/10/2026 11:41:06	INFO	02266388	VOTA	Eleitor foi habilitado	8F7D7F15364F0A3E
007789	25/10/2026 11:41:14	INFO	02266388	VOTA	Voto confirmado para [Governador]	B03A00378E820807
007790	25/10/2026 11:41:19	INFO	02266388	VOTA	Voto confirmado para [Presidente]	DF7186618F7AADD5
007791	25/10/2026 11:41:19	INFO	02266388	VOTA	O voto do eleitor foi computado	5A1065F00BB4EB78
007792	25/10/2026 11:41:20	INFO	02266388	VOTA	Aguardando digitação do identificador do eleitor	46BBDF6403F559BA
007793	25/10/2026 11:45:37	INFO	02266388	VOTA	Identificador do eleitor digitado pelo mesário	0F57348642B87451
007794	25/10/2026 11:45:37	INFO	02266388	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	C095F87599DA834E
007795	25/10/2026 11:45:43	INFO	02266388	VOTA	Ano de nascimento digitado é igual ao do cadastro	B8FCF1F84122B9D2
007796	25/10/2026 11:46:16	INFO	02266388	VOTA	Eleitor foi habilitado	3BEEC3DB8F3EB266
007797	25/10/2026 11:46:26	INFO	02266388	VOTA	Voto confirmado para [Governador]	B76BA99394F76B09
007798	25/10/2026 11:46:29	INFO	02266388	VOTA	Voto confirmado para [Presidente]	F74B486BAAACA852
007799	25/10/2026 11:46:30	INFO	02266388	VOTA	O voto do eleitor foi computado	C78ECDFC2ACA4967
007800	25/10/2026 11:46:31	INFO	02266388	VOTA	Aguardando digitação do identificador do eleitor	CFD74ED55F1B7CF6
007801	25/10/2026 11:46:49	INFO	02266388	VOTA	Identificador do eleitor digitado pelo mesário	24149F0D52384DE7
007802	25/10/2026 11:46:49	ALERTA	02266388	VOTA	Identificador do eleitor digitado inválido	74B274A88B6F05EC
007803	25/10/2026 11:46:51	INFO	02266388	VOTA	Aguardando digitação do identificador do eleitor	446D479C364F0239
007804	25/10/2026 11:46:59	INFO	02266388	VOTA	Identificador do eleitor digitado pelo mesário	A98B690B17B05643
007805	25/10/2026 11:47:02	INFO	02266388	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	F0F1774BD2863A82
007806	25/10/2026 11:47:09	INFO	02266388	VOTA	Ano de nascimento digitado é igual ao do cadastro	B7F12EE8E4D8C721
007807	25/10/2026 11:47:30	INFO	02266388	VOTA	Eleitor foi habilitado	5BBCCD93F8347FE2
007808	25/10/2026 11:47:43	INFO	02266388	VOTA	Voto confirmado para [Governador]	5C247B4837E6E271
007809	25/10/2026 11:47:46	INFO	02266388	VOTA	Tecla indevida pressionada	B6E5C14B863C9F9D
007810	25/10/2026 11:47:47	INFO	02266388	VOTA	Voto confirmado para [Presidente]	32764252D788D6CD
007811	25/10/2026 11:47:48	INFO	02266388	VOTA	O voto do eleitor foi computado	ED9B8D697F1CD25E
007812	25/10/2026 11:47:49	INFO	02266388	VOTA	Aguardando digitação do identificador do eleitor	F327653E9128F60E
007813	25/10/2026 11:49:19	INFO	02266388	VOTA	Identificador do eleitor digitado pelo mesário	4DA7E34DB35DB232
007814	25/10/2026 11:49:19	INFO	02266388	VOTA	Identificador digitado pelo mesário foi: (Título de eleitor)	8E7FF0031C280101
007815	25/10/2026 11:49:26	INFO	02266388	VOTA	Ano de nascimento digitado é igual ao do cadastro	98737898D32C77B4
007816	25/10/2026 11:49:58	INFO	02266388	VOTA	Eleitor foi habilitado	004F8872CC294BBB
007817	25/10/2026 11:50:27	INFO	02266388	VOTA	Voto confirmado para [Governador]	2C4B934AF3A8BF7F
007818	25/10/2026 11:50:32	INFO	02266388	VOTA	Voto confirmado para [Presidente]	39B6B50DEB6DC417
007819	25/10/2026 11:50:32	INFO	02266388	VOTA	O voto do eleitor foi computado	1A9996F6DF390C84

```
