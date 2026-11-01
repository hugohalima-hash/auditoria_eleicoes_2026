> **RELATÓRIO HISTÓRICO DO MOTOR 2.1 — RETIRADO DE USO PARA CONCLUSÕES.** Foram identificados defeitos no classificador. Números e rankings abaixo aguardam reprocessamento. Consulte `VALIDACAO_V3.md` e `STATUS.json`.

# Auditor Eleitoral Independente 2026 — relatório de execução

**Escopo:** logs públicos do segundo turno de 25/10/2026, durante todo o dia. Motor 2.1.

**Situação:** 13 de 28 UFs processadas (26 estados, Distrito Federal e exterior).
**Arquivos de log processados:** 260.026.
**Erros de leitura:** 0; **habilitações indefinidas:** 2.200; **avisos:** 5.115.

**UFs pendentes:** AM, DF, ES, GO, MA, MS, MT, PB, PI, RN, RO, SC, SE, SP, TO.

## Resultados por estado

As contagens abaixo são de habilitações e de eventos de voto vinculados pelo analisador. As categorias permanecem distintas.

| UF | Logs | Cobertura da lista principal | Habilitações com eventos de mesário | Destas, com voto vinculado | Maior série de habilitações com eventos de mesário | Maior série no grupo ampliado | Indefinidas |
|---|---:|---:|---:|---:|---:|---:|---:|
| AC | 2.270 | 100.00% | 22.661 | 22.654 | 6 | 10 | 15 |
| AL | 7.101 | 100.00% | 135.906 | 135.874 | 75 | 83 | 68 |
| AP | 1.914 | 100.00% | 19.689 | 19.685 | 5 | 8 | 7 |
| BA | 35.476 | 100.00% | 702.347 | 702.243 | 102 | 178 | 314 |
| CE | 23.765 | 100.00% | 429.368 | 429.294 | 52 | 100 | 183 |
| MG | 52.062 | 100.00% | 888.015 | 887.910 | 59 | 80 | 354 |
| PA | 20.827 | 100.00% | 277.411 | 277.373 | 14 | 39 | 193 |
| PE | 21.418 | 100.00% | 399.854 | 399.764 | 54 | 157 | 211 |
| PR | 27.142 | 100.00% | 493.375 | 493.321 | 139 | 158 | 248 |
| RJ | 37.675 | 100.00% | 750.381 | 750.301 | 60 | 190 | 381 |
| RR | 1.519 | 100.00% | 12.649 | 12.646 | 4 | 9 | 5 |
| RS | 27.547 | 100.00% | 582.425 | 582.379 | 77 | 96 | 221 |
| ZZ | 1.310 | 96.97% | 0 | 0 | 0 | 579 | 0 |

## Totais das UFs processadas

- Habilitações: 67.163.128.
- Eventos de voto computado: 67.158.013.
- Habilitações com eventos de mesário: 4.714.081; com voto vinculado: 4.713.444.
- Grupo ampliado sem evento biométrico reconhecido: 9.416.783; com voto vinculado: 9.415.650.

## Quantas sequências foram identificadas

Contagens de séries máximas consecutivas de habilitações. Uma série de dez também entra nas faixas de pelo menos três e cinco; as faixas não devem ser somadas.

| Grupo | Séries de 3 ou mais | Séries de 5 ou mais | Séries de 10 ou mais |
|---|---:|---:|---:|
| Com eventos de mesário | 45.577 | 2.078 | 598 |
| Grupo ampliado sem evento biométrico | 272.661 | 22.730 | 2.008 |

## Maiores sequências de habilitações com eventos de mesário

Ranking descritivo; não é classificação de fraude. Datas e horários são os registrados pelos equipamentos. O CSV contém todos os casos, referências às linhas e categorias.

