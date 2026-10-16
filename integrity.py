"""Small-file hashing and MD5 integrity-demo helpers."""
from __future__ import annotations

import hmac
from pathlib import Path

from md5_core import md5


def hash_file(path: str | Path) -> str:
    """Read a file as bytes and return its MD5 digest (educational demo)."""
    file_path = Path(path)
    data = file_path.read_bytes()
    return str(md5(data))


def verify_file(path: str | Path, expected_digest: str) -> tuple[bool, str]:
    """Compare a file's calculated digest to a supplied reference digest.

    This only detects accidental/unauthorized modification when the reference
    digest itself is trusted. MD5 is not safe against deliberate collision attacks.
    """
    actual = hash_file(path)
    normalized_expected = expected_digest.strip().lower()
    is_hex_digest = len(normalized_expected) == 32 and all(ch in "0123456789abcdef" for ch in normalized_expected)
    matched = is_hex_digest and hmac.compare_digest(actual, normalized_expected)
    return matched, actual
