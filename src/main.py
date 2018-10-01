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

    # Process Predictions
    if args.model == 'ALL' or args.model == 'AMPA':     # PARTIALLY-VERIFIED (NON-ROBUST/STABLE)
        print('[PROCESSING: AMPA]')
        srv = AMPA.AMPA(data, batch_size=args.batch_size)
        write_log(args.out + '/' + args.data.split('/')[-1] + '_AMPA.csv', srv.predict())

    if args.model == 'ALL' or args.model == 'DBAASP':   # VERIFIED
        print('[PROCESSING: DBAASP]')
        srv = DBAASP.DBAASP(data[:10000], batch_size=args.batch_size)
        write_log(args.out + '/' + args.data.split('/')[-1] + '_DBAASP.csv', srv.predict())

    if args.model == 'ALL' or args.model == 'ADAM_SVM': # VERIFIED
        print('[PROCESSING: ADAM_SVM]')
        srv = ADAM.ADAM(data, mode='SVM', batch_size=args.batch_size)
        write_log(args.out + '/' + args.data.split('/')[-1] + '_ADAM-SVM.csv', srv.predict())

    if args.model == 'ALL' or args.model == 'ADAM_HMM': # VERIFIED
        print('[PROCESSING: ADAM_HMM]')
        srv = ADAM.ADAM(data, mode='HMM', batch_size=args.batch_size)
        write_log(args.out + '/' + args.data.split('/')[-1] + '_ADAM-HMM.csv', srv.predict())

    if args.model == 'ALL' or args.model == 'CMPR3_SVM':
        print('[PROCESSING: CAMPR3_SVM]')
        srv = CAMPR3.CAMPR3(data, mode='SVM', batch_size=args.batch_size)
        write_log(args.out + '/' + args.data.split('.')[0] + '_CAMPR3-SVM.csv', srv.predict())

    if args.model == 'ALL' or args.model == 'CMPR3_RF':
        print('[PROCESSING: CAMPR3_RF]')
        srv = CAMPR3.DBAASP(data, mode='RF', batch_size=args.batch_size)
        write_log(args.out + '/' + args.data.split('.')[0] + '_CAMPR3-RF.csv', srv.predict())

    if args.model == 'ALL' or args.model == 'CMPR3_ANN':
        print('[PROCESSING: CAMPR3_ANN]')
        srv = CAMPR3.CAMPR3(data, mode='ANN', batch_size=args.batch_size)
        write_log(args.out + '/' + args.data.split('.')[0] + '_CAMPR3-ANN.csv', srv.predict())

    if args.model == 'ALL' or args.model == 'CMPR3_DA':
        print('[PROCESSING: CAMPR3_DA]')
        srv = CAMPR3.CAMPR3(data, mode='DA', batch_size=args.batch_size)
        write_log(args.out + '/' + args.data.split('.')[0] + '_CAMPR3-DA.csv', srv.predict())