| UF | Município | Zona / seção | Habilitações | Votos vinculados | Início | Fim |
|---|---|---|---:|---:|---|---|
| PR | UBIRATÃ | 0098 / 0100 | 139 | 139 | 25/10/2026 09:25:13 | 25/10/2026 16:11:13 |
| PR | TOMAZINA | 0019 / 0055 | 137 | 137 | 25/10/2026 08:01:25 | 25/10/2026 11:39:34 |
| BA | DIAS D'ÁVILA | 0186 / 0134 | 102 | 102 | 25/10/2026 08:40:47 | 25/10/2026 11:28:29 |
| PR | MANDAGUAÇU | 0102 / 0008 | 85 | 85 | 25/10/2026 08:10:36 | 25/10/2026 10:45:21 |
| PR | TOMAZINA | 0019 / 0055 | 85 | 85 | 25/10/2026 11:42:27 | 25/10/2026 16:23:46 |
| BA | MARAÚ | 0078 / 0158 | 78 | 78 | 25/10/2026 10:54:03 | 25/10/2026 15:17:06 |
| RS | OSÓRIO | 0077 / 0093 | 77 | 77 | 25/10/2026 10:45:51 | 25/10/2026 13:24:41 |
| AL | OLHO D'ÁGUA DAS FLORES | 0011 / 0119 | 75 | 75 | 25/10/2026 12:29:01 | 25/10/2026 16:30:02 |
| AL | OLHO D'ÁGUA DAS FLORES | 0011 / 0119 | 73 | 73 | 25/10/2026 09:13:29 | 25/10/2026 11:23:15 |
| BA | LAURO DE FREITAS | 0180 / 0232 | 72 | 72 | 25/10/2026 12:54:14 | 25/10/2026 14:29:25 |
| BA | CANDEIAS | 0127 / 0326 | 71 | 71 | 25/10/2026 11:04:07 | 25/10/2026 12:39:13 |
| RS | IVOTI | 0118 / 0143 | 65 | 65 | 25/10/2026 13:29:35 | 25/10/2026 15:35:47 |
| BA | LAURO DE FREITAS | 0180 / 0547 | 64 | 64 | 25/10/2026 11:44:40 | 25/10/2026 13:08:13 |
| BA | TERRA NOVA | 0128 / 0190 | 60 | 60 | 25/10/2026 09:41:24 | 25/10/2026 10:51:27 |
| RJ | RIO DE JANEIRO | 0008 / 0074 | 60 | 60 | 25/10/2026 11:27:11 | 25/10/2026 12:55:12 |
| RS | COTIPORÃ | 0088 / 0113 | 60 | 60 | 25/10/2026 08:16:52 | 25/10/2026 09:30:47 |
| RS | COTIPORÃ | 0088 / 0113 | 60 | 60 | 25/10/2026 09:40:57 | 25/10/2026 10:53:51 |
| MG | SÃO MIGUEL DO ANTA | 0268 / 0068 | 59 | 59 | 25/10/2026 08:32:24 | 25/10/2026 10:19:00 |
| BA | SIMÕES FILHO | 0033 / 0139 | 58 | 58 | 25/10/2026 09:22:29 | 25/10/2026 10:59:32 |
| BA | SÃO GONÇALO DOS CAMPOS | 0108 / 0148 | 56 | 56 | 25/10/2026 08:49:55 | 25/10/2026 16:04:34 |

## Como interpretar

O grupo de eventos de mesário reúne: mensagem explícita de habilitação; captura seguida de gravação de digital de mesário; ou indicação de que a habilitação não pode ser associada a um mesário. Essa última mensagem não significa, isoladamente, que o voto foi irregular.

O grupo ampliado acrescenta confirmações do ano de nascimento sem evento biométrico reconhecido na tentativa. É uma inferência do log; não informa se o eleitor tinha biometria cadastrada. Não se deve equiparar esse total ao indicador específico do BU sobre biometria cadastrada não reconhecida.

Uma habilitação pode não terminar em voto computado. Por isso, as colunas de habilitação e de voto vinculado são separadas. Avisos e categorias indefinidas estão listados e não foram convertidos automaticamente em liberações por mesário.

A cobertura compara as seções identificadas nos logs com as seções principais da configuração oficial. Seções agregadas são separadas. Seções não instaladas ou com apuração por cédulas podem exigir exame distinto. Uma cobertura de 100% não elimina ressalvas de classificação.

O processamento lê logs aninhados de equipamentos substituídos e elimina cópias de linhas por multiplicidade máxima. São registrados CRC de leitura e SHA-256 por log. Não há autenticação de assinaturas criptográficas nesta ferramenta.

**Limites da conclusão:** sequências e frequências descrevem os registros publicados. Não demonstram a identidade ou a presença física dos votantes, não revelam o candidato escolhido e não comprovam fraude. Este trabalho não verifica hardware, software instalado, documentos de identificação, assinaturas dos cadernos de votação ou intenção de voto.

## Fontes e reprodução

- [Portal de Dados Abertos do TSE](https://dadosabertos.tse.jus.br/dataset/resultados-2026-arquivos-transmitidos-para-totalizacao).
- Configurações oficiais de seções, pleito 3221, preservadas por UF junto aos resultados.
- O arquivo `fontes_estaduais.json` registra os endereços dos pacotes e os metadados observados.
- Código, comando de execução, testes e metodologia detalhada acompanham a entrega.

```bash
MALLOC_ARENA_MAX=2 python auditar.py --brasil --saida resultados --estados-simultaneos 1 --conexoes 4 --processos 1 --limite-memoria-mib 1536 --apagar-pacotes
python consolidar.py --resultados resultados --saida entrega
```
