#!/usr/bin/python
from sys import argv

SUB = [0, 1, 1, 0, 1, 0, 1, 0]
N_B = 32
N = 8 * N_B

def get_contents(f_name):
    return


def main():
    plain = open('bis.txt', 'rb').read()
    secret = open('bis.txt.enc', 'rb').read()
    super_cipher = open('super_cipher.py.enc', 'rb').read()

    length = len(plain) if len(plain) < len(secret) else len(secret)
    keystream = []
    for i in range(length):
            keystream.append(plain[i] ^ secret[i] ^ super_cipher[i])

    print(bytes(keystream))
    print (len(msg))

if __name__ == '__main__':
    main()
