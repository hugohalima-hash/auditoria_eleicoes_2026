# Relatório completo do Acre

[Leia o relatório completo](RELATORIO_COMPLETO_AC.md).

Análise documental dos 2.270 logs públicos, segundo turno de 25/10/2026. Versão fixada: motor 3.0, fingerprint 7c0a3a5dd412d61bedf77aba11c9e4df4a8574b52718e502e9a5d45c7d5a70cb, commit de execução 83d6bed1523a4ec20d9a55dce4e7aaa49646023d. A análise não certifica fraude, regularidade integral nem acurácia de 99,9%.

## Anexos completos

- [Sete interrupções, com linhas dos logs](anexos/01_interrupcoes.csv).
- [Dez seções em quarentena](anexos/02_quarentena.csv).
- [39 seções com múltiplos blocos](anexos/03_multiplos_blocos.csv).
- [Blocos do dia e identificadores de equipamento](anexos/04_blocos_do_dia.csv).
- [Resumo dos 22 municípios](anexos/05_resumo_municipal.csv).
- [53 itens de alerta em 45 seções](anexos/06_alertas_integrais.csv).
- [Referências da comparação estatística](anexos/07_referencias_comparacao.csv).
- [Evidências e metadados do relatório](evidencias_relatorio.json).

O pacote integral publicado, incluindo todas as 2.270 linhas de perfil de seção, séries e originais selecionados, está em [AC-tentativa1.zip](https://github.com/hugohalima-hash/auditoria_eleicoes_2026/releases/download/auditoria-v3-41263277696/AC-tentativa1.zip).

## Reprodução da apresentação

A fonte de geração é `gerar_relatorio.py`. Para reproduzir a apresentação, coloque o pacote publicado no mesmo diretório do script com o nome `AC-publicado.zip`, extraia seu conteúdo para `dados/` e disponibilize `fonte_publicada.json`. Execute a partir de uma cópia do repositório com Python, ReportLab e fontes DejaVu em Linux. O script confere os hashes do manifesto e gera Markdown, PDF e os anexos em `output/`. A versão em texto deste diretório é o resultado publicado; a aparência do PDF não constitui uma validação adicional dos dados.
