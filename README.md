# SecureDocs — Missão 5

Biblioteca e CLI Python para investigar funções hash e verificar a integridade de arquivos. A aplicação calcula resumos MD5, SHA-1, SHA-2 e SHA-3, compara documentos e mede a distância de Hamming entre os resultados.

## Sumário

1. [Início rápido](#início-rápido) — Instale o pacote, calcule um hash e rode o experimento e os testes.
2. [Como executar](#como-executar) — Configure o ambiente no Windows, Linux ou macOS, consulte os comandos da CLI e interprete os retornos.
   - [Preparação](#preparação) · [Windows PowerShell](#windows-powershell) · [Linux e macOS](#linux-e-macos) · [Comandos](#comandos) · [Leitura dos resultados](#leitura-dos-resultados) · [Erros comuns](#erros-comuns)
3. [Uso da biblioteca](#uso-da-biblioteca) — Calcule e verifique hashes diretamente em código Python.
4. [Arquivos da entrega](#arquivos-da-entrega) — Encontre o código, os exemplos, os resultados, o relatório e a apresentação.
5. [Stack tecnológica](#stack-tecnológica) — Conheça as bibliotecas, a arquitetura, as dependências e os limites da solução.

## Início rápido

Requer Python 3.11 ou superior. Na raiz do projeto:

```console
python -m pip install .
python -m securedocs_hash texto "abc" -a sha256
python -m securedocs_hash demo exemplos/documento_original.txt exemplos/documento_modificado.txt
python -m unittest discover -s tests -v
```

## Como executar

### Preparação

1. Instale Python 3.11 ou superior com pip. O projeto foi testado no Windows com CPython 3.12.14.
2. Clone o repositório e entre na pasta do projeto. O GitHub exige acesso ao repositório privado.

   ```console
   git clone https://github.com/gsantanaoffsec/SecureDocs-Missao-5.git
   cd SecureDocs-Missao-5
   ```

   Se você já tiver o ZIP da entrega acadêmica, extraia `SecureDocs-Missao-5.zip` e abra a pasta que contém `pyproject.toml`. Se estiver na pasta que contém o ZIP, no PowerShell use `Expand-Archive -LiteralPath ./SecureDocs-Missao-5.zip -DestinationPath ./entrega`, seguido de `Set-Location ./entrega/SecureDocs-Missao-5`. Em Linux/macOS, use `unzip SecureDocs-Missao-5.zip -d entrega` e `cd entrega/SecureDocs-Missao-5`.

#### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install .
```

Se o PowerShell bloquear a ativação, chame `.\.venv\Scripts\python.exe` no lugar de `python`. Se `py` estiver indisponível, crie o ambiente com `python -m venv .venv`.

#### Linux e macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install .
```

O projeto não tem dependências externas de execução. O pip pode baixar setuptools para construir o pacote. Em ambiente sem acesso à rede e sem instalação, use `$env:PYTHONPATH = 'src'` no PowerShell ou `export PYTHONPATH=src` em Linux/macOS. Execute os comandos abaixo na raiz.

### Comandos

```console
python -m securedocs_hash --help
python -m securedocs_hash texto "abc" -a sha3-256
python -m securedocs_hash arquivo exemplos/contrato_original.pdf -a sha256
python -m securedocs_hash comparar exemplos/contrato_original.pdf exemplos/contrato_modificado.pdf
python -m securedocs_hash verificar exemplos/contrato_original.pdf 094de8d3da50a38b3e286fcab36ee1479a976b0ee2988bdd274e0586f8df4227
python -m securedocs_hash demo exemplos/documento_original.txt exemplos/documento_modificado.txt
python scripts/executar_experimento.py
python -m unittest discover -s tests -v
```

A instalação também disponibiliza o comando `securedocs`. Escolha o algoritmo com `-a`. Os identificadores aceitos são `md5`, `sha1`, `sha224`, `sha256`, `sha384`, `sha512`, `sha3-224`, `sha3-256`, `sha3-384` e `sha3-512`. O padrão é SHA-256.

### Leitura dos resultados

- **0** indica sucesso. Nas operações de comparação e verificação, indica também coincidência.
- **1** indica divergência entre os resumos. É o retorno esperado ao comparar os contratos de exemplo.
- **2** indica erro de entrada, leitura ou uso. Consulte a mensagem exibida no terminal.

No PowerShell, veja o código com `$LASTEXITCODE`. Em Linux/macOS, use `echo $?` imediatamente após o comando. A demonstração mostra os dois hashes completos, a distância de Hamming e o percentual de bits divergentes. O script atualiza os dois CSVs em `resultados/`. Use `--saida caminho` para gravá-los em outro diretório. A suíte registra 15 testes no ambiente usado para a entrega.

### Erros comuns

- **Módulo não encontrado.** Confirme que o interpretador do ambiente é o mesmo usado para instalar o pacote ou configure `PYTHONPATH` como acima.
- **Arquivo inexistente ou inacessível.** Confira a pasta atual, as permissões de leitura e as aspas em caminhos com espaços.
- **Resumo malformado.** Informe somente os dígitos hexadecimais, com o tamanho do algoritmo selecionado. SHA-256 requer 64 dígitos.
- **Algoritmo inválido.** Consulte `python -m securedocs_hash arquivo --help`. Alguns ambientes restringem algoritmos legados, mesmo em uso didático.
- **Hash diferente após copiar um texto.** Uma quebra de linha, um BOM ou uma mudança de codificação altera os bytes. Use o comando `arquivo` para preservar a entrada do experimento.

## Uso da biblioteca

```python
from securedocs_hash.hashing import hash_file
from securedocs_hash.integrity import verify_file

referencia = hash_file("exemplos/contrato_original.pdf", "sha256")
resumo, coincide = verify_file("exemplos/contrato_modificado.pdf", referencia)
```

SHA-256 é o padrão. MD5 e SHA-1 são opções didáticas e de compatibilidade. A verificação depende da procedência da referência. Em um fluxo real, obtenha o resumo por um canal autenticado ou valide uma assinatura digital antes de confiar no documento.

## Arquivos da entrega

- `src/securedocs_hash/` contém a biblioteca e a CLI.
- `tests/` contém os testes automatizados.
- `exemplos/` contém dois TXT e dois contratos fictícios em PDF.
- `scripts/executar_experimento.py` reproduz as duas tabelas CSV.
- `resultados/` inclui CSVs, gráfico e registros das execuções.
- `docs/` inclui o [relatório em PDF](docs/RELATORIO_ACADEMICO.pdf), o [relatório em DOCX](docs/RELATORIO_ACADEMICO.docx) e a [apresentação em PowerPoint](docs/APRESENTACAO_MISSAO_5.pptx).

## Stack tecnológica

### Execução

O projeto usa Python 3.11 ou superior. A validação ocorreu com CPython 3.12.14 no Windows, com OpenSSL 3.5.8. A biblioteca padrão cobre toda a execução da CLI, dos testes e da reprodução dos CSVs.

| Componente | Responsabilidade | Justificativa |
| --- | --- | --- |
| `hashlib` | Primitivas MD5, SHA-1, SHA-2 e SHA-3 | Usa implementações consolidadas do interpretador e fornece interface incremental uniforme |
| `argparse` | Subcomandos, opções, argumentos e ajuda | Padroniza validação de uso e mensagens de erro |
| `pathlib` | Caminhos e abertura binária | Melhora a portabilidade e preserva os bytes do arquivo |
| `hmac.compare_digest` e `re` | Comparação e validação de formato | Compara resumos de mesmo tamanho e rejeita referências malformadas |
| `dataclasses` e `csv` | Linhas de medições e saída tabular | Mantêm a estrutura de dados explícita e facilitam análise e auditoria |

O módulo `hashing` recebe bytes via leitura binária em blocos de 1 MiB ou codifica texto em UTF-8. O módulo `integrity` usa o motor de hash e compara a saída com outra saída calculada ou com um valor esperado. `avalanche` transforma cada par de hashes em bytes, aplica XOR e usa `int.bit_count()`. A CLI traduz as operações em mensagens e códigos de saída. Cada algoritmo lê os arquivos de forma independente durante o experimento.

### Desenvolvimento e distribuição

`unittest`, `tempfile`, `io` e `unittest.mock` permitem testar vetores, fluxos, formato e leituras em blocos sem dependências externas. `setuptools` é a dependência de construção do pacote. Nenhuma biblioteca externa é importada pela aplicação instalada.

### Geração dos materiais

ReportLab gerou os PDFs. Pillow gerou o gráfico. python-docx e python-pptx geraram os documentos editáveis. Essas ferramentas pertencem ao processo de autoria e são dispensáveis para executar o projeto e reproduzir os dois CSVs.

### Vantagens, limites e evolução

A memória da leitura binária é proporcional ao bloco. O tempo cresce com o tamanho do arquivo. Os resultados pressupõem arquivos estáveis durante a leitura. A comparação de digest verifica coincidência e depende tanto do algoritmo quanto da origem da referência. A implementação clássica do digest também não estabelece a identidade do emissor.

Para aplicar a solução ao produto, registre a identificação do algoritmo e vincule o resumo ao ID e à versão do documento em um manifesto autenticado. Um serviço que recebe documentos continuamente pode trabalhar com cópias imutáveis ou snapshots. Um protocolo entre serviços pode usar HMAC-SHA-256 com chaves protegidas. Para clientes independentes, a alternativa é validar uma assinatura digital com uma cadeia de confiança.
