# Acre - habilitação por mesário e ano de nascimento

[Relatório revisado](RELATORIO_COMPLETO_AC.md), com totais, proporções, sequências e tempos. Data: 01/11/2026.

## Resultados centrais

- 37.979 votações concluídas no conjunto: 22.654 com registros de mesário e 15.325 com confirmação de ano de nascimento.
- 41 seções com proporção elevada do conjunto, contendo 2.458 dessas votações.
- 1.620 conclusões em até dez segundos, incluindo 114 após espera por identificação de pelo menos cinco minutos.
- Totais e casos isolados são avaliados; pertencer a uma sequência não é requisito de seleção.

Os números delimitam um universo de conferência, não uma contagem de fraudes ou de eleitores ausentes. O relatório explica os critérios, as diferenças entre as medidas de tempo e os documentos necessários para investigação.

## Dados completos

[Baixar o pacote de dados e anexos](Dados_Acre_Habilitacoes_e_Tempos.zip).

O pacote contém a relação integral das 37.979 votações do conjunto, com horários, procedimento e referências ao log; os totais das 2.270 seções; as 41 seções selecionadas por proporção; os recortes de duração e espera; as sequências concluídas; e os anexos de interrupções e múltiplos históricos. Os checksums estão incluídos no ZIP.

### Anexos de consulta direta

- [41 seções com proporção elevada](anexos/10_secoes_proporcao_elevada.csv).
- [Referências da comparação conjunta](anexos/11_referencias_proporcao_combinada.csv).
- [Resumo municipal por votos concluídos](anexos/16_resumo_municipal_por_votos.csv).
- [Sete interrupções](anexos/01_interrupcoes.csv).
- [Dez seções separadas da comparação](anexos/02_quarentena.csv).
- [39 seções com múltiplos históricos](anexos/03_multiplos_blocos.csv).
- [Metadados e indicadores completos](evidencias_relatorio_revisado.json).

A fonte operacional permanece [AC-tentativa1.zip](https://github.com/hugohalima-hash/auditoria_eleicoes_2026/releases/download/auditoria-v3-41263277696/AC-tentativa1.zip), da execução 41263277696. Os tempos foram apurados adicionalmente no pacote bruto oficial, conferido por SHA-256. A contagem por seção foi reconciliada com a fonte publicada.

## Reprodução

Os scripts complementares estão em `revisao/`: `analisar_tempos.py`, `complementar_analise.py`, `conferir_esperas.py` e `gerar_relatorio_revisado.py`. Para reproduzir, obtenha o pacote publicado e extraia-o para `dados/` neste diretório; mantenha o pacote oficial AC em `downloads/` na raiz do repositório e o motor de fingerprint indicado nos metadados. Execute os quatro scripts nessa ordem. A apresentação PDF requer ReportLab e fontes DejaVu em Linux. A análise usa a biblioteca padrão do Python.
