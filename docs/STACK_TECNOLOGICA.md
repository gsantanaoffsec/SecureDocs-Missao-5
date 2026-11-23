# Stack tecnológica do SecureDocs

## Execução

O projeto usa Python 3.11 ou superior. A validação ocorreu com CPython 3.12.14 no Windows, com OpenSSL 3.5.8. A biblioteca padrão cobre toda a execução da CLI, dos testes e da reprodução dos CSVs.

| Componente | Responsabilidade | Justificativa |
| --- | --- | --- |
| `hashlib` | Primitivas MD5, SHA-1, SHA-2 e SHA-3 | Usa implementações consolidadas do interpretador e fornece interface incremental uniforme |
| `argparse` | Subcomandos, opções, argumentos e ajuda | Padroniza validação de uso e mensagens de erro |
| `pathlib` | Caminhos e abertura binária | Melhora a portabilidade e preserva os bytes do arquivo |
| `hmac.compare_digest` e `re` | Comparação e validação de formato | Compara resumos de mesmo tamanho e rejeita referências malformadas |
| `dataclasses` e `csv` | Linhas de medições e saída tabular | Mantêm a estrutura de dados explícita e facilitam análise e auditoria |

O módulo `hashing` recebe bytes via leitura binária em blocos de 1 MiB ou codifica texto em UTF-8. O módulo `integrity` usa o motor de hash e compara a saída com outra saída calculada ou com um valor esperado. `avalanche` transforma cada par de hashes em bytes, aplica XOR e usa `int.bit_count()`. A CLI traduz as operações em mensagens e códigos de saída. Cada algoritmo lê os arquivos de forma independente durante o experimento.

## Desenvolvimento e distribuição

`unittest`, `tempfile`, `io` e `unittest.mock` permitem testar vetores, fluxos, formato e leituras em blocos sem dependências externas. `setuptools` é a dependência de construção do pacote. Nenhuma biblioteca externa é importada pela aplicação instalada.

## Geração dos materiais

ReportLab gerou os PDFs. Pillow gerou o gráfico. python-docx e python-pptx geraram os documentos editáveis. Essas ferramentas pertencem ao processo de autoria e são dispensáveis para executar o projeto e reproduzir os dois CSVs.

## Vantagens, limites e evolução

A memória da leitura binária é proporcional ao bloco. O tempo cresce com o tamanho do arquivo. Os resultados pressupõem arquivos estáveis durante a leitura. A comparação de digest verifica coincidência e depende tanto do algoritmo quanto da origem da referência. A implementação clássica do digest também não estabelece a identidade do emissor.

Para aplicar a solução ao produto, registre a identificação do algoritmo e vincule o resumo ao ID e à versão do documento em um manifesto autenticado. Um serviço que recebe documentos continuamente pode trabalhar com cópias imutáveis ou snapshots. Um protocolo entre serviços pode usar HMAC-SHA-256 com chaves protegidas. Para clientes independentes, a alternativa é validar uma assinatura digital com uma cadeia de confiança.
