# Auditor Eleitoral Independente 2026 — versão 2.1

Análise exploratória dos **logs públicos do segundo turno de 25/10/2026**, durante todo o dia. Detecta sequências consecutivas de habilitações, registra os eventos de voto computado e verifica a cobertura contra o cadastro oficial de seções principais.

O programa foi criado nesta conversa e corrigido após a validação do arquivo enviado pelo usuário. Não executa o DataUrnas-BR nem incorpora código desse projeto. Utiliza a biblioteca padrão do Python 3.11 ou posterior. É uma auditoria computacional de registros públicos, não uma perícia física nem uma autenticação da identidade dos votantes.

## Executar

Mantenha `auditar.py`, `motor.py` e `lote.py` na mesma pasta.

```powershell
python auditar.py --ufs AC --saida resultados
python auditar.py --ufs SP MG --saida resultados
python auditar.py --brasil --saida resultados --apagar-pacotes
python auditar.py --arquivos urna-log.jez --saida teste --eventos
```

O modo Brasil inclui 26 estados, o Distrito Federal e a UF ZZ (exterior). O download é retomável e usa faixas HTTP verificadas pelo cabeçalho Content-Range, pelo tamanho e pelo ETag. Cada faixa é persistida antes de marcar a conclusão. O padrão conservador usa um estado por vez, quatro conexões HTTP e um processo de análise. No Linux, o processo principal tem limite padrão de 1536 MiB de memória virtual. As transferências são agrupadas em blocos de até 32 MiB. A execução fica suspensa se atingir a reserva mínima de 6 GiB livres.

`--apagar-pacotes` remove cada ZIP oficial baixado após o processamento sem erros de leitura. Relatórios, hashes SHA-256 por log, configurações oficiais e checkpoints são preservados. **Não use essa opção se precisar manter uma cópia bruta local de cada pacote.** Somente os ZIPs baixados pelo modo estadual são removidos; arquivos passados por `--arquivos` não são apagados. Uma análise incompleta ou com ressalvas de classificação não equivale a erro de descompactação.

## Categorias separadas

| Coluna | Evidência usada no log |
|---|---|
| `biometrica` | Mensagem explícita de tipo de habilitação biométrica. |
| `mesario_explicito` | Mensagem de que o mesário habilitou o eleitor. |
| `digital_mesario_gravada` | Captura da digital do mesário e indicação de gravação de uma digital nova antes da habilitação. Não significa que a digital foi reconhecida como a de um mesário cadastrado. |
| `digital_mesario_sem_associacao` | Mensagem explícita de que não foi possível associar a habilitação a um mesário. |
| `ano_nascimento_sem_evento_biometrico` | Ano de nascimento confirmado, sem tipo biométrico nem solicitação/captura biométrica reconhecida nessa tentativa. É uma categoria inferida e não confirma a situação cadastral biométrica do eleitor. |
| `tipo_outro` | Tipo de habilitação explícito que ainda não foi mapeado. |
| `indefinida` | Ausência de evidências suficientes para as categorias anteriores. |

`com_evento_mesario` soma as três categorias de eventos de mesário. `sem_evento_biometrico` inclui também a categoria inferida pelo ano de nascimento. **Esses dois totais não são intercambiáveis, nem equivalem automaticamente ao indicador de eleitores com biometria cadastrada que votaram sem reconhecimento do BU.** A coluna `_com_voto` exige que a habilitação tenha sido seguida por um evento de voto computado vinculado pelo parser. Os totais de habilitações também incluem tentativas sem conclusão registrada.

## Sequências e horários

As sequências são contadas na ordem dos eventos de habilitação. Uma tentativa biométrica malsucedida anterior à habilitação não interrompe a sequência. Uma habilitação biométrica, de tipo desconhecido ou fora do grupo interrompe a sequência. Troca de equipamento, retrocesso de horário ou ajuste explícito do relógio também interrompem a sequência. Há duas análises: eventos de mesário e o grupo ampliado sem evento biométrico reconhecido. Ambas têm uma coluna específica para sequências cujas habilitações foram vinculadas a voto computado.

Os horários do relatório são **os do relógio registrado no log**, sem conversão automática para Brasília. O horário de uma habilitação é diferente do horário anterior de autorização do mesário. Nenhuma sequência permite identificar o candidato escolhido.

