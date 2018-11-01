'''
Output File Merge: Generate Final Output Based on Specified Schema
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--proc", type=str, required=True, help="Raw proc file to merge.")
    parser.add_argument("--res", type=str, required=True, help="Prediction results file.")
    parser.add_argument("--out", type=str, required=True, help="Output filename of csv file.")
    return parser.parse_args()

if __name__ == '__main__':
    # Parse Arguments
    args = parse_args()

    # Build Data Dict
    data = {}
    proc = open(args.proc, 'r').read().split('\n')[1:-1]
    for i in range(0, len(proc)):
        row = proc[i].replace('\n', '').split(',')
        data[row[0]] = {'PepSeq' : row[2], 'PepType' : row[3], 'AMPLabel' : row[1]}

    # Merge with Predictions
    pred = open(args.res, 'r').read().split('\n')[1:-1]
    for p in pred:
        row = p.split(',')
        data[row[0]]['PredScore'] = row[2]
        data[row[0]]['PredLabel'] = row[1]

    # Validate Merge
    for d in data:
        if len(data[d].keys()) != 5:
            print('INVALID FILE!')
            sys.exit()

    print('MERGE COMPLETE - DATASET VALID!')

    # Output File
    output = open(args.out, 'w')
    output.write('PepID,PepSeq,PepType,AMPLabel,PredScore,PredLabel\n')
    for d in data:
        row = d+','+data[d]['PepSeq']+','+data[d]['PepType']+','+data[d]['AMPLabel']+','+data[d]['PredScore']+','+data[d]['PredLabel']+'\n'
        output.write(row)
    output.close()

    print('DONE!')
