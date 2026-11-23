"""Medição da distância entre os resumos de dois arquivos."""
from dataclasses import dataclass
from pathlib import Path

from .hashing import ALGORITHMS
from .integrity import compare_files


@dataclass(frozen=True)
class Measurement:
    """Uma linha de resultados do experimento."""
    algorithm: str
    bits: int
    original: str
    modified: str
    changed: int
    percentage: float


def hamming(first: bytes, second: bytes) -> int:
    """Conte as posições binárias divergentes entre sequências de mesmo tamanho."""
    if len(first) != len(second):
        raise ValueError('Os resumos devem ter o mesmo tamanho.')
    return sum((a ^ b).bit_count() for a, b in zip(first, second))


def experiment(first: Path, second: Path) -> list[Measurement]:
    """Calcule os resumos e suas distâncias para todos os algoritmos."""
    rows = []
    for algorithm in ALGORITHMS:
        original, modified, _ = compare_files(first, second, algorithm)
        left = bytes.fromhex(original)
        bits = 8 * len(left)
        changed = hamming(left, bytes.fromhex(modified))
        rows.append(Measurement(algorithm, bits, original, modified,
                                changed, 100 * changed / bits))
    return rows
