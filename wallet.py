from exampleBlockchain import get_blockchain
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import hashlib
import os
from random import random


blockchain = get_blockchain()


def generate_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    save_key(private_key)


def save_key(private_key):
    # Takes in private_key and stores it on disk
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open("private_key.pem", "wb") as f:
        f.write(pem)


def read_key():
    with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend(),
        )
    return private_key


def get_public_key(private_key):
    return private_key.public_key()


def get_address():
    address = hashlib.sha256(str(get_public_key(read_key()).public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
        )).encode()).hexdigest()
    return address


def send(receiver, amount, private_key):
    """

    RECEIVER:AMOUNT:NONCE
    :param receiver: <str> SHA-256 hash of someone else's public key
    :param amount: <int> # robcoin
    :param private_key: <bytes>

    """
    nonce = random()
    packet = f'{receiver}:{amount}:{nonce}'
    bytes_package = packet.encode()

    signature = private_key.sign(
        bytes_package,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print(packet)


if __name__ == "__main__":
    # If private key is detected
    if os.path.exists("private_key.pem"):
        print("Private key is detected!")
        print(get_address())

        # Get balance of address
        balance = 0

        for block in blockchain:
            for transaction in block['transactions']:
                if transaction['recipient'] == get_address():
                    balance += transaction['amount']
                elif transaction['sender'] == get_address():
                    balance -= transaction["amount"]

        print(f'Your current balance is: {balance}')
    else:
        print("No private key detected, creating private key now...")
        generate_key()
        print('Private key has been saved as "private_key.pem". DO NOT share this key with ANYONE!')

    send("Dhyey", 10, read_key())