A coluna `inicios_esperados_ge_max_*` é o número esperado de inícios de sequências com comprimento pelo menos igual ao máximo observado, sob permutação uniforme com as quantidades de habilitações e de eventos do grupo fixas. Não é p-valor, não corrige a multiplicidade de centenas de milhares de comparações e não modela mudanças de fluxo, problemas de equipamentos ou dependência temporal. Não deve ser interpretada como probabilidade de fraude.

## Arquivos de saída por UF

- `resumo.json`: totais, cobertura e ressalvas.
- `urnas.csv`: uma linha por arquivo de log, com zona, seção, município, hashes, contagens e sequências.
- `sequencias.csv`: início, fim, intervalos, categorias e referências às linhas de origem para sequências de duas ou mais habilitações.
- `avisos.csv`: votos sem habilitação vinculável e habilitações sem desfecho reconhecido.
- `erros.csv`: falhas de leitura ou descompactação; vazio não significa ausência de outras ressalvas.
- `lacunas_cobertura.csv`: seções do pacote ou da configuração sem log processado.
- `config_oficial.json`: cópia da configuração oficial usada na conferência de cobertura.
- `checkpoint.sqlite`: retomada local, sem publicação de identificadores pessoais.
- `habilitacoes.jsonl`: opcional, gerado no modo local com `--eventos`.

A extração lê `logd.dat` e os arquivos .jez aninhados, incluindo logs de equipamentos substituídos. Cópias idênticas de linhas entre arquivos são eliminadas por multiplicidade máxima, preservando repetições existentes no mesmo arquivo. O CRC-32 dos membros é verificado pela biblioteca ZIP. Há limite de 256 MiB descompactados por pacote de log e de seis níveis de aninhamento.

## Cobertura e limitações

A configuração oficial é `https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3221/config/{uf}/{uf}-p003221-cs.json`. Seções agregadas são separadas das principais. O cadastro pode conter seções não instaladas ou cujo resultado veio do sistema de apuração; uma lacuna precisa ser examinada, não rotulada automaticamente como irregularidade.

Os pacotes estaduais são os do conjunto Arquivos transmitidos para totalização do TSE, restrito aos arquivos em situação Totalizado:
https://dadosabertos.tse.jus.br/dataset/resultados-2026-arquivos-transmitidos-para-totalizacao

**Cobertura de 100% de uma lista não significa ausência de falhas de classificação nem auditoria de 100% da eleição.** Os registros públicos não demonstram por si só a presença física ou a identidade de cada eleitor. O programa não confere assinaturas criptográficas, não decodifica os BUs para reconciliar seus indicadores, não verifica hardware ou software instalado e não confirma a intenção de voto. Sequências longas, duração curta e alta frequência são descrições operacionais; isoladamente não comprovam fraude. Resultados com categorias indefinidas ou avisos permanecem acompanhados dessas ressalvas.

## Validação

```powershell
python -m unittest -v test_motor test_lote
```

Os testes verificam as mensagens alternativas de mesário, o isolamento de tentativas canceladas, a interrupção das sequências por categoria desconhecida, a deduplicação de logs aninhados e a fórmula de referência estatística por enumeração exata. O teste da amostra externa depende da presença do arquivo enviado e é pulado quando a amostra não está disponível.

## Consolidação e proteção de armazenamento

Use `python consolidar.py --resultados resultados --saida entrega` para gerar o relatório e o ZIP por UF. Resultados de outras versões ou UFs não processadas não são imputados. A execução final usa dois estados simultâneos; o download suspende novas faixas ao atingir uma reserva mínima de 6 GiB livres.


## Configuração segura usada na execução final

No Linux: `MALLOC_ARENA_MAX=2 python auditar.py --brasil --saida resultados --estados-simultaneos 1 --conexoes 4 --processos 1 --limite-memoria-mib 1536 --apagar-pacotes`. O processo principal fica limitado a 1,5 GiB de memória virtual, sem processos auxiliares. As threads reservam pilhas de 1 MiB e a configuração MALLOC_ARENA_MAX reduz reservas virtuais do alocador glibc. Não existem cópias duplicadas dos pacotes em outra pasta temporária. O cache de cada UF é removido após processamento sem erros de leitura.

Os testes de memória identificaram e corrigiram uma referência cíclica no leitor. Em uma validação local sequencial de 5.000 logs reais do RJ, com limite de 1 GiB, o pico RSS permaneceu em 166,6 MiB. Nove testes de regressão foram aprovados. O limite de memória usa o módulo resource quando disponível; esse módulo não existe em algumas plataformas, inclusive Windows.
