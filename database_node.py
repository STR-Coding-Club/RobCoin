import sqlite3

con = sqlite3.connect("blockchain.db")

cur = con.cursor()

"""
Block Data
    {
        "height": 6,
        "transactions": [
            {
                "timestamp",
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
    - 
id int, timestamp datetime, sender text, recipient text, amount string 

wallet table  # Time complexity vs space complexity
    -

address text (primary key), verified_balance string, balance string

connections table
    - Prefilled with mandatory "starter" nodes
    - Wallet will have other 
    -  use default boot nodes to connect to the blockchain or choose a custom ip

- problem
    someone might make their own boot node and create a segment blockchain cluster

- solution
    By making the "starter" mandatory peers, users will be forced to connect to our vetted nodes. This way, there will always be some degree of connection between official and potentially stranded nodesdatetime A combination of a date and a time. Attributes: ()

    the mandatory boot node will periodically update based on the nodes connected to it and the nodes in that node's connection table

    once other people start making their own boot nodes then it becomes decentralized (as long as no one owns more than 50% of the hashing power)


ip text, port text
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