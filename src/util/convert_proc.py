'''
Convert from FASTA File
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function

# Application Parameters
DATA_DIR = '../../data/proc/'
ORG_DIR = DATA_DIR + 'data.csv'
FST_DIR = '../../data/fasta/data3_merge.fasta.txt'
OUT_DIR = DATA_DIR + 'data3.csv'

def read_proc(dir, ignore_header=True):
    st = 1 if ignore_header else 0
    data = open(dir, 'r').read().split('\n')[st:-1]
    res = {}
    for i in range(0, len(data), 2):
        id = data[i].split(',')[0]
        res[id] = {}
        res[id]['AMPLabel'] = data[i].split(',')[1]
        res[id]['AMP'] = data[i].split(',')[2]
        res[id]['PepType'] = data[i+1].split(',')[1]
    return res

def read_fasta(data_dir):
    return open(data_dir, 'r').read().split('\n')[:-1]

if __name__ == '__main__':
    # Read Data File
    orig_data = read_proc(ORG_DIR)
    fast_data = read_fasta(FST_DIR)

    # Setup Output CSV File
    out = open(OUT_DIR, 'w')
    out.write('PepID,AMPLabel,AMP,PepType\n')

    # Merge Proc File
    for i in range(0, len(fast_data), 2):
        id = fast_data[i][1:]

        if id not in orig_data:
            seq = fast_data[i+1]
            label = 0
            if id.split('R')[1] == '': type = 'REVERSE'
            elif id.split('R')[1] == '1': type = 'RANDOM1'
            elif id.split('R')[1] == '2': type = 'RANDOM2'
            elif id.split('R')[1] == '3': type = 'RANDOM3'
        else:
            seq = orig_data[id]['AMP']
            label = orig_data[id]['AMPLabel']
            type = orig_data[id]['PepType']

        out.write(','.join([id, str(label), seq, type]) + '\n')

    out.close()
