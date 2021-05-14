block1 = {  # type = Dict
    'index': 1,
    'timestamp': 1506057125.900785,
    'transactions': [
        {
            'sender': "miner",
            'recipient': "2f4c0b13ad5b8a3dfc29ffbad1954f0cf098cc9ce769cfb8c7dc94dd474d1eb5",
            # IMPORTANT! REPLACE HASH WITH HASH PRINTED IN CONSOLE BEFORE DOING THING
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
            'sender': "2f4c0b13ad5b8a3dfc29ffbad1954f0cf098cc9ce769cfb8c7dc94dd474d1eb5",
            'recipient': "7020f19f81a86ba882f3eb587a1608e6a9ddfd8c2a53037ec83db4d56bc83d8a",
            'amount': 5,
        },
        {
            'sender': "2f4c0b13ad5b8a3dfc29ffbad1954f0cf098cc9ce769cfb8c7dc94dd474d1eb5",
            'recipient': "5ac42b0b4704565d9b87651345eed5b04011915d135645ea4f856cd6f01808f9",
            'amount': 5,
        },
        {
            'sender': "2f4c0b13ad5b8a3dfc29ffbad1954f0cf098cc9ce769cfb8c7dc94dd474d1eb5",
            'recipient': "e78bf12431c2cda9c7de4c4a608204193a25b99ce947f1f2be87e1118cee5e41",
            'amount': 5,
        },
        {
            'sender': "2f4c0b13ad5b8a3dfc29ffbad1954f0cf098cc9ce769cfb8c7dc94dd474d1eb5",
            'recipient': "34b72cce39da8440933a1e215d8b2bc2e0faa737c45dddba6076ccf59b8f9ab6",
            'amount': 5,
        },
        {
            'sender': "2f4c0b13ad5b8a3dfc29ffbad1954f0cf098cc9ce769cfb8c7dc94dd474d1eb5",
            'recipient': "625e853783a41401de7df94f3c911b6ee3b2e19c27018f40d8cc9a7a43891e19",
            'amount': 5,
        }
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


def blockchain():
    return block_list

