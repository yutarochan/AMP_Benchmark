'''
AMP Prediction Job Submission
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import sys
import argparse
from server import ADAM, AMPA, CAMPR3, DBAASP

def parse_arg():
    # TODO: Consider index/ID based batch processing. Give parameter to start from certain indexself.
    parser = argparse.ArgumentParser()
    parser.add_argument("--ls", action="store_true", help="List all available servers.")
    parser.add_argument('--data', type=str, help='Path to dataset (Must be in FASTA format).')
    parser.add_argument('--out', type=str, help='Path to result output.')
    parser.add_argument('--model', type=str, help='Model server to use. (Use ls to find the model names).')
    parser.add_argument('--batch_size', type=int, default=50, help='Number of data to handle per batch transaction.')
    parser.add_argument('--start_id', type=str, help='Specify ID for starting index for batch processing.')
    parser.add_argument('--job_size', type=int, help='How many samples to submit per job.')
    parser.add_argument('--missing', type=bool, default=False, help='If provided, will only process the indexed values listed.')
    return parser.parse_args()

def server_dict():
    data = open('../data/servers.csv').read().split('\n')[1:-1]
    servers = {}
    for d in data:
        r = d.split(',')
        servers[r[1]] = r[0]
    return servers

def list_server():
    print('[AVAILABLE MODEL SERVERS]')
    print('> ALL')
    data = open('../data/servers.csv').read().split('\n')[1:-1]
    servers = server_dict().keys()
    for s in servers: print('> ' + s)
    sys.exit()

def read_fasta(data_dir):
    return open(data_dir, 'r').read().split('\n')[:-1]

def find_idx(data, pid):
    index = 0
    for d in data:
        if d[1:] == pid: break
        index += 1
    return index

def write_log(out_dir, data):
    out = open(out_dir, 'w')
    out.write('PepID,AMPLabel,Prob\n')
    for d in data: out.write(d[0] + ',' + str(d[1]) + ',' + str(d[2]) + '\n')
    out.close()

if __name__ == '__main__':
    args = parse_arg()          # Parse Arguments
    if args.ls: list_server()   # List Servers

    # Load Dataset
    print('> LOADING DATA FILE: ' + str(args.data))
    if args.data is not None:
        data = read_fasta(args.data)
    else:
        print('> ERROR: Please provide valid FASTA dataset path.')
        sys.exit()
    print('> LOADED ' + str(len(data)) + ' AMP SAMPLES\n')

    if not args.missing:
        # Find Start ID
        if args.start_id is not None:
            st = find_idx(data, args.start_id)
        else: st = 0

        # Compute End Index
        if args.job_size is not None:
            if st + (args.job_size * 2) >= len(data): ed = len(data)
            else: ed = st + (args.job_size * 2)
        else: ed = len(data)

    # Process Predictions
    if args.model == 'ALL' or args.model == 'AMPA':     # PARTIALLY-VERIFIED (NON-ROBUST/STABLE)
        print('[PROCESSING: AMPA]')
        if args.missing == False:
            srv = AMPA.AMPA(data[st:ed], batch_size=args.batch_size)
            write_log(args.out + '/' + args.data.split('/')[-1] + '_' + str(st) + '_' + str(ed)  + '_AMPA.csv', srv.predict())

    if args.model == 'ALL' or args.model == 'DBAASP':   # VERIFIED
        print('[PROCESSING: DBAASP]')
        if args.missing == False:
            srv = DBAASP.DBAASP(data[st:ed], batch_size=args.batch_size)
            write_log(args.out + '/' + args.data.split('/')[-1] + '_' + str(st) + '_' + str(ed) + '_DBAASP.csv', srv.predict())

    if args.model == 'ALL' or args.model == 'ADAM_SVM': # VERIFIED
        print('[PROCESSING: ADAM_SVM]')
        if args.missing == False:
            srv = ADAM.ADAM(data[st:ed], mode='SVM', batch_size=args.batch_size)
            write_log(args.out + '/' + args.data.split('/')[-1] + '_' + str(st) + '_' + str(ed) + '_ADAM-SVM.csv', srv.predict())
        else:
            srv = ADAM.ADAM(data, mode='SVM', batch_size=args.batch_size)
            write_log(args.out + '/' + args.data.split('/')[-1] + '_MISSING_ADAM-SVM.csv', srv.predict())

    if args.model == 'ALL' or args.model == 'ADAM_HMM': # VERIFIED
        print('[PROCESSING: ADAM_HMM]')
        if args.missing == False:
            srv = ADAM.ADAM(data[st:ed], mode='HMM', batch_size=args.batch_size)
            write_log(args.out + '/' + args.data.split('/')[-1] + '_' + str(st) + '_' + str(ed) + '_ADAM-HMM.csv', srv.predict())

    if args.model == 'ALL' or args.model == 'CMPR3_SVM':    # STABLE
        print('[PROCESSING: CAMPR3_SVM]')
        if args.missing == False:
            srv = CAMPR3.CAMPR3(data[st:ed], mode='SVM', batch_size=args.batch_size)
            write_log(args.out + '/' + args.data.split('/')[-1] + '_' + str(st) + '_' + str(ed) + '_CAMPR3-SVM.csv', srv.predict())
        else:
            srv = CAMPR3.CAMPR3(data, mode='SVM', batch_size=args.batch_size)
            write_log(args.out + '/' + args.data.split('/')[-1] + '_MISSING_CAMPR3-SVM.csv', srv.predict())

    if args.model == 'ALL' or args.model == 'CMPR3_RF':     # STABLE
        print('[PROCESSING: CAMPR3_RF]')
        if args.missing == False:
            srv = CAMPR3.CAMPR3(data[st:ed], mode='RF', batch_size=args.batch_size)
            write_log(args.out + '/' + args.data.split('/')[-1] + '_' + str(st) + '_' + str(ed) + '_CAMPR3-RF.csv', srv.predict())

    if args.model == 'ALL' or args.model == 'CMPR3_ANN':    # STABLE
        print('[PROCESSING: CAMPR3_ANN]')
        if args.missing == False:
            srv = CAMPR3.CAMPR3(data[st:ed], mode='ANN', batch_size=args.batch_size)
            write_log(args.out + '/' + args.data.split('/')[-1] + '_' + str(st) + '_' + str(ed) + '_CAMPR3-ANN.csv', srv.predict())

    if args.model == 'ALL' or args.model == 'CMPR3_DA':
        print('[PROCESSING: CAMPR3_DA]')
        if args.missing == False:
            srv = CAMPR3.CAMPR3(data[st:ed], mode='DA', batch_size=args.batch_size)
            write_log(args.out + '/' + args.data.split('/')[-1] + '_' + str(st) + '_' + str(ed) + '_CAMPR3-DA.csv', srv.predict())
