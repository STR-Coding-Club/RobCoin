import blockchain
import miner

current_chain = blockchain.Blockchain()


print(current_chain.chain)
current_chain.new_transaction('Ernest', 'Dhyey', 100)
print(current_chain.current_transactions)
current_chain.new_transaction('Bank', 'Government', 200)
print(current_chain.current_transactions)

current_miner = miner.Miner(current_chain.hash(current_chain.last_block))
# Literally mining
current_chain.new_block(current_miner.proof_of_work())

print(current_chain.chain)
