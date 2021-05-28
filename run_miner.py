"""
MIT License

Copyright (c) 2021 STR-Coding-Club

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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
