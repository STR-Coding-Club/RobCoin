import wallet
from os import path

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

print('Looking for Private Key...')
print()
if path.exists("private_key.pem"):
    print("Private key detected!")
    print(f'Your Receiving Address: {wallet.get_address()}')

# If private key is not detected
else:
    print("No private key detected, creating private key now...")
    wallet.generate_key()
    print("Private key has been saved as \' private_key.pem \' DO NOT share this key with anyone")

if path.exists("miner_address.txt"):
    print("Miner address detected!")
else:
    print("No Miner address detected, generating one now...")
    wallet.save_address()


def command_error():
    print("Command error, listing available commands")
    print()
    print('\t> send <receiver>, <amount>')
    print()
    print('\t> balance [optional: address]')
    print()
    print('\t> address')
    print()
    
print()
print('Wallet initialized!')
print()
while True:
    try:
        command = input('> ').split()
    except IndexError:
        command_error()
    try:
        if command[0].lower() == 'send':
            if len(command) == 3:
                receiver = command[1]
                amount = command[2]
                sent = wallet.send(receiver, amount, wallet.read_key()) 
                if sent:
                    print(f"Sent {amount} to {receiver}")
                    print(f"Your current balance is: {wallet.get_balance()[0]} (Pending: {wallet.get_balance()[1]})")
                else:
                    print("Command error, check if you have enough balance. Please refer to the documentation.")
                    print("Link to docs")
            else:
                print("Command Error:")
                print("\tUsage: `send <receiver> <amount>`")
        elif command[0].lower() == 'balance':
            if len(command) == 1:
                print(f"Your current balance is: {wallet.get_balance()[0]} (Pending: {wallet.get_balance()[1]})")
            elif len(command) == 2:
                balance = wallet.get_balance(command[1])[0]
                if balance:
                    print(f'Balance for input address: {balance}')
                else:
                    print(f'Error: Invalid Address (Does not exist on blockchain)')
        elif command[0].lower() == 'address':
            print(f'Your Receiving Address is: {wallet.get_address()}')
        else:
            command_error()
    except IndexError:
        command_error()
    except Exception:
        print('Networking Error - Make sure you are connected to the internet/check your DNS')

