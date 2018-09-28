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

def read_csv(dir, ignore_header=True):
    st = 1 if ignore_header else 0
    data = open(dir, 'r').read().split('\n')[st:-1]
    raw_data = []
    for d in data:
        r = d.split(',')
        r[1] = int(r[1])
        raw_data.append(r)
    return raw_data

if __name__ == '__main__':
    # Application Parameters
    DATA_DIR = '../../data/proc/'
    INPUT_DIR = DATA_DIR + 'data.csv'
    OUT_DIR = DATA_DIR + 'data2.csv'

    # Read CSV File
    data = read_csv(INPUT_DIR)

    # Process Negative Samples
    neg_pep = []
    for d in data:
        if d[1] == 0:
            # Reversed Sequence
            neg_pep.append([d[0]+'R', 0, reverse_seq(d[2]), 'REVERSE'])

            # Randomized K-Gram Sequence
            for k in range(1, 4):
                neg_pep.append([d[0]+'R'+str(k), 0, shuffle_seq(d[2], k), 'RANDOM'+str(k)])

    data += neg_pep

    print('Generated Fake Data:\t' + str(len(neg_pep)))
    print('Total Sample Size:\t' + str(len(data)))

    # Generate Output File
    out = open(OUT_DIR, 'w')
    out.write('PepID,AMPLabel,AMP,PepType\n')
    for d in data: out.write(','.join([str(i) for i in d])+'\n')
    out.close()
