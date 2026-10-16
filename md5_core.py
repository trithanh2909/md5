"""Educational MD5 implementation based on RFC 1321.

WARNING: MD5 is cryptographically broken for collision resistance. This module
is for coursework and interoperability demonstrations only, not new security
applications.

The core implementation deliberately does NOT call hashlib.md5 or another
cryptographic library. hashlib is used only by the test suite as an oracle.
"""
from __future__ import annotations

import math
import struct
from typing import Any

_MASK32 = 0xFFFFFFFF

# RFC 1321 rotation schedule, 4 rounds x 16 steps.
_SHIFT = (
    [7, 12, 17, 22] * 4
    + [5, 9, 14, 20] * 4
    + [4, 11, 16, 23] * 4
    + [6, 10, 15, 21] * 4
)

# T[i] = floor(2^32 * abs(sin(i))), i = 1..64 (RFC 1321).
_K = [int(abs(math.sin(i + 1)) * (1 << 32)) & _MASK32 for i in range(64)]

# RFC 1321 initial chaining state, represented as four 32-bit words.
_INITIAL_STATE = (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476)


def _left_rotate(value: int, amount: int) -> int:
    """Rotate a 32-bit integer left by amount bits."""
    value &= _MASK32
    return ((value << amount) | (value >> (32 - amount))) & _MASK32


def _pad(message: bytes) -> bytes:
    """Apply MD5 padding: 1 bit, zero bits, then original length in little-endian."""
    original_length_bits = (len(message) * 8) & 0xFFFFFFFFFFFFFFFF
    padded = bytearray(message)
    padded.append(0x80)  # binary 10000000: the first padding bit is 1
    while len(padded) % 64 != 56:
        padded.append(0)
    padded.extend(struct.pack("<Q", original_length_bits))
    return bytes(padded)


def md5(message: bytes, *, trace: bool = False) -> str | tuple[str, list[dict[str, Any]]]:
    """Return the MD5 digest as 32 lowercase hexadecimal characters.

    Args:
        message: Raw input bytes. Encode text to bytes before calling this function.
        trace: If True, also return the intermediate registers after every step.

    Returns:
        Digest string, or (digest string, trace rows) if trace=True.
    """
    if not isinstance(message, (bytes, bytearray, memoryview)):
        raise TypeError("md5() expects bytes-like input; encode text with UTF-8 first")

    data = _pad(bytes(message))
    a0, b0, c0, d0 = _INITIAL_STATE
    trace_rows: list[dict[str, Any]] = []

    for block_index in range(0, len(data), 64):
        block = data[block_index : block_index + 64]
        words = struct.unpack("<16I", block)  # sixteen 32-bit little-endian words

        a, b, c, d = a0, b0, c0, d0

        for i in range(64):
            if i < 16:
                function = (b & c) | ((~b) & d)
                word_index = i
                round_number = 1
            elif i < 32:
                function = (d & b) | ((~d) & c)
                word_index = (5 * i + 1) % 16
                round_number = 2
            elif i < 48:
                function = b ^ c ^ d
                word_index = (3 * i + 5) % 16
                round_number = 3
            else:
                function = c ^ (b | (~d))
                word_index = (7 * i) % 16
                round_number = 4

            # Addition is modulo 2^32; Python integers do not overflow by default.
            mixed = (a + function + _K[i] + words[word_index]) & _MASK32
            rotated = _left_rotate(mixed, _SHIFT[i])

            # Move the four working registers according to RFC 1321.
            old_a, old_b, old_c, old_d = a, b, c, d
            a = old_d
            b = (old_b + rotated) & _MASK32
            c = old_b
            d = old_c

            if trace:
                trace_rows.append({
                    "block": block_index // 64 + 1,
                    "step": i + 1,
                    "round": round_number,
                    "word_index": word_index,
                    "A": f"{a:08x}",
                    "B": f"{b:08x}",
                    "C": f"{c:08x}",
                    "D": f"{d:08x}",
                })

        # Feed-forward: add the working state to the previous chaining state.
        a0 = (a0 + a) & _MASK32
        b0 = (b0 + b) & _MASK32
        c0 = (c0 + c) & _MASK32
        d0 = (d0 + d) & _MASK32

    digest_bytes = struct.pack("<4I", a0, b0, c0, d0)
    digest = digest_bytes.hex()
    if trace:
        return digest, trace_rows
    return digest


def md5_text(text: str) -> str:
    """Convenience wrapper: hash a Unicode string encoded as UTF-8."""
    return str(md5(text.encode("utf-8")))
