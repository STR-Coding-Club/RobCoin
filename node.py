# import hashlib
# import json
# import sys

# from time import time
from uuid import uuid4

import blockchain
# import cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding #, rsa
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature
from flask import Flask, request, jsonify
from base64 import b64decode

# Instantiate our Node
app = Flask(__name__)

current_chain = blockchain.Blockchain("blockchain.txt")
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')


def verifySignature(signature, packet, pubKeySerialized):
    # TODO storage of addresses and public keys
    # Takes in signature, public key and packet and returns true if it is a valid transaction
    try:
        BytesPackage = packet.encode()
        pubKey = load_pem_public_key(bytes(pubKeySerialized, 'utf-8'))
        pubKey.verify(
            signature,
            BytesPackage,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    except InvalidSignature:
        return False

    return True


def parse_blockchain():
    """
    TODO:
    Parse blockchain and store balance for every address in blockchain as dict
    instead of get_balance() just find balance['get_address()']
    """
    pass
    coin_balances = {}
    for block in blockchain:
        for transaction in block["transactions"]:
            if transaction["recipient"] not in coin_balances:
                coin_balances[transaction["recipient"]] = transaction["amount"]
            else:
                coin_balances[transaction["recipient"]] += transaction["amount"]
                coin_balances[transaction["sender"]] -= transaction[
                    "amount"]  # Will not return negative - checked already


@app.route('/mine', methods=['GET'])
def mine():
    pass
    # After set interval send out block to mine
    # Send collected transactions to miners to mine
    # Clear current transaction list
    # return "Block has been sent to mine!"


@app.route('/submitproof', methods=['POST'])
def submit_proof():
    # Listen for submissions of proofs
    # Check if proof is valid
    #   If valid --> append block to blockchain, add miner reward to current transactions
    pass


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    # print(request.form)
    required = ['transaction', 'signature', 'pubkey']
    if not all(p in request.form for p in required):
        return 'Missing required transaction data', 400  # Bad request

    # Create transaction on the chain \\ sender:recipient:amount
    sender = request.form['transaction'].split(':')[0]
    recipient = request.form['transaction'].split(':')[1]
    amount = float(request.form['transaction'].split(':')[2])
    valid = verifySignature(b64decode(request.form['signature']), request.form['transaction'], request.form['pubkey'])
    if not valid:
        return "Invalid signature", 401  # Unauthorized
    index = current_chain.new_transaction(sender, recipient, amount)
    return "Success", 201  # Created


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': current_chain.blockchain,
        'length': len(current_chain.blockchain),
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
