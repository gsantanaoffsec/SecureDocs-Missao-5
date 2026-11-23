"""Interface de linha de comando do SecureDocs."""
import argparse
import sys
from pathlib import Path

from .avalanche import experiment
from .hashing import ALGORITHMS, hash_file, hash_text
from .integrity import compare_files, verify_file


def main(argv: list[str] | None = None) -> int:
    """Execute uma operação. Retorne 0, 1 para divergência ou 2 para erro."""
    parser = argparse.ArgumentParser(description='Verificação de integridade SecureDocs')
    commands = parser.add_subparsers(dest='command', required=True)
    text = commands.add_parser('texto')
    text.add_argument('texto')
    file = commands.add_parser('arquivo')
    file.add_argument('arquivo', type=Path)
    compare = commands.add_parser('comparar')
    compare.add_argument('original', type=Path)
    compare.add_argument('recebido', type=Path)
    verify = commands.add_parser('verificar')
    verify.add_argument('arquivo', type=Path)
    verify.add_argument('esperado')
    demo = commands.add_parser('demo')
    demo.add_argument('original', type=Path)
    demo.add_argument('modificado', type=Path)
    for command in (text, file, compare, verify):
        command.add_argument('-a', '--algoritmo', default='sha256', choices=ALGORITHMS)
    args = parser.parse_args(argv)
    try:
        if args.command == 'demo':
            print('Algoritmo | Bits | Hash original | Hash modificado | Bits diferentes | Percentual')
            for row in experiment(args.original, args.modificado):
                print(f'{row.algorithm} | {row.bits} | {row.original} | '
                      f'{row.modified} | {row.changed} | {row.percentage:.2f}%')
            return 0
        algorithm = args.algoritmo
        if algorithm in ('md5', 'sha1'):
            print('Aviso: algoritmo legado para estudo e compatibilidade.', file=sys.stderr)
        if args.command == 'texto':
            print(hash_text(args.texto, algorithm))
        elif args.command == 'arquivo':
            print(hash_file(args.arquivo, algorithm))
        elif args.command == 'comparar':
            left, right, matches = compare_files(args.original, args.recebido, algorithm)
            print(f'Original: {left}\nRecebido: {right}')
            print('Resumos coincidentes.' if matches else 'Resumos diferentes.')
            return 0 if matches else 1
        else:
            actual, matches = verify_file(args.arquivo, args.esperado, algorithm)
            print(f'Calculado: {actual}')
            print('Integridade compatível com a referência.' if matches else 'Integridade divergente.')
            return 0 if matches else 1
    except (OSError, ValueError) as error:
        print(f'Erro: {error}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
