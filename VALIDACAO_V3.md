# Correção do motor e estado da validação

## Validade dos resultados anteriores

As classificações do motor 2.1 e os rankings delas derivados foram retirados de uso para conclusões até reprocessamento. Isso inclui as listas históricas de 422 seções com proporção elevada de eventos de mesário e 64 com volume elevado. Os arquivos e as Releases antigas são preservados como evidência do histórico, não como resultados validados.

## Defeitos constatados em logs originais

1. O tipo biométrico pode ser registrado depois de “Eleitor foi habilitado”, antes do voto computado. A versão anterior classificava na abertura do ciclo e ignorava essa evidência tardia. Há 15 trechos reais dessa regressão, mais seis exemplos dirigidos de outras categorias e desfechos, em `validacao/casos_reais.json`, com hash do original, origem e linhas.
2. “Eleitor foi suspenso e não confirmou nenhum voto” não era reconhecido como desfecho explícito. Isso gerava habilitação sem voto sem explicar uma suspensão registrada. A suspensão parcial é distinta: só se conta voto computado quando a mensagem correspondente existe.
3. A deduplicação por linhas isoladas entre blocos não demonstrava que cada linha removida era uma cópia do mesmo evento. Agora somente blocos integralmente idênticos são removidos. Blocos distintos são preservados; suas fronteiras rompem ciclos e séries e a seção fica fora da comparação estatística.
4. Faltavam barreiras completas para reinício, troca de identificador de equipamento, regressão de relógio e registros inválidos. Evidências não atravessam essas fronteiras.

## Controles da versão 3.0

- Classificação no fechamento do ciclo, com evidência tardia e conflito preservado como indefinido. As mensagens de tipo e de autorização explícita são reconhecidas por padrões ancorados; uma frase citada ou negada não basta.
- Desfechos separados: voto computado, suspensão explícita sem voto, cancelamento explícito, interrupção e desfecho não explicado. Nenhum voto é inferido de uma confirmação parcial ou da falta de outra mensagem.
- Balanços: habilitações = ciclos com voto + suspensões sem voto + cancelamentos explícitos + ciclos não resolvidos; mensagens de voto computado = ciclos com voto + mensagens sem habilitação associada. Os resíduos ficam exportados.
- Quarentena para indefinições, tipos não suportados, conflitos, fronteiras não demonstradas, registros inválidos, relógio inconsistente e vínculos não resolvidos. Não entram na comparação estatística. Casos em quarentena não são acusados de fraude nem apagados.
- Fingerprint SHA-256 do motor, executor e verificador. Cache e consolidação recusam versões/fingerprints antigos.
- Manifesto SHA-256 dos arquivos de resultado. Cache, triagem e consolidação recusam conjuntos incompletos ou alterados. Isso não verifica assinatura criptográfica do TSE.
- Datas e campos validados. Pacotes não suportados ou danificados são erros explícitos, sem classificação presumida. O leitor atual suporta contêiner ZIP; um contêiner 7z genuíno não é silenciosamente tratado como ZIP.

## Evidência executada

Amostra de desenvolvimento de 188 logs do Amazonas: casos problemáticos, controles e amostras exploratórias. Não é amostra nacional independente para certificação. Os hashes dos originais estão no arquivo `validacao/resultado_corpus.json`; os originais podem ser reconstituídos com `preparar_amostra.py`.

| Indicador na amostra | Motor 2.1 | Motor 3.0 |
|---|---:|---:|
| Habilitações | 48.473 | 48.473 |
| Votos computados | 48.422 | 48.422 |
| Indefinidas | 15 | 0 |
| Avisos | 51 | 2 |
| Suspensões explícitas sem voto identificadas separadamente | não exportado | 49 |

Uma contagem implementada separadamente conferiu habilitações e votos em 165 logs com um único bloco distinto: nenhuma divergência. Os outros 23 não foram presumidos equivalentes para essa comparação. Não se confunde esse controle de contagens com um segundo classificador independente.

As duas interrupções restantes ocorreram nos arquivos `o03221am0229100110063-log.jez` e `o03221am0241000030230-log.jez`. O primeiro registra desligamento pela chave durante um ciclo; o segundo registra erro com mensagem de voto não registrado e desligamento. São preservados para revisão; o programa não inventa conclusão de voto nem vincula a sessão após reinício.

Os testes incluem ciclos com evidência tardia, suspensão parcial e sem voto, tentativas canceladas, mudança de equipamento, relógio, arquivo truncado, repetição legítima, blocos idênticos e distintos, registros inválidos, conflito, manifesto alterado e exclusão de versões antigas. Há 500 ciclos gerados com resultados conhecidos, além de 21 trechos reais congelados. Os exemplos reais cobrem biometria, autorização explícita de mesário, captura de nova digital de mesário, digital sem associação a mesário, confirmação de ano de nascimento, suspensão sem voto e suspensão parcial. Identificadores numéricos longos foram substituídos nos trechos de teste; hashes e linhas apontam ao original. O resultado integral da execução está em `validacao/testes.txt`. Um teste legado depende de arquivo externo ausente e permanece explicitamente pulado.

## O que falta para sustentar 99,9%

**Nenhuma acurácia de 99,9% foi certificada.** Não é possível garantir isso por testes unitários, por cobertura de linhas ou pela proporção de registros classificados. Quarentena evita conclusões automáticas em casos ambíguos, mas não prova que todos os casos aceitos estão corretos.

É necessária uma base de referência rotulada independentemente, congelada e separada do desenvolvimento, cobrindo modelos/versões de urna, estados, tipos de habilitação e contingências. É preciso medir erros de classificação e de vínculo por classe, além da cobertura de casos que o programa aceita e rejeita. BUs/RDVs e documentos de seção são verificações adicionais; igualdade entre contagens de log não certifica esses artefatos.

Como ilustração matemática, com zero erros em n observações independentes e representativas, o limite inferior unilateral binomial exato de 95% é 0,05^(1/n). Para esse limite atingir 0,999, seriam necessárias ao menos 2.995 observações. Isso exige as hipóteses de amostragem e unidade de erro corretas; ciclos da mesma seção não podem ser tratados automaticamente como independentes, e um conjunto quase todo biométrico não valida as classes raras. O corpus atual não atende a esse protocolo.

O relatório eleitoral final só deverá usar alertas recalculados depois do reprocessamento e informar cobertura, exclusões e validação efetivamente obtida. A análise computacional segue exploratória até a validação independente.

## Fonte técnica

A documentação oficial [Formato dos arquivos de log do TSE (2022)](https://www.tse.jus.br/eleicoes/eleicoes-2022/arquivos/formato-dos-arquivos-de-log-17-9-22/@@download/file/formato-arquivos-log.pdf) descreve arquivos internos e pacotes arquivados. É referência estrutural, não um dicionário completo ou certificação das mensagens de 2026. As correções semânticas acima foram baseadas nas mensagens observadas nos originais de 2026, cujos hashes e linhas estão preservados.
