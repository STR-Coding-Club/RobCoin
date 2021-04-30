block = {  # type = Dict
    'index': 1,
    'timestamp': 1506057125.900785,
    'transactions': [
        {
            'sender': "8527147fe1f5426f9dd545de4b27ee00",
            'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
            'amount': 5,
        },
        {
            'sender': "8527147fe1f5426f9dd545de4b27ee00",
            'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
            'amount': 5,
        }
    ],

    'proof': 324984774000,  # Proof is some int that 'solves' the block - Proof of Work (POW)
                            # hash(proof, block) will return value < POW requirement
    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}

"""
    'transactions' stores new transactions to the blockchain. 
    ---
    block['transactions'] 
        #  returns a list of transactions from the block. 
        #  specific transactions from a block are retrieved using their index in the list.
            #  eg. block['transactions'][0] returns info from the first transaction as dict.
"""

print(block['proof'])
print(block['transactions'][0]['sender'])