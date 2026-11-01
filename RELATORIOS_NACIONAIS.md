# Relatórios estaduais: ritmo entre liberações e logs

Complemento à execução nacional concluída `41263277696`, usando os mesmos pacotes congelados. O relatório do Acre aprovado é a referência de método e apresentação.

## Entregas por unidade

- Relatório PDF e Markdown, em linguagem acessível e autônoma.
- Totais de votações concluídas com mesário e ano de nascimento, incluindo ocorrências isoladas.
- Séries exclusivamente de mesário e séries do conjunto, com horários de cada liberação, cada intervalo, média, mínimo e máximo.
- Referência biométrica da própria seção: pares consecutivos, média, mediana e percentil 10.
- Concentração do conjunto por seção, com referência no mesmo município e zona.
- CSVs completos, comprimidos, de todos os pares, séries e votações do conjunto.
- Trechos integrais de todas as séries selecionadas por ritmo; originais e texto de todo o dia de todas as seções selecionadas por ritmo ou concentração.
- Até oito exemplos no PDF, com trechos completos; os exemplos não substituem os anexos integrais.

O universo compreende os 26 estados, o Distrito Federal e o exterior (ZZ), 28 unidades. A duração de digitação e confirmação do voto não é usada para selecionar suspeitas. As contagens não são contagens de fraude.

## Qualidade e execução

Cada pacote de referência é conferido contra o SHA-256 publicado no GitHub e todos os hashes internos. O pacote bruto do TSE precisa ter o mesmo SHA-256 usado na execução nacional original. Cada seção precisa reproduzir as contagens por tipo e os máximos das séries concluídas nos dois grupos.

O processamento retém na memória apenas os ciclos e pares de uma seção por vez; os pares e séries integrais são gravados em CSV comprimido. As distribuições estaduais são agregadas por frequência exata, sem amostragem de intervalos.

A seleção de rapidez é exploratória: série com pelo menos três votações concluídas, seção admissível, pelo menos trinta pares biométricos da própria seção e média da série inferior ao percentil 10 desses pares. Não há ajuste por fila, horário, perfil individual ou múltiplas comparações. Diferenças próximas do limite não constituem evidência forte de ritmo excepcional.

A comparação de concentração exige cem votações concluídas por seção e vinte seções no mesmo município e zona; limite superior ao maior entre Q3 + 3 IQR e mediana + dez pontos percentuais. Os grupos e referências ficam disponíveis.

A execução é persistente no GitHub Actions, no fluxo **Relatórios nacionais - ritmo e logs**, com duas unidades em paralelo. Cada unidade publica seu diagnóstico, inclusive em falha. O índice e os totais nacionais só são emitidos depois da conferência de conclusão das 28 unidades. O reprocessamento original e seus arquivos são preservados.

## Reprodução

`python -m unittest -v test_motor test_lote test_validacao test_relatorios_nacionais`

`python -m relatorios_nacionais.executar AC --metadados fonte_relatorios.json`

O arquivo de metadados é a resposta pública da API GitHub para a release `auditoria-v3-41263277696`, congelada no início da execução. O fluxo salva os scripts, o commit e os metadados junto dos resultados. As dependências de PDF têm versões fixadas no workflow.
