from uuid import uuid4

import blockchain

# import cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding  # rsa
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature
from flask import Flask, request
from base64 import b64decode
import crypto
import wallet

# Instantiate our Node
app = Flask(__name__)

current_chain = blockchain.Blockchain("blockchain.txt")
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')


def verifySignature(signature, packet, pubKeySerialized) -> bool:
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


@app.route('/submitproof', methods=['POST'])
def submit_proof():
    # Listen for submissions of proofs
    # Check if proof is valid
    # If valid --> append block to blockchain, add miner reward to current transactions
    required = ['miner', 'proof']
    if not all(p in request.form for p in required):
        return 'Missing required transaction data', 400  # Bad request
    if not current_chain.ready_to_mine():
        return 'No block ready to mine!', 425    
    block = {
        'index': len(current_chain.chain) + 1,
        'transactions': current_chain.current_transactions,
        'previous_hash': crypto.hash(current_chain.last_block)
    }

    valid = crypto.valid_proof(block, int(request.form['proof']), True)
    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    # Miner reward
    REWARD: int = 1
    if valid:

        # Add mined block to chain
        block = current_chain.new_block(request.form['proof'])
        response = {
            'message': f"New Block Mined, {REWARD} $TR has been added to your account",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        current_chain.new_transaction(
            sender="0",
            recipient=request.form['miner'],  # Send to miner who submitted proof
            amount=REWARD,
        )
        print(response)
        return response, 200
    else:
        return "Invalid proof", 406


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
    current_balance = float(current_chain.current_balances[sender]) if sender in current_chain.current_balances.keys() else 0 
    pending_balance = float(current_chain.pending_balances[sender]) if sender in current_chain.pending_balances.keys() else 0 
    
    validSignature: bool = verifySignature(b64decode(request.form['signature']), request.form['transaction'], request.form['pubkey']) 
    validBalance: bool = wallet.get_balance(wallet.get_address())[0] >= (amount + pending_balance + current_balance)  
    if not validSignature:
        return "Invalid signature", 401  # Unauthorized
    if not validBalance: 
        return "Insufficient funds", 401 # Unauthorized
    index = current_chain.new_transaction(sender, recipient, amount)
    return "Success", 201  # Created


@app.route('/chain', methods=['GET'])
def full_chain():
    """
    :return: Returns entire blockchain in memory (current_chain.blockchain)
    """
    response = {
        'chain': current_chain.blockchain,
        'length': len(current_chain.blockchain),
    }
    return response, 200


@app.route('/work', methods=['GET'])
def broadcast_work():
    """
    sends block to be mined
        incoming transactions coming after block to be mined still is being mined will be added to pending_transactions
        After set time interval, if no block has been mined (blockchain size has not increased), pending_transactions is
            appended to next block to be broadcasted
    """
    if current_chain.ready_to_push:
        current_chain.push_pending()
    if not current_chain.ready_to_mine():
        return "", 204
    response = {
        'index': len(current_chain.chain) + 1,
        'transactions': current_chain.current_transactions,
        'previous_hash': crypto.hash(current_chain.last_block)
    }
    return response, 200


@app.route('/pendingbalance', methods=['POST'])
def get_pending_balance(): 
    required = ['address']
    balance = 0
    if not all(p in request.form for p in required):
        return 'Missing address for request', 400  # Bad request
    if request.form['address'] in current_chain.pending_balances:
        balance = current_chain.pending_balances[request.form['address']]
    if request.form['address'] in current_chain.current_balances:
        balance += current_chain.current_balances[request.form['address']]
    response = {
        'pending': balance
    }
    return response, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)