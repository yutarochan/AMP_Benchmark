'''
Negative Sample Generator
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import math
import random

def kgram(s, k=1):
    kgram = []
    for i in range(0, int(math.ceil(len(s) / k))):
        kgram.append(s[i*k:i*k+k])
    if len(s)%k > 0: kgram.append(s[-(len(s)%k):])
    return kgram

def reverse_seq(s, k=1):
    return ''.join(kgram(s, k)[::-1])

def shuffle_seq(s, k=1):
    seq = kgram(s, k)
    random.shuffle(seq)
    return ''.join(seq)

# if __name__ == '__main__':
