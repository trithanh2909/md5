"""Tests: RFC 1321 vectors plus additional boundary/Unicode/file-like cases."""
from __future__ import annotations

import hashlib
import sys
import unittest
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from md5_core import md5, md5_text  # noqa: E402
from integrity import hash_file, verify_file  # noqa: E402


class TestMD5RFC1321(unittest.TestCase):
    def test_rfc_1321_known_vectors(self) -> None:
        vectors = [
            (b"", "d41d8cd98f00b204e9800998ecf8427e"),
            (b"a", "0cc175b9c0f1b6a831c399e269772661"),
            (b"abc", "900150983cd24fb0d6963f7d28e17f72"),
            (b"message digest", "f96b697d7cb7938d525a2f31aaf161d0"),
            (b"abcdefghijklmnopqrstuvwxyz", "c3fcd3d76192e4007dfb496cca67e13b"),
            (b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
             "d174ab98d277d9f5a5611c2c9f419d9f"),
            (b"1234567890" * 8, "57edf4a22be3c955ac49da2e2107b67a"),
        ]
        for message, expected in vectors:
            with self.subTest(message=message[:24]):
                self.assertEqual(md5(message), expected)

    def test_boundary_lengths_against_standard_library(self) -> None:
        # Includes the 55/56-byte padding boundary and 64-byte block boundary.
        for length in (0, 1, 2, 3, 54, 55, 56, 57, 63, 64, 65, 127, 128, 129, 1000):
            data = b"a" * length
            with self.subTest(length=length):
                self.assertEqual(md5(data), hashlib.md5(data).hexdigest())

    def test_all_byte_values_and_multiple_blocks(self) -> None:
        data = bytes(range(256)) * 4
        self.assertEqual(md5(data), hashlib.md5(data).hexdigest())

    def test_utf8_text(self) -> None:
        text = "Xin chào mạng máy tính – MD5"
        self.assertEqual(md5_text(text), hashlib.md5(text.encode("utf-8")).hexdigest())

    def test_trace_has_64_steps_for_one_block(self) -> None:
        digest, rows = md5(b"abc", trace=True)
        self.assertEqual(len(rows), 64)
        self.assertEqual([row["step"] for row in rows], list(range(1, 65)))
        self.assertEqual(digest, "900150983cd24fb0d6963f7d28e17f72")


    def test_file_integrity_check_detects_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "sample.txt"
            path.write_bytes(b"original content")
            reference = hash_file(path)
            matched, actual = verify_file(path, reference)
            self.assertTrue(matched)
            self.assertEqual(actual, hashlib.md5(b"original content").hexdigest())

            path.write_bytes(b"modified content")
            matched_after_change, changed_digest = verify_file(path, reference)
            self.assertFalse(matched_after_change)
            self.assertNotEqual(changed_digest, reference)

    def test_rejects_string_in_core_api(self) -> None:
        with self.assertRaises(TypeError):
            md5("abc")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main(verbosity=2)
