'''
AMP FAST Formater
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function

# Application Parameters
DATA_DIR = '../../data/proc/'
INPUT_DIR = DATA_DIR + 'data3.csv'
OUTPUT_DIR = '../../data/fasta/data3.fasta.txt'

def read_csv(dir, ignore_header=True):
    st = 1 if ignore_header else 0
    data = open(dir, 'r').read().split('\n')[st:-1]
    return [[d.split(',')[0], d.split(',')[2]] for d in data]

if __name__ == '__main__':
    # Read CSV File
    data = read_csv(INPUT_DIR)

    for d in data:
        if '\n' in d[1]:
            print(d)

    '''
    # FASTA File Generate Output
    out = open(OUTPUT_DIR, 'w')
    for d in data:
        out.write('>' + d[0] + '\n')
        out.write(d[1] + '\n')
    out.close()

    print('Output File: ' + OUTPUT_DIR)
    '''
