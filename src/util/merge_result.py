'''
Merge CSV Utility
Merges CSV and Validates Record Against Original - Reports Missing Records

Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import argparse
from os import listdir
from os.path import isfile, join

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, required=True, help="Dataset folder to merge files with.")
    parser.add_argument("--out", type=str, required=True, help="Output filename of csv file.")
    return parser.parse_args()

if __name__ == '__main__':
    # Parse Arguments
    args = parse_args()

    # Collect Result to List
    data = []
    data_file = [f for f in listdir(args.dir) if isfile(join(args.dir, f))]
    for file in data_file:
        raw = open(args.dir + '/' + file, 'r').read().split('\n')[1:-1]
        data += raw

    # Write to Output File
    out = open(args.out, 'w')
    out.write('PepID,AMPLabel,Prob\n')
    for row in data: out.write(row + '\n')
    out.close()

    print('DONE')
    print('MERGED ' + str(len(data)) + ' RECORDS')
