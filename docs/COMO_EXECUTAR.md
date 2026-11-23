# Como executar o SecureDocs

## Preparação

1. Instale Python 3.11 ou superior com pip. O projeto foi testado no Windows com CPython 3.12.14.
2. Extraia `SecureDocs-Missao-5.zip` e abra o terminal na pasta extraída que contém `pyproject.toml`. Se estiver na pasta que contém o ZIP, no PowerShell use `Expand-Archive -LiteralPath ./SecureDocs-Missao-5.zip -DestinationPath ./entrega`, seguido de `Set-Location ./entrega/SecureDocs-Missao-5`. Em Linux/macOS, use `unzip SecureDocs-Missao-5.zip -d entrega` e `cd entrega/SecureDocs-Missao-5`.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install .
```

Se o PowerShell bloquear a ativação, chame `.\.venv\Scripts\python.exe` no lugar de `python`. Se `py` estiver indisponível, crie o ambiente com `python -m venv .venv`.

### Linux e macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install .
```

O projeto não tem dependências externas de execução. O pip pode baixar setuptools para construir o pacote. Em ambiente sem acesso à rede e sem instalação, use `$env:PYTHONPATH = 'src'` no PowerShell ou `export PYTHONPATH=src` em Linux/macOS. Execute os comandos abaixo na raiz.

## Comandos

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

## Leitura dos resultados

- **0** indica sucesso. Nas operações de comparação e verificação, indica também coincidência.
- **1** indica divergência entre os resumos. É o retorno esperado ao comparar os contratos de exemplo.
- **2** indica erro de entrada, leitura ou uso. Consulte a mensagem exibida no terminal.

No PowerShell, veja o código com `$LASTEXITCODE`. Em Linux/macOS, use `echo $?` imediatamente após o comando. A demonstração mostra os dois hashes completos, a distância de Hamming e o percentual de bits divergentes. O script atualiza os dois CSVs em `resultados/`. Use `--saida caminho` para gravá-los em outro diretório. A suíte registra 15 testes no ambiente usado para a entrega.

## Erros comuns

- **Módulo não encontrado.** Confirme que o interpretador do ambiente é o mesmo usado para instalar o pacote ou configure `PYTHONPATH` como acima.
- **Arquivo inexistente ou inacessível.** Confira a pasta atual, as permissões de leitura e as aspas em caminhos com espaços.
- **Resumo malformado.** Informe somente os dígitos hexadecimais, com o tamanho do algoritmo selecionado. SHA-256 requer 64 dígitos.
- **Algoritmo inválido.** Consulte `python -m securedocs_hash arquivo --help`. Alguns ambientes restringem algoritmos legados, mesmo em uso didático.
- **Hash diferente após copiar um texto.** Uma quebra de linha, um BOM ou uma mudança de codificação altera os bytes. Use o comando `arquivo` para preservar a entrada do experimento.
