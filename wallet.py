from base64 import b64encode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import hashlib
from os import path
from random import random
import requests
import sys
NODE = "http://localhost:5000"


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
    can_afford: bool = float(amount) <= float(update_balance())
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


def update_balance():
    response = requests.get(NODE + "/chain")
    chain = response.json()
    balance = 0
    for block in chain['chain']:
        for transaction in block["transactions"]:
            if transaction["recipient"] == get_address():
                balance += transaction["amount"]
            elif transaction["sender"] == get_address():
                balance -= transaction["amount"]
    return balance


if __name__ == "__main__":
    # If private key is detected
    if path.exists("private_key.pem"):
        print("Private key detected!")
        print(get_address())

    # If private key is not detected
    else:
        print("No private key detected, creating private key now...")
        generate_key()
        print("Private key has been saved as \' private_key.pem \' DO NOT share this key with anyone")

    if path.exists("miner_address.txt"):
        print("Miner address detected!")
    else:
        print("No Miner address detected, generating one now...")
        save_address()

    # Send packets here // TODO: Add async support


    while True:
        print(f"Your current balance is: {update_balance()}")
