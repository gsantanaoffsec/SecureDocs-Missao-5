"""Cálculo incremental de resumos criptográficos."""
import hashlib
from pathlib import Path

ALGORITHMS = {
    'md5': 'md5', 'sha1': 'sha1',
    **{f'sha{size}': f'sha{size}' for size in (224, 256, 384, 512)},
    **{f'sha3-{size}': f'sha3_{size}' for size in (224, 256, 384, 512)},
}
BLOCK_SIZE = 1024 * 1024


def _new(algorithm: str):
    name = ALGORITHMS.get(algorithm)
    if name is None:
        raise ValueError(f'Algoritmo inválido: {algorithm}')
    return hashlib.new(name, usedforsecurity=algorithm not in ('md5', 'sha1'))


def digest_size(algorithm: str) -> int:
    """Retorne o tamanho do resumo em bytes."""
    return _new(algorithm).digest_size


def hash_text(value: str, algorithm: str = 'sha256') -> str:
    """Calcule o resumo hexadecimal do texto codificado em UTF-8."""
    digest = _new(algorithm)
    digest.update(value.encode('utf-8'))
    return digest.hexdigest()


def hash_file(path: str | Path, algorithm: str = 'sha256',
              block_size: int = BLOCK_SIZE) -> str:
    """Calcule o resumo dos bytes do arquivo com memória limitada."""
    if block_size <= 0:
        raise ValueError('O tamanho do bloco deve ser positivo.')
    digest = _new(algorithm)
    with Path(path).open('rb') as stream:
        while block := stream.read(block_size):
            digest.update(block)
    return digest.hexdigest()
