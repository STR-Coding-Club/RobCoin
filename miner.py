import blockchain
import random


class Miner(object):
    def __init__(self, last_hash):
        self.last_hash = last_hash

    def proof_of_work(self):
        """
        Proof of Work (POW algorithm)
            - Find <int> p' such that p' combined by p < POW target, where p is the previous hash
            - for hash(pp') to be smaller than the POW target, the hash must have N number of leading zeros
            - leading zeros N can be increased to increase mining difficulty
        :param last_hash: <bytes> p where p is the last block's hash
        :return: <int> p'
        """
        proof = 0
        while not blockchain.Blockchain.valid_proof(self.last_hash, proof):
            proof = random.getrandbits(256)
        return proof
