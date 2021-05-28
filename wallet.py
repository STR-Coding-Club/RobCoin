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

from base64 import b64encode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from random import random

import hashlib
import requests
import sys
NODE = "http://robcoin.strcoding.club:5000"


def generate_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    save_key(private_key)


def read_key():
    # Reads private key from "private_key.pem"
    with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key


def get_public_key(private_key):
    return private_key.public_key()


def save_key(private_key):
    # Takes in private_key param and stores it in "private_key.pem"
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open('private_key.pem', 'wb') as f:
        f.write(pem)


def get_address():
    address = hashlib.sha256(str(get_public_key(read_key()).public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )).encode()).hexdigest()
    return address


def save_address():
    with open("miner_address.txt", 'w') as out:
        out.write(get_address())


def send(receiver, amount, private_key):
    """
    EXAMPLE:

    SENDER:RECEIVER:AMOUNT:NONCE

    Sender
    Receiver
    Amount
    Nonce
    """
    
    can_afford: bool = float(amount) <= float(get_balance()[0])
    if can_afford:
        nonce = random()
        packet = f'{get_address()}:{receiver}:{amount}:{nonce}'

        bytes_package = packet.encode()

        signature = private_key.sign(
            bytes_package,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        response = requests.post(NODE + "/transactions/new",
                                 data={
                                     "transaction": packet,
                                     "signature": b64encode(signature),
                                     "pubkey": get_public_key(private_key).public_bytes(
                                         serialization.Encoding.PEM,
                                         serialization.PublicFormat.SubjectPublicKeyInfo).decode("utf-8")
                                 }
                                 )
    else:
        print(f'Error while sending transaction! - You cannot afford to send {amount} $TR. Try lowering the amount', file=sys.stderr)
        return False
    print(response.status_code)
    return response.status_code  < 400


def get_balance(address=None):
    if not address:
        address = get_address()
    response_chain = requests.get(NODE + "/chain")
    response_pending = requests.post(NODE + "/pendingbalance",
                                 data={
                                     "address": address
                                 })
    chain = response_chain.json()
    pending = response_pending.json()["pending"]
    balance = 0
    exists = pending > 0
    for block in chain['chain']:
        for transaction in block["transactions"]:     
            if transaction["recipient"] == address:
                exists = True
                balance += transaction["amount"]
            elif transaction["sender"] == address:
                exists = True
                balance -= transaction["amount"]
    if exists:
        return [balance, pending]
    else:
        return ["Address Not found",""]
