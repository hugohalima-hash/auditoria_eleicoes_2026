# Auditor Eleitoral Independente 2026

**Motor 3.0 em validação. As classificações do motor 2.1 e seus alertas foram retirados de uso para conclusões até reprocessamento. Nenhuma acurácia de 99,9% está certificada.**

O programa analisa os logs públicos do TSE de 25/10/2026. Não autentica assinaturas dos arquivos, não identifica pessoas e não confirma fraude.

## Correção e evidências

- [Correções, testes e limitações da validação](VALIDACAO_V3.md).
- [Critérios da triagem estatística e quarentena](METODOLOGIA_ALERTAS.md).
- [Estado atual](STATUS.json).
- [Evidências de regressão extraídas de logs reais](validacao/casos_reais.json).
- [Comparação das versões em 188 logs](validacao/resultado_corpus.json).

A amostra de desenvolvimento tem 48.473 habilitações: os 15 registros antes indefinidos passaram a biométricos, e 49 dos 51 avisos anteriores foram explicados por suspensão sem voto. As duas interrupções restantes foram preservadas para revisão. Há reconciliação independente de contagens em 165 logs, sem divergência. Esses resultados não constituem estimativa de acurácia populacional.

Os 422 alertas de proporção elevada e os 64 de volume elevado são **históricos e não validados**. Não devem ser usados como lista de irregularidades. Os arquivos da Release `checkpoint-2026-10-31` preservam a execução antiga; não são uma validação da versão 3.0.

## Executar

Mantenha todos os módulos Python juntos. Reprocesse em uma pasta nova e preserve os pacotes originais durante a validação:

```bash
python -m unittest -v test_motor test_lote test_validacao
python auditar.py --ufs AM --saida resultados_v3_revisado --pasta-download downloads
python anomalias.py --resultados resultados_v3_revisado --saida alertas_v3
python consolidar.py --resultados resultados_v3_revisado --saida entrega_v3
```

Resultados antigos, de outro fingerprint ou sem manifesto íntegro são recusados. Casos ambíguos ficam fora da comparação estatística, em quarentena, preservados para revisão. Manifestos detectam alteração dos resultados; não autenticam a origem TSE.

Para repetir a verificação do corpus, baixe o pacote do AM da fonte registrada e use `preparar_amostra.py`; depois execute `python validar_corpus.py`. A comparação antiga exige o arquivo de referência preservado em `validacao/`.

[Documentação de execução](LEIA-ME.md). [Relatório histórico, aguardando reprocessamento](RELATORIO_PARCIAL.md). GitHub preserva os arquivos; o processamento depende dos recursos do computador ou servidor executor.
