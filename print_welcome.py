def print_welcome():
    with open("welcome.txt", "r") as f:
        for line in f.readlines():
            print(line[:-1])
    print()