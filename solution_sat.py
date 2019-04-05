#!/usr/bin/python3
from sys import argv
from satispy import Variable
from satispy.solver import Minisat
import string

N_B = 32
N = 8 * N_B


# xor two byte arrays
def xor(ar1, ar2):
    length = len(ar1) if len(ar1) < len(ar2) else len(ar2)
    res = []
    for i in range(length):
        res.append(ar1[i] ^ ar2[i])
    return res

# getting a value from a bit on nth position
def get_bit(value, n):
    return (value >> n) & 1


def get_eq(bit, c, b, a):
    a, b, c = Variable(str(a)), Variable(str(b)), Variable(str(c))
    if bit:
        return (-a & -b & c) | (b & -c) | (a & -c)
    else:
        return (-a & -b & -c) | (b & c) | (a & c)


def solve(eq):
    solution = Minisat().solve(eq)
    assert solution.success, 'ERR: Failed to solve'

    result = 1 << N-1 if solution[Variable('0')] else 0
    for i in range(1, N):
        result |= 1 << i-1 if (solution[Variable(str(i))]) else 0

    return result


def r_sat_step(x):
    eq = Variable('eq')
    for i in range(0, N):
        eq = eq & get_eq(get_bit(x, i), i % N, (i + 1) % N, (i +2) % N)
    return solve(eq)



if __name__ == '__main__':
    plain = open('bis.txt', 'rb').read(N_B)
    secret = open('bis.txt.enc', 'rb').read(N_B)

    # use known plaintext attack to get first 32B of keystream
    k = xor(plain, secret)
    kstrm = int.from_bytes(k, 'little')

    for i in range(N // 2):
        kstrm = r_sat_step(kstrm)

    print(kstrm.to_bytes(N_B, 'little').decode())
