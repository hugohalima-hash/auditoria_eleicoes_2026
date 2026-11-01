# Execução nacional persistente

A execução usa `ubuntu-24.04` padrão no repositório público, com duas unidades simultâneas, sem executores pagos ou auto-hospedados. O workflow recusa repositório privado. A documentação do GitHub informa que os executores padrão são gratuitos em repositórios públicos: https://docs.github.com/en/actions/reference/runners/github-hosted-runners

O workflow inicia ao publicar ou alterar seu arquivo na branch main, ou por acionamento manual. Uma trava impede execuções nacionais sobrepostas. O código usado fica congelado no commit da execução, com fingerprint e cópia das fontes em uma Release marcada como prévia. A execução não depende de a conversa continuar aberta.

## Por estado

1. Analisa os logs com o motor corrigido, em um processo de análise por UF.
2. Confere manifesto, erros e total de logs processados.
3. Compara contagens literais por leitor independente onde aplicável. Isso não certifica acurácia semântica de 99,9%.
4. Recalcula a triagem, preservando as exclusões e seus motivos.
5. Preserva originais de todos os casos em quarentena e até cem controles determinísticos, com hashes. O pacote bruto completo fica disponível na URL oficial e seu SHA-256 é registrado pela conferência. O executor mantém o pacote até concluir as verificações; não depende de guardar todos os pacotes brutos simultaneamente.
6. Publica CSVs, JSONs, conferências e originais selecionados em um ZIP estadual anexado à Release da execução. Falhas também geram diagnóstico; não se apresentam como processamento completo.

Os resultados estaduais são gravados após cada UF. Uma UF com falha não interrompe as demais. A consolidação nacional só ocorre após sucesso das 28 unidades e verifica hashes dos pacotes e manifestos antes de combinar os resultados. As triagens estaduais não são sobrescritas entre si: a nacional é recalculada a partir dos resultados conferidos.

O workflow libera ferramentas preinstaladas sem uso no executor descartável e mantém a reserva de disco do auditor. Se o espaço não for suficiente, a UF falha explicitamente; não é omitida nem imputada como zero. Falhas podem ser retomadas pelo GitHub Actions sem apagar os pacotes das UFs já concluídas.

## Memória e rastreabilidade

A exportação estadual de séries passou a escrever um log por vez, evitando acumular todas as séries de estados grandes na memória. O CSV estadual fica em ordem de arquivo, preservando campos e contagens. O ranking consolidado nacional permanece ordenado por tamanho. Um teste de integração verifica exportação e reaproveitamento de cache compatível. Como o executor mudou, o fingerprint mudou e nenhum cache de outro fingerprint é aceito.

As listas do motor 2.1 permanecem históricas e suspensas para conclusões. A execução nacional recalcula os alertas; não certifica fraude nem acurácia de 99,9%.
