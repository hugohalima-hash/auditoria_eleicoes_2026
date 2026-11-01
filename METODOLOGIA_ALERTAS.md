# Triagem ampliada de anomalias — versão 1

Este módulo complementa o motor 2.1, sem alterar suas classificações. Os alertas são descritivos e não constituem conclusão de fraude ou de atuação irregular de mesários. A execução nacional segue em andamento. A primeira triagem contém somente as 12 unidades do checkpoint original.

Execute `python anomalias.py --resultados resultados --saida alertas` após cada atualização. O módulo só inclui pastas com resumo e CSV de urnas cujo total processado coincide com o total de logs do pacote. Essa condição não garante cobertura de todas as seções oficiais; consulte as lacunas do relatório principal.

## Critérios implementados

- Proporção de habilitações com eventos de mesário e volume total de habilitações: comparação dentro do mesmo município e zona, exigindo ao menos 20 seções com 100 habilitações ou mais. Limite superior exploratório: Q3 + 3 × IQR, usando quartis inclusivos. Também exige diferença maior que 10 pontos percentuais da mediana para proporções, ou 50 habilitações para volumes. A própria seção participa da referência. Não é teste de significância nem probabilidade de fraude; não controla diferenças de eleitorado, biometria cadastrada ou agregações.
- Sequência com eventos de mesário de pelo menos dez habilitações: limiar fixo de triagem, preservando a definição do motor.
- Intervalo médio entre inícios de habilitações inferior a 30 segundos em séries de mesário com pelo menos dez registros. A média é duração entre primeiro e último início dividida por N−1; não mede duração individual dos votos e não cobre as habilitações fora dessas séries.
- Ajustes de relógio registrados, linhas malformadas, categorias indefinidas, avisos de vínculo, diferença entre votos computados e vinculados, diferença entre habilitações e votos vinculados.
- Múltiplos blocos de log: informação de contexto, sem afirmar substituição de equipamento. Cancelamentos legítimos podem explicar habilitações sem voto vinculado.

Os arquivos `alertas.csv`, `referencias_comparacao.csv` e `resumo.json` preservam os valores, limites e contexto. Uma seção pode receber vários alertas. Os totais de alertas não devem ser interpretados como total de votos suspeitos. Grupos com menos de 20 seções elegíveis ficam sem comparação estatística.

## Etapas que exigem evidências adicionais

A versão atual não faz análise de distribuição de votos por candidato, não identifica voto individual, não compara horários individuais de todas as habilitações e não fornece contagem explícita de cancelamentos. Para essas verificações, são necessários BU/RDV e/ou nova passagem pelos logs originais. Confrontar cadernos de votação e atas requer acesso a esses documentos. Ausência de um alerta não certifica regularidade.

Antes de atribuir irregularidade, verificar o log original, configuração e agregação da seção, eventual substituição de urna, falhas de leitor, atas, número de eleitores aptos e perfil de biometria. Uma diferença estatística também pode indicar limitação do analisador.
