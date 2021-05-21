import wallet
from os import path

if path.exists("private_key.pem"):
    print("Private key detected!")
    print(wallet.get_address())

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

while True:
    command = input().split() # Write Docs for this lmao  
    if command[0].lower() == '$trsend':
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
            print("Command error, please refer to the documentation.")
            print("Link to docs")
    elif command[0].lower() == '$trbalance':
        if len(command) == 1:
            print(f"Your current balance is: {wallet.get_balance()[0]} (Pending: {wallet.get_balance()[1]})")
        elif len(command) == 2:
            balance = wallet.get_balance(command[1])[0]
            if balance:
                print(f'Balance for input address: {balance}')
            else:
                print(f'Error: Invalid Address (Does not exist on blockchain)')
    elif command[0].lower() == '$traddress':
        print(f'Your Receiving Address is: {wallet.get_address()}')
    else:
        print("Command error, Please refer to the documentation.")
        print("Link to docs")
