import sqlite3

con = sqlite3.connect("blockchain.db")

cur = con.cursor()

"""
Block Data
    {
        "height": 6,
        "transactions": [
            {
                "timestamp": ,
                "sender": "0",
                "recipient": "122c55d8231889c4babfcf523adb0bec0729a7045517fb20aa33b2e3ee3053dc",
                "amount": 1
            }
        ],
        "previous_hash": "9c911890d00da5e9e291bea2cbb0ea94ef82fda00bc6b685a9eee56281bc3394",
        "proof": "44134922049878989083772700660191407967931859896339461090370777570167769441250"
    },

block table
    - Stores all blocks
    - Transactions are stored as <>
id int, firsttransaction int, lasttransaction int, transactions text, previoushash text, proof int

#all blockchains are a scam

transactions table # Once node is fully synced, broadcast all pending transactions
    - Store Pending as Bool
    - Store #of confirmations (blocks since transaction)
    - If transaction doesn't work, retry
id int, timestamp datetime, sender text, recipient text, amount string 

wallet table  # Time complexity vs space complexity
    -

address text (primary key), verified_balance string, balance string

connections table
    - Prefilled with mandatory "starter" nodes
    - Wallet will have other 
    -  use default boot nodes to connect to the blockchain or choose a custom ip
    - Cap the # of connections
    - Kick out idle/non-responsive nodes

Consensus problem
    - If a block "n" gets mined at the same time, but with different transactions, your blockchain will branch
        - If you're a node/miner, store the FIRST block (n) you recieve, but store the other copy (n')
            - Keep the longer branch after N blocks
        

- problem
    someone might make their own boot node and create a segment blockchain cluster

- solution
    By making the "starter" mandatory peers, users will be forced to connect to our vetted nodes. This way, there will always be some degree of connection between official and potentially stranded nodesdatetime A combination of a date and a time. Attributes: ()

    the mandatory boot node will periodically update based on the nodes connected to it and the nodes in that node's connection table

    once other people start making their own boot nodes then it becomes decentralized (as long as no one owns more than 50% of the hashing power)


ip text, port text

# Node Syncing
    - Nodes will Sync every n/2 seconds where n = block time
    - Sync Time is local based on own clock
        - Every 5 seconds after boot up, send GET request


PROBLEMS
    1. Blockchain Branching
        - When you are mining, you are not sure of when to stop mining. We must define some point where you stop mining & start resyncing
        - Once 50% of the miners on the blockchain have finished mining block n, all miners will sync and move on to the next block
        - If when syncing the miner realizes their hash is wrong, then the code will automatically backtrack them to the correct blockchain
        - The first miner who got the hash correct gets a reward
            - The first miner appends their block reward to the block they mine
        - When a node syncs a block, clear all pending transactions that have already been added to the blockchain
        
    2. Transaction Verification
        - What currently happens when a malicious party decides to alter a transaction
            - Increase sending amount, adjust 
        - Right now, signature is only checked by node
        - Potential fix: Store transaction signature in Blockchain
            - Also add transaction hash with the transaction (ensures immutibility)
    3. Syncing
        - Block syncing process
            i. First, ask all nodes for hash of block n
            ii. Next, prune all nodes that do not agree
            iii. Ask for random node for block data
            iv. Verify all aspects of block (transaction, proof of work)
    4. Transaction Broadcasting / Wallet
        - Wallets broadcast their transactions to everyone they know
        
        
        - Wallets must connect to all "starter" nodes, and then proliferate 
            - Wallets are not necessarily nodes, but they do connect to other nodes like a node
            
            - FIX:
                - All wallets are nodes, but not necessarily miners
                - They still perform all of the functions of a node

        - Wallets will broadcast transactions to all nodes, and all nodes hearing the transaction will broadcast transaction to other nodes
        - If a transaction is lost (not added within 5 blocks), resend transaction [automatically/manually?] (seanFix)

"""

# name, datatype
cur.execute('''CREATE TABLE transactions (id int, data text)''')

cur.execute("INSERT INTO transactions VALUES (1, 'Dhyey sends Ernest 2.0 RobCoin2')")

cur.execute("INSERT INTO transactions VALUES (2, 'Dhyey sends Ernest 2.0 RobCoin21')")

cur.execute("INSERT INTO transactions VALUES (3, 'Dhyey sends Ernest 2.0 RobCoin22')")

cur.execute("INSERT INTO transactions VALUES (4, 'Dhyey sends Ernest 2.0 RobCoin23')")

con.commit()

for row in cur.execute('SELECT * FROM transactions ORDER BY id'):
    print(row)

con.close()
