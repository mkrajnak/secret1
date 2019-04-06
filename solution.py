#!/usr/bin/env python3
from os import path
from sys import argv, exit

SUB = [0, 1, 1, 0, 1, 0, 1, 0]
N_B = 32
N = 8 * N_B
ZEROS = [x for x in range(len(SUB)) if SUB[x] == 0]
ONES = [x for x in range(len(SUB)) if SUB[x] == 1]


# Next keystream, taken from decrypted file
def s_step(x):
    x = (x & 1) << N+1 | x << 1 | x >> N-1
    y = 0
    for i in range(N):
        y |= SUB[(x >> i) & 7] << i
    return y


# xor or two byte arrays
def xor(ar1, ar2):
    length = len(ar1) if len(ar1) < len(ar2) else len(ar2)
    res = []
    for i in range(length):
        res.append(ar1[i] ^ ar2[i])
    return res


# generator yielding next 32 Bytes of array
def get_part(arr):
    for i in range(0, len(arr), N_B):
        yield arr[i:i + N_B]


# applying xor step by step with a fresh keystream
def decrypt(secret, key):
    decrypted = []
    for x in get_part(secret):
        decrypted.append(xor(x, key))
        key = s_step(int.from_bytes(bytes(key), 'little')).to_bytes(N_B, 'little')
    return decrypted


# getting a value from a bit on nth position
def get_bit(value, n):
    return (value >> n) & 1


def next_bit(g, bit):
    one = 0 if g & 0b011 else 1
    zero = 1 if g & 0b011 else 0
    return one if bit else zero


def r_step(x):
    # possibilities for the first bit
    guess = ONES if get_bit(x, 255) else ZEROS
    # find all 4 possibilitis
    for j in range(2, N+1):
        bit = get_bit(x, N - j)
        guess = [(g << 1) + next_bit(g, bit) for g in guess]
    # one possibily has to match original step
    for g in guess:
        tmp = g >> 1 & ~(1 << N)
        if x == s_step(tmp):
            return tmp  # match

# Function used for decription of encrypted files
# def decrypt_from_keystream():
    # # use obtained keystream and step to decrypt the rest of the algorithm
    # super_cipher = open('super_cipher.py.enc', 'rb').read()
    # # print(''.join([bytes(x).decode() for x in decrypt(super_cipher, k)]))
    #
    # # same fo the hint.gif
    # hint = open('hint.gif.enc', 'rb').read()
    # with open('hint.gif', 'wb') as f:
    #     for x in decrypt(hint, k):
    #         f.write(bytes(x))


if __name__ == '__main__':
    PATH = path.abspath(argv[1])
    plain = open(PATH + '/bis.txt', 'rb').read(N_B)
    secret = open(PATH + '/bis.txt.enc', 'rb').read(N_B)

    # use known plaintext attack to get first 32B of keystream
    k = xor(plain, secret)
    kstrm = int.from_bytes(k, 'little')

    for i in range(N//2):
        kstrm = r_step(kstrm)

    print(kstrm.to_bytes(N_B, 'little').decode())
