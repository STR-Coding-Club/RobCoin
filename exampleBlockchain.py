block1 = {  # type = Dict
    'index': 1,
    'timestamp': 1506057125.900785,
    'transactions': [
        {
            'sender': "miner",
            'recipient': "9f6cbc12b89b0eac7670acc753983f688067060e4d2f2dd218079973d39666e0",
            'amount': 100,
        },
    ],

    'proof': 324984774000,  # Proof is some int that 'solves' the block - Proof of Work (POW)
    # hash(proof, block) will return value < POW requirement
    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}

block2 = {
    'index': 2,
    'timestamp': 1504356437.53456,
    'transactions': [
        {
            'sender': "9f6cbc12b89b0eac7670acc753983f688067060e4d2f2dd218079973d39666e0",
            'recipient': "5ac42b0b4704565d9b87651345eed5b04011915d135645ea4f856cd6f01808f9",
            'amount': 5,
        },
        {
            'sender': "9f6cbc12b89b0eac7670acc753983f688067060e4d2f2dd218079973d39666e0",
            'recipient': "e78bf12431c2cda9c7de4c4a608204193a25b99ce947f1f2be87e1118cee5e41",
            'amount': 5,
        },
        {
            'sender': "9f6cbc12b89b0eac7670acc753983f688067060e4d2f2dd218079973d39666e0",
            'recipient': "2cf24dba5fb0a30e26edfg3456tdfg343efsdf37425e73043362938b9824",
            'amount': 5,
        },
    ],

    'proof': 345345435345345,  # Proof is some int that 'solves' the block - Proof of Work (POW)
    # hash(proof, block) will return value < POW requirement
    'previous_hash': "2cf24dba5fb0a30e26edfg3456tdfg343efsdf37425e73043362938b9824"
}
"""
    'transactions' stores new transactions to the blockchain. 
    ---
    block['transactions'] 
        #  returns a list of transactions from the block. 
        #  specific transactions from a block are retrieved using their index in the list.
            #  eg. block['transactions'][0] returns info from the first transaction as dict.
"""

block_list = [block1, block2]


def get_blockchain():
    return block_list
