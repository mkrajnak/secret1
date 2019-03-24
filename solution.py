#!/usr/bin/python
from sys import argv

SUB = [0, 1, 1, 0, 1, 0, 1, 0]
N_B = 32
N = 8 * N_B


# Next keystream, taken from decrypted file
def step(x):
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
        key = step(int.from_bytes(bytes(key), 'little')).to_bytes(N_B, 'little')
    return decrypted

# initial decryption of files from extracted keystream aka attack
def decrypt_from_keystream():
    plain = open('bis.txt', 'rb').read(N_B)
    secret = open('bis.txt.enc', 'rb').read(N_B)

    # use known plaintext attack to get first 32B of keystream
    kstrm = xor(plain,secret)

    # use obtained keystream and step to decrypt the rest of the algorithm
    super_cipher = open('super_cipher.py.enc', 'rb').read()
    print(''.join([bytes(x).decode() for x in decrypt(super_cipher, kstrm)]))

    # same fo the hint.gif
    hint = open('hint.gif.enc', 'rb').read()
    with open('hint.gif', 'wb') as f:
        for x in decrypt(hint, kstrm):
            f.write(bytes(x))


if __name__ == '__main__':
    decrypt_from_keystream()
