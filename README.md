# SecureDocs — Missão 5

Biblioteca e CLI Python para investigar funções hash e verificar a integridade de arquivos. A aplicação calcula resumos MD5, SHA-1, SHA-2 e SHA-3, compara documentos e mede a distância de Hamming entre os resultados.

## Início rápido

Requer Python 3.11 ou superior. Na raiz extraída:

```console
python -m pip install .
python -m securedocs_hash texto "abc" -a sha256
python -m securedocs_hash demo exemplos/documento_original.txt exemplos/documento_modificado.txt
python -m unittest discover -s tests -v
```

Em [COMO_EXECUTAR.md](docs/COMO_EXECUTAR.md) estão a configuração do ambiente, os comandos e os códigos de saída. A [stack tecnológica](docs/STACK_TECNOLOGICA.md) descreve as decisões técnicas.

## Arquivos da entrega

- `src/securedocs_hash/` contém a biblioteca e a CLI.
- `tests/` contém os testes automatizados.
- `exemplos/` contém dois TXT e dois contratos fictícios em PDF.
- `scripts/executar_experimento.py` reproduz as duas tabelas CSV.
- `resultados/` inclui CSVs, gráfico e registros das execuções.
- `docs/` inclui o relatório em PDF e DOCX e a apresentação em PowerPoint.

## Uso da biblioteca

```python
from securedocs_hash.hashing import hash_file
from securedocs_hash.integrity import verify_file

referencia = hash_file("exemplos/contrato_original.pdf", "sha256")
resumo, coincide = verify_file("exemplos/contrato_modificado.pdf", referencia)
```

SHA-256 é o padrão. MD5 e SHA-1 são opções didáticas e de compatibilidade. A verificação depende da procedência da referência. Em um fluxo real, obtenha o resumo por um canal autenticado ou valide uma assinatura digital antes de confiar no documento.
