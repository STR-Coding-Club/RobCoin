import miner

print("***********************************************")
print("""  _____       _      _____      _       
 |  __ \     | |    / ____|    (_)      
 | |__) |___ | |__ | |     ___  _ _ __  
 |  _  // _ \| '_ \| |    / _ \| | '_ \ 
 | | \ \ (_) | |_) | |___| (_) | | | | |
 |_|  \_\___/|_.__/ \_____\___/|_|_| |_|""")

print()
print("***********************************************")

print("Copyright (c) 2021 STR-Coding-Club")
print('View the docs: https://github.com/STR-Coding-Club/RobCoin')
print()

miner = miner.Miner()
print()
try:
    miner.mine()
except Exception as error:
    print(f'Connection error - {error}')
    print()
    print('Please check your internet connection. Is the node online?')
