'''
Data Preprocessing Routine
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function

def read_csv(dir, id, ignore_header=True):
    st = 1 if ignore_header else 0
    data = open(dir, 'r').read().split('\n')[st:-1]
    return [['{}{:05d}'.format(id, i+1), int(d.split(',')[0]), d.split(',')[1]] for i, d in enumerate(data)]

def merge(d1, d2):
    return d1 + d2

def duplicates(d1, d2):
    return list(set([d[2] for d in d1]).intersection(set([d[2] for d in d2])))

def replace_label(data):
    for i in range(len(data)):
        if data[i][1] == -1: data[i][1] = 0
    return data

if __name__ == '__main__':
    # Application Parameters
    RAW_DIR = '../../data/raw/'
    AMP_DIR = RAW_DIR + 'ADP3.csv'
    DAMPD_DIR = RAW_DIR + 'DAMPD.csv'
    OUT_DIR = '../../data/merge/data.csv'

    # Read CSV Data
    amp_raw = read_csv(AMP_DIR, id='A')
    dampd_raw = read_csv(DAMPD_DIR, id='D')

    print('AMPD Sample:\t' + str(len(amp_raw)))
    print('DAMPD Sample:\t' + str(len(dampd_raw)))

    # Merge Datasets
    merged_data = merge(amp_raw, dampd_raw)
    print('Merged Total:\t' + str(len(merged_data)))

    # Duplicates Check
    # TODO: Ask how to handle duplicate data.
    dup_list = duplicates(amp_raw, dampd_raw)
    print('Dup. Samples:\t' + str(len(dup_list)))

    # Filter & Replace Labels
    filtered = list(filter(lambda x: x[1] != 0, merged_data))
    replaced = replace_label(filtered)
    print('Filtered Count:\t' + str(len(replaced)))
    print()

    # Append PepType Column (Set All Real)
    output = list(map(lambda x: x + ['R'], replaced))

    # Generate Output File
    out = open(OUT_DIR, 'w')
    out.write('PepID,AMPLabel,AMP,PepType\n')
    for data in output: out.write(','.join([str(i) for i in data])+'\n')
    out.close()

    print('Output File: ' + OUT_DIR)
