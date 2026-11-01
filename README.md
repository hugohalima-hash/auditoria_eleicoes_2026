# Auditor Eleitoral Independente 2026

Programa em Python para análise exploratória dos logs públicos das urnas do TSE, com foco nas habilitações sem reconhecimento biométrico, eventos de mesário e sequências consecutivas durante todo o dia do segundo turno de 25/10/2026.

## Situação atual

**Auditoria nacional incompleta.** O último consolidado preservado contém **260.026 arquivos de log**, referentes a **AC, AL, AP, BA, CE, MG, PA, PE, PR, RJ, RR, RS e exterior (ZZ)**.

As demais UFs permanecem pendentes no consolidado. A existência de sequências longas não comprova fraude. Os arquivos públicos não confirmam a identidade ou a presença física de cada eleitor, e este programa não autentica assinaturas criptográficas nem faz perícia física nos equipamentos.

O checkpoint da Release original contém 252.925 logs de 12 unidades. O resultado posterior de AL e o consolidado de 13 unidades estão documentados no relatório e no status; o novo pacote integral ainda não foi anexado à Release original.

A triagem ampliada está em [METODOLOGIA_ALERTAS.md](METODOLOGIA_ALERTAS.md), com resumo e comparações em `triagem/`. Execute `python anomalias.py --resultados resultados --saida alertas`. Os alertas não são conclusões de fraude.

## Organização do trabalho

- Código e documentação: arquivos deste repositório.
- Resultados completos do checkpoint: arquivo `resultados_auditoria_2026.zip` disponível na [versão publicada](https://github.com/hugohalima-hash/auditoria_eleicoes_2026/releases/tag/checkpoint-2026-10-31), junto da cópia do programa e dos hashes SHA-256.
- Documentação técnica: [LEIA-ME.md](LEIA-ME.md).
- Relatório parcial: [RELATORIO_PARCIAL.md](RELATORIO_PARCIAL.md).
- Estado de retomada: [STATUS.json](STATUS.json).
- Arquivos brutos do TSE: obtidos diretamente na fonte oficial durante a execução; não devem ser incorporados ao histórico Git.

GitHub preserva o código e os resultados. O processamento ainda depende da RAM e do disco de um computador ou servidor. O programa usa limites conservadores e pode apagar os pacotes baixados depois da análise, preservando os resultados.

## Retomar o checkpoint

Baixe o anexo `resultados_auditoria_2026.zip` da versão publicada e extraia seu conteúdo na pasta `resultados`. As subpastas das UFs devem ficar diretamente dentro dela, como `resultados/AC/resumo.json`.

```bash
python auditar.py --brasil --saida resultados --estados-simultaneos 1 --conexoes 4 --processos 1 --limite-memoria-mib 1536 --apagar-pacotes
python consolidar.py --resultados resultados --saida entrega
```

Em Linux com glibc, pode-se iniciar com `MALLOC_ARENA_MAX=2 python auditar.py ...` para reduzir reservas virtuais do alocador. Os limites pelo módulo `resource` são aplicados onde esse módulo está disponível.

Os resultados completos da mesma versão e data são reaproveitados automaticamente. O checkpoint preservado não inclui os pacotes brutos ou as partes de downloads que estavam em andamento quando o ambiente anterior se desconectou.

## Verificação

```bash
python -m unittest -v test_motor test_lote
```

Há nove testes de regressão, incluindo classificação, cancelamentos, logs aninhados, deduplicação, controle de retenção de memória e downloads por faixas.

## Fonte

[Arquivos transmitidos para totalização — TSE](https://dadosabertos.tse.jus.br/dataset/resultados-2026-arquivos-transmitidos-para-totalizacao).

Os relatórios detalham habilitações, votos vinculados, categorias indefinidas, avisos, falhas de leitura e cobertura contra a lista oficial de seções principais. Uma cobertura de 100% dessa lista não equivale a uma auditoria integral da eleição.
