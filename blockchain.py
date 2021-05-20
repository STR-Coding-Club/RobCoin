import json
import sys

from time import time

from crypto import hash


class Blockchain(object):
    @property
    def last_block(self) -> dict:
        # Returns the last (header) block in the chain
        return self.chain[-1]

    @property
    def blockchain(self) -> list:
        return self.chain

    def __init__(self, chain_file):
        self.chain = []
        self.pending_transactions = []
        self.current_transactions = []
        self.push_time = 0
        self.mine_time = 0
        # If chain already exists on disk
        if chain_file:
            try:
                with open(chain_file, 'r') as blockchain_file:
                    self.chain = json.loads(blockchain_file.read())
                return None
            except (FileNotFoundError, json.JSONDecodeError):
                print('Error while importing chain_file! Creating temporary test chain', file=sys.stderr)
                """
                Create Testchain with default Genesis Block
                THIS SHOULD NEVER BE CALLED!!
                    - When rolled out, this functions should instead call for a sync with the node to import the live
                        chain
                """

                self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None) -> dict:
        """
        Creates new block to add to the blockchain. Uses previous header to generate new block.
        :param proof: <int> POW value that returns hash < predetermined target hash
        :param previous_hash: <str> hash of current header block
        :return: <dict> new block
        """
        print(self.chain)
        block = {
            'index': len(self.chain) + 1,
            'transactions': self.current_transactions,
            'previous_hash': hash(self.last_block)
        }
        self.current_transactions = []
        # Reset the current list of transactions
        block['proof'] = proof
        self.chain.append(block)
        self.save_blockchain()
        self.push_time = time()
        self.mine_time = time()
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
        self.pending_transactions.append(
            {
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
            })

        return self.last_block['index'] + 1

    def save_blockchain(self, file="blockchain.txt"):
        """
        :param file: saves blockchain to 'blockchain.txt' in case node goes down
        """
        with open('blockchain.txt', 'w', encoding='utf-8') as out:
            json.dump(self.chain, out, ensure_ascii=False, indent=4)  # Padding to make json look pretty

    def ready_to_push(self) -> bool:
        return (time() - self.push_time) >= 10 # seconds

    def ready_to_mine(self) -> bool:
        return (time() - self.mine_time) >= 10

    def push_pending(self) -> list:
        self.current_transactions += self.pending_transactions
        self.pending_transactions = []
        self.push_time = time()
