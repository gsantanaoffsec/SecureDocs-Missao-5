"""Reexecute os experimentos de texto e PDF e exporte dois CSVs."""
import argparse
import csv
from dataclasses import astuple
from pathlib import Path

from securedocs_hash.avalanche import experiment

ROOT = Path(__file__).resolve().parents[1]
HEADERS = ('algoritmo', 'bits', 'hash_original', 'hash_modificado',
           'bits_diferentes', 'percentual')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--saida', type=Path, default=ROOT / 'resultados')
    args = parser.parse_args()
    examples = ROOT / 'exemplos'
    first = examples / 'documento_original.txt'
    second = examples / 'documento_modificado.txt'
    left, right = (path.read_bytes().decode('utf-8') for path in (first, second))
    if len(left) != len(right) or sum(a != b for a, b in zip(left, right)) != 1:
        parser.error('Os TXT devem diferir por exatamente um caractere.')
    args.saida.mkdir(parents=True, exist_ok=True)
    pairs = {
        'comparacao_hashes.csv': (first, second),
        'comparacao_pdfs.csv': (examples / 'contrato_original.pdf',
                               examples / 'contrato_modificado.pdf'),
    }
    for name, (original, modified) in pairs.items():
        with (args.saida / name).open('w', encoding='utf-8', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(HEADERS)
            for row in experiment(original, modified):
                writer.writerow((*astuple(row)[:-1], f'{row.percentage:.4f}'))
        print(args.saida / name)


if __name__ == '__main__':
    main()
