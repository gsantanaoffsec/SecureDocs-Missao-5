"""Comparação de arquivos e verificação contra uma referência."""
import re
from hmac import compare_digest
from pathlib import Path

from .hashing import digest_size, hash_file


def compare_files(first: str | Path, second: str | Path,
                  algorithm: str = 'sha256') -> tuple[str, str, bool]:
    """Retorne os dois resumos e a indicação de coincidência."""
    left = hash_file(first, algorithm)
    right = hash_file(second, algorithm)
    return left, right, compare_digest(left, right)


def verify_file(path: str | Path, expected: str,
                algorithm: str = 'sha256') -> tuple[str, bool]:
    """Valide a referência hexadecimal e compare-a com o resumo calculado."""
    width = 2 * digest_size(algorithm)
    if not re.fullmatch(r'[0-9a-fA-F]{%d}' % width, expected):
        raise ValueError(f'O resumo esperado deve ter {width} dígitos hexadecimais.')
    actual = hash_file(path, algorithm)
    return actual, compare_digest(actual, expected.lower())
