'''
AMP Dataset Generation
Author: Yuya Jeremy Ong (yuyajong@ibm.com)
'''
from __future__ import print_function
import random
import warnings
import numpy as np
import pandas as pd

# Supress User Warnings
warnings.filterwarnings('ignore')

# Application Parameters
DATA_ROOT = '../data/out/data3.fasta.txt/'
SERVERS = ['ADAM_HMM', 'ADAM_SVM', 'AMPA', 'CMPR3_ANN', 'CMPR3_DA', 'CMPR3_RF', 'CMPR3_SVM', 'DBAASP']
DATASET = ['A', 'D']
REVERSE = ['', 'R', 'R1', 'R2', 'R3']
SEED = 9892 # SEED for PRNG

# Initialize PRNG
random.seed(SEED)
np.random.seed(SEED)

# Helper Function for Display
def data_type(d, r):
    d_type = 'APD' if d == 'A' else 'DAMPD'
    if r == '': r_type = 'BAL'
    elif r[0] == 'R':
        r_type = 'RAND' + str(r[1]) if len(r) > 1 else 'REV'
    return d_type, r_type

# Load Original Dataset
data = {}
for s in SERVERS:
    raw = pd.read_csv(DATA_ROOT + s + '.csv')
    data[s] = {}
    for d in DATASET:
        data[s][d] = {}
        for r in REVERSE:
            # Append True Values
            data[s][d][r] = pd.DataFrame(raw[raw.PepID.str.contains(d)]
                                            [raw.PepID.str.contains('R') == False]
                                            [raw.AMPLabel == 1])

            # Filter Operations by Type
            if r == 'R':
                data[s][d][r] = data[s][d][r].append(raw[raw.PepID.str.contains(d)]
                                                        [raw.PepID.str.contains('R') == True]
                                                        [raw.PepID.str.contains('R1') == False]
                                                        [raw.PepID.str.contains('R2') == False]
                                                        [raw.PepID.str.contains('R3') == False])
            elif r != '':
                data[s][d][r] = data[s][d][r].append(raw[raw.PepID.str.contains(d)]
                                                        [raw.PepID.str.contains(r)])

            d_type, r_type = data_type(d, r)

# Rebalance Dataset Distribution with Positive Samples
orig_dist = {}
for s in SERVERS:
    raw = pd.read_csv(DATA_ROOT + s + '.csv')
    orig_dist[s] = {}
    for d in DATASET:
        # Evaluate Sequence Length Positive Samples
        len_count = raw[raw.PepID.str.contains(d)][raw.PepID.str.contains('R') == False][raw.AMPLabel == 1]['PepSeq'].str.len()

        # Track Distribution from Positive Samples
        orig_dist[s][d] = {}
        for l in len_count:
            if l not in orig_dist[s][d]:
                orig_dist[s][d][l] = 0
            orig_dist[s][d][l] += 1

out_data = []
for s in SERVERS:
    raw = pd.read_csv(DATA_ROOT + s + '.csv')
    for d in DATASET:
        # Identify Negative Sequence Distribution
        dat = raw[raw.PepID.str.contains(d)][raw.PepID.str.contains('R') == False][raw.AMPLabel == 0]
        seq_len = dat['PepSeq'].astype(str).str.len()

        # Randomly Sample Based on Number of Positive Samples
        for k in list(orig_dist[s][d]):
            idx = seq_len[seq_len == k].index.values
            idx_sel = np.random.choice(len(idx), orig_dist[s][d][k], replace=False)

            data[s][d][''] = data[s][d][''].append(dat[dat.index.isin(idx[idx_sel])])

        # Collect Pep ID for Consolidation
        for r in REVERSE:
            for id in data[s][d][r][['PepID', 'PepSeq', 'AMPLabel']].values.tolist():
                if id not in out_data: out_data.append(id)

# Initialize Output DataFrame Structure
out = []
for row in out_data:
    o = [row[0][0], row[0], 'T' if len(row[0]) == 6 else row[0][6:], row[1], row[2]]
    o += [-1.0 for i in range(len(SERVERS))]
    out.append(o)
out_df = pd.DataFrame(out, columns=['Database', 'PepID', 'PepType', 'PepSeq', 'PepLabel'] + SERVERS)

# Populate Server Prediction in DataFrame
for s in SERVERS:
    '''
    for d in DATASET:
        for r in REVERSE:
            for row in data[s][d][r].values.tolist():
                out_df.loc[out_df['PepID'] == row[0], s] = row[4]
    '''
    raw = pd.read_csv(DATA_ROOT + s + '.csv')
    for row in raw.values.tolist():
        out_df.loc[out_df['PepID'] == row[0], s] = row[4]
        
out_df.to_csv('../data/AMP_dataset.csv', index=False)