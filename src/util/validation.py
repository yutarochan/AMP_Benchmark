'''
Result Validation Assertion
Given original dataset file and folder of results, report any missing samples.

Author: Yuya Jeremy Ong
'''
from __future__ import print_function
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orig", type=str, required=True, help="Original dataset to assert from.")
    parser.add_argument("--data", type=str, required=True, help="Input data to assert against.")
    parser.add_argument("--missing", type=str, required=True, help="Output for writing missing list.")
    return parser.parse_args()

def find_idx(data, pid):
    index = 0
    for d in data:
        if d[1:] == pid: break
        index += 1
    return index

if __name__ == '__main__':
    # Parse Arguments
    args = parse_args()

    # Read Dataset
    orig_raw = open(args.orig, 'r').read().split('\n')[:-1]
    test_raw = open(args.data, 'r').read().split('\n')[1:-1]

    # Build Dictionary of Original Data
    orig_id = list(map(lambda x: x[1:], orig_raw[::2]))
    test = { x.split(',')[0] : {'AMPLabel':x.split(',')[1], 'Prob':x.split(',')[2]} for x in test_raw }

    # Find Missing Index
    missing = list(set(orig_id) - set(test.keys()))

    if len(missing) > 0:
        # Generate Missing List
        miss_out = open(args.missing, 'w')
        for m in missing:
            idx = find_idx(orig_raw, m)
            miss_out.write(orig_raw[idx] + '\n')
            miss_out.write(orig_raw[idx+1] + '\n')
        miss_out.close()

    # Report Stats
    print('DONE')
    print('MISSING: ' + str(len(missing)) + ' / ' + str(len(orig_id)) + ' RECORDS')
