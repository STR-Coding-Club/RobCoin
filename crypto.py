"""
MIT License

Copyright (c) 2021 STR-Coding-Club

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import hashlib
import json
from binascii import unhexlify


def hash(block) -> str:
    """
    Hashes a block
    :param block: <dict> block (see example-block.py)
    :return: <bytes> hash of block
        - Returns block hash as bytes
    """
    block_encoded = bytes(json.dumps(block, sort_keys=True).encode())  # Sorted to ensure consistent hashes
    return hashlib.sha256(block_encoded).hexdigest()


def valid_proof(block, proof, node=False) -> bool:
    """
    Validates the Proof.
    :param current_hash: <bytes> Previous hash
    :param proof: <int> current proof
    :return: <bool> true the guessed POW meets the POW criteria (Guessed hash < POW requirement), false if not
            Guess hash is represented as a binary string.
            When inverted, the binary hash must have N leading 0s
            https://en.bitcoin.it/wiki/Block_hashing_algorithm
    """

    """Difficulty N increases mining difficulty exponentially (2**N)"""
    N: int = 20  # Difficulty (N >= 1)

    block['proof'] = proof
    guess = block
    # Append proof to end of block hash
    guess_hash = hash(guess)
    bin_guess_hash = f"{bin(int.from_bytes(unhexlify(guess_hash), byteorder='big'))}"[::-1]  # Reverse binary string
    return bin_guess_hash[:N] == "0" * N
