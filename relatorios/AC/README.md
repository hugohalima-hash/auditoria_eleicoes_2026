# Acre - liberações sucessivas e intervalo entre eleitores

[Relatório completo e cronologia dos casos](RELATORIO_COMPLETO_AC.md). Revisão de 01/11/2026.

O tempo avaliado é o intervalo entre duas mensagens consecutivas de liberação do eleitor. A duração da digitação do voto não é usada para selecionar suspeitas.

## Resultados

- Somente mesário: 1.316 séries de duas ou mais votações concluídas, em 869 seções; 103 séries com três ou mais, em 90 seções. Maior série: seis, em Jordão, zona 0005, seção 0122. Intervalos: 186, 178, 182, 179 e 125 segundos.
- Mesário ou ano de nascimento: 3.580 séries com duas ou mais; 557 com três ou mais. Maior série: dez, em Assis Brasil, zona 0006, seção 0150; mistura os procedimentos.
- Nenhuma série exclusivamente de mesário atingiu a triagem de rapidez. Uma série de três confirmações de ano de nascimento atingiu o critério, em Rio Branco, zona 0001, seção 0830: intervalos de 43 e 56 s. Média de 49,5 s, somente 0,5 s abaixo da referência rápida local; resultado limítrofe.
- O universo de conferência permanece em 37.979 votações concluídas: 22.654 com registro de mesário e 15.325 com ano de nascimento. Quarenta e uma seções apresentaram concentração elevada, contendo 2.458 dessas votações.

Esses números não são contagens de fraude. A comparação de rapidez é exploratória: média de série com três ou mais liberações inferior ao percentil 10 de pelo menos trinta pares biométricos da própria seção, exigindo registros adequados à comparação. Não há ajuste por fila, horário ou perfil individual, nem teste de significância com correção de múltiplas comparações.

## Dados e logs

- [Pares, sequências e trechos cronológicos integrais](Acre_Sequencias_e_Logs.zip): todos os pares consecutivos do estado, todas as séries, referência biométrica de cada seção, casos destacados e oito trechos completos, sem omissão de eventos intermediários.
- [Logs originais e texto integral do dia](Acre_Logs_Integrais.zip): 46 seções, incluindo as 41 com concentração elevada e as demais dos exemplos; sem duplicação de seções.
- [Índice dos oito casos](ritmo/04_casos_destacados.csv), [resumo numérico](ritmo/resumo.json) e [conferências de consistência](ritmo/validacao.json).
- [41 seções com concentração elevada](anexos/10_secoes_proporcao_elevada.csv).
- [Totais dos municípios](anexos/16_resumo_municipal_por_votos.csv).
- [Pacote anterior de totais e votações individuais](Dados_Acre_Habilitacoes_e_Tempos.zip), preservado como dados complementares. Os recortes antigos de duração do voto não integram o critério de rapidez desta revisão.

Os ZIPs têm SHA-256 de cada entrada. O PDF apresenta a explicação, os horários de cada liberação das maiores séries e os oito trechos integrais. Os logs de um dia inteiro estão nos anexos digitais, para evitar substituir a evidência completa por exemplos.

## Reprodução

1. Obtenha `AC-tentativa1.zip` na [execução publicada](https://github.com/hugohalima-hash/auditoria_eleicoes_2026/releases/tag/auditoria-v3-41263277696) e extraia para `relatorios/AC/dados/`, mantendo também o próprio ZIP em `dados/publicado.zip`.
2. Obtenha o [pacote oficial bruto do Acre](https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2026/arqurnatot/bu_imgbu_logjez_rdv_vscmr_2026_2t_AC.zip), em `downloads/` na raiz do repositório.
3. Execute `python relatorios/AC/ritmo/analisar_ritmo.py`, depois `python relatorios/AC/ritmo/gerar_relatorio.py` e `python relatorios/AC/ritmo/validar_e_empacotar.py`.

Os scripts exigem os hashes congelados dos pacotes e do motor e conferem todas as contagens por seção. A geração de PDF requer ReportLab e fontes DejaVu. Os máximos das séries foram conferidos para os dois grupos nas 2.270 seções; os oito trechos foram conferidos linha a linha com a origem.
