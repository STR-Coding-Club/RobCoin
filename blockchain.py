import hashlib
import json
import sys

from time import time
from uuid import uuid4
from binascii import hexlify, unhexlify


class Blockchain(object):
    @property
    def last_block(self):
        # Returns the last (header) block in the chain
        return self.chain[-1]

    @property
    def blockchain(self):
        return self.chain

    def __init__(self, chain_file=''):
        self.chain = []
        self.current_transactions = []

        # If chain already exists on disk
        if chain_file:
            try:
                with open(chain_file, 'r') as blockchain_file:
                    self.chain = json.loads(blockchain_file.read())
                return
            except (FileNotFoundError, json.JSONDecodeError):
                print('Error while importing chain_file! Continuing anyways with an empty chain...', file=sys.stderr)

        # Genesis Block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Creates new block to add to the blockchain. Uses previous header to generate new block.
        :param proof: <int> POW value that returns hash < predetermined target hash
        :param previous_hash: <str> hash of current header block
        :return: <dict> new block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'previous_hash': previous_hash or hexlify(self.hash(self.last_block)),
        }
        self.current_transactions = []
        # Reset the current list of transactions
        self.current_transactions = []
        block['proof'] = proof
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Compiles and appends new incoming transactions to add to the block.
        Once mined, transactions will "go through" and are added to the blockchain.
        Incoming transactions, therefore, are not transacted until the block is mined.
        :param sender: <str> Wallet address of the Sender
        :param recipient: <str> Wallet address of the Recipient
        :param amount: <float> Amount of $TR (Robcoin) to be transacted
        :return: <int> Index of transaction to add to the new block. (see example-block.py)
        """
        self.current_transactions.append(
            {
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
            })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Hashes a block
        :param block: <dict> block (see example-block.py)
        :return: <bytes> hash of block
            - Returns block hash as bytes
        """
        block_encoded = bytes(json.dumps(block, sort_keys=True).encode())  # Sorted to ensure consistent hashes
        return hashlib.sha256(block_encoded).digest()

    @staticmethod
    def valid_proof(last_hash, proof):
        """
        Validates the Proof.
        :param last_hash: <bytes> Previous hash
        :param proof: <int> current proof
        :return: <bool> true the guessed POW meets the POW criteria (Guessed hash < POW requirement), false if not
                Guess hash is represented as a binary string.
                When inverted, the binary hash must have N leading 0s
                https://en.bitcoin.it/wiki/Block_hashing_algorithm
        """

        """Difficulty N increases mining difficulty exponentially (2**N)"""
        N = 5  # Difficulty (N >= 1)
        guess = f'{last_hash.hex()}{proof}'  # Append proof to end of block hash
        guess_hash = hashlib.sha256(guess.encode()).hexdigest()
        bin_guess_hash = f"{bin(int.from_bytes(unhexlify(guess_hash), byteorder='big'))}"[::-1]  # Reverse binary string
        if proof < 5:
            print(f'proof={proof}: {bin_guess_hash}')
            print(f'{last_hash.hex()}{proof}')
        if bin_guess_hash[:N] == "0" * N:
            print(f'proof={proof}: {bin_guess_hash}')
        return bin_guess_hash[:N] == "0" * N

    def save_blockchain(self, file="blockchain.txt"):
        with open('blockchain.txt', 'w') as out:
            json.dump(self.chain, out)
