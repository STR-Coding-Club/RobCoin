import blockchain
import crypto
import random
import requests
from time import sleep, time
from numpy import average
import sys

NODE = "http://robcoin.strcoding.club:5000"

try:
    with open("miner_address.txt", "r") as address:
        mining_address = address.read()
except FileNotFoundError:
    print("'miner_address.txt' not detected! Run 'run_wallet.py' first!", file=sys.stderr)
    sys.exit(0)

hash_per_second = []


class Miner(object):
    @property
    def current_chain(self):
        response = requests.get(NODE + "/chain")
        chain = blockchain.Blockchain()
        chain.chain = response["chain"]
        return chain

    def __init__(self):
        print('Miner initialized!')

    def proof_of_work(self, block) -> int:
        """
        Proof of Work (POW algorithm)
            - Find <int> p' such that p' combined by p < POW target, where p is the previous hash
            - for hash(pp') to be smaller than the POW target, the hash must have N number of leading zeros
            - leading zeros N can be increased to increase mining difficulty
        :param block: <dict>
        :return: <int> p'
        """

        guesses = 0
        proof = 0
        start = time()
        while not crypto.valid_proof(block, proof):
            proof = random.getrandbits(256)
            guesses += 1
        end = time()
        hash_per_second.append(guesses / (end - start))
        print(f'Hashrate: {average(hash_per_second) / 1000:.2f} KH/s')
        return proof

    def mine(self):
        while True:
            while requests.get(NODE + "/work").status_code == 204:  # Empty
                sleep(2)
            response = requests.get(NODE + "/work")
            proof = self.proof_of_work(response.json())
            print(f'Proof found: {proof}')
            print('Sending now to node...')
            if requests.get(NODE + "/work").status_code == 200:  # worked
                print('Success! You have been rewarded with 1 $TR (to be added in next block)')
                print()
            else:
                print('Error! Did not send block in on-time!')
                print()
            headers = {'User-Agent': 'Mozilla/5.0'}
            requests.post(NODE + "/submitproof", headers=headers, data={
                "proof": proof,
                "miner": mining_address
            })
