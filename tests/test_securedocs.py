"""Vetores conhecidos e testes de integração da biblioteca."""
import contextlib
import hashlib
import io
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from securedocs_hash.avalanche import experiment, hamming
from securedocs_hash.cli import main
from securedocs_hash.hashing import hash_file, hash_text
from securedocs_hash.integrity import compare_files, verify_file

ABC = 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'


class ObservedStream(io.BytesIO):
    """Registre o tamanho solicitado em cada leitura."""
    def __init__(self, payload: bytes):
        super().__init__(payload)
        self.requests = []

    def read(self, size: int = -1) -> bytes:
        self.requests.append(size)
        return super().read(size)


class TestSecureDocs(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        directory = Path(temporary.name)
        self.one = directory / 'one.txt'
        self.two = directory / 'two.txt'
        self.one.write_bytes(b'abc')
        self.two.write_bytes(b'abc')

    def test_known_text(self):
        self.assertEqual(hash_text('abc'), ABC)
        self.assertEqual(hash_text('abc', 'md5'), '900150983cd24fb0d6963f7d28e17f72')
        self.assertEqual(hash_text('abc', 'sha3-256'),
                         '3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532')

    def test_utf8(self):
        self.assertEqual(hash_text('ação'), hashlib.sha256('ação'.encode()).hexdigest())

    def test_file(self):
        self.assertEqual(hash_file(self.one), ABC)

    def test_same(self):
        self.assertEqual(compare_files(self.one, self.two), (ABC, ABC, True))

    def test_different(self):
        self.two.write_bytes(b'abd')
        self.assertFalse(compare_files(self.one, self.two)[2])

    def test_empty(self):
        self.two.write_bytes(b'')
        self.assertEqual(hash_file(self.two),
                         'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')

    def test_missing(self):
        with self.assertRaises(FileNotFoundError):
            hash_file(self.one.with_name('missing'))

    def test_invalid_algorithm(self):
        with self.assertRaises(ValueError):
            hash_text('abc', 'crc32')

    def test_correct_reference(self):
        self.assertEqual(verify_file(self.one, ABC.upper()), (ABC, True))

    def test_incorrect_reference(self):
        self.assertEqual(verify_file(self.one, '0' * 64), (ABC, False))

    def test_malformed_reference(self):
        for reference in ('g' * 64, 'a' * 63, ABC + '\n'):
            with self.subTest(reference=reference), self.assertRaises(ValueError):
                verify_file(self.one, reference)

    def test_one_character(self):
        self.two.write_bytes(b'abd')
        left, right = (path.read_text(encoding='utf-8') for path in (self.one, self.two))
        self.assertEqual(len(left), len(right))
        self.assertEqual(sum(a != b for a, b in zip(left, right)), 1)
        rows = experiment(self.one, self.two)
        self.assertEqual(len(rows), 10)
        for row in rows:
            with self.subTest(algorithm=row.algorithm):
                parameters = {'usedforsecurity': row.algorithm not in ('md5', 'sha1')}
                name = row.algorithm.replace('-', '_')
                a = hashlib.new(name, b'abc', **parameters).hexdigest()
                b = hashlib.new(name, b'abd', **parameters).hexdigest()
                self.assertEqual((row.original, row.modified), (a, b))
                self.assertGreater(row.changed, 0)
                self.assertAlmostEqual(row.percentage, 100 * row.changed / row.bits)

    def test_hamming(self):
        self.assertEqual(hamming(b'\x00\xff', b'\x0f\x00'), 12)
        with self.assertRaises(ValueError):
            hamming(b'', b'\x00')

    def test_blocks(self):
        stream = ObservedStream(b'abc')
        with patch.object(Path, 'open', return_value=stream):
            self.assertEqual(hash_file(self.one, block_size=2), ABC)
        self.assertEqual(stream.requests, [2, 2, 2])
        with self.assertRaises(ValueError):
            hash_file(self.one, block_size=0)

    def test_cli_exit_codes(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(['verificar', str(self.one), ABC]), 0)
            self.assertEqual(main(['verificar', str(self.one), '0' * 64]), 1)
            self.assertEqual(main(['verificar', str(self.one), 'abc']), 2)
            self.assertEqual(main(['arquivo', str(self.one.with_name('missing'))]), 2)
