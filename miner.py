import blockchain
import crypto
import random
import requests
from time import sleep

NODE = "http://localhost:5000"

with open("miner_address.txt", "r") as address:
    mining_address = address.read()


class Miner(object):
    @property
    def current_chain(self):
        response = requests.get(NODE + "/chain")
        chain = blockchain.Blockchain()
        chain.chain = response["chain"]
        return chain

    def __init__(self):
        pass

    def proof_of_work(self, block) -> int:
        """
        Proof of Work (POW algorithm)
            - Find <int> p' such that p' combined by p < POW target, where p is the previous hash
            - for hash(pp') to be smaller than the POW target, the hash must have N number of leading zeros
            - leading zeros N can be increased to increase mining difficulty
        :param block: <dict>
        :return: <int> p'
        """

        proof = 0
        while not crypto.valid_proof(block, proof):
            proof = random.getrandbits(256)
        return proof

    def mine(self):
        while True:
            while requests.get(NODE + "/work").status_code == 204:  # Empty
                sleep(2)
            response = requests.get(NODE + "/work")
            proof = self.proof_of_work(response.json())
            headers = {'User-Agent': 'Mozilla/5.0'}
            print(type(proof))
            requests.post(NODE + "/submitproof", headers=headers, data={
                "proof": proof,
                "miner": mining_address
            })