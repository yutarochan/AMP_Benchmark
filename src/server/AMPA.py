'''
AMPA - Batch Prediction Routine
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import math
import requests

# Application URL Parameters
ROOT_URL = 'http://tcoffee.crg.cat/apps/ampa/'
ACTION_URL = ROOT_URL + 'do:ampa'
STATUS_URL = ROOT_URL + 'status'
RESULT_URL = ROOT_URL + 'result'

class AMPA:
    def __init__(self, fasta_data, batch_size=50, window=7, threshold=0.225):
        # Class Parameters
        self.data = fasta_data
        self.batch_size = batch_size

        # Server Parameters
        self.window = window
        self.threshold = threshold

    # Server accepts at most 50, batch data into chunks via generator func.
    def batch(self):
        for i in range(0, len(self.data), self.batch_size):
             yield (i, min(i + self.batch_size, len(self.data)))

    # Single Job Submission Function
    def process_job(self, data):
        # Build Payload
        body_data = {
            'protein' : '\n'.join(data),
            'window' : self.window,
            'threshold' : self.threshold
        }

        # Submit Requests
        try:
            req = requests.post(ACTION_URL, params=body_data)
            print(req)
        except Exception as e:
            print(e)

        return None

    # Prediction Function
    def predict(self):
        return None

def read_fasta(data_dir):
    return open(data_dir, 'r').read().split('\n')[:-1]

# Unit Testing
if __name__ == '__main__':
    # Application Parameters
    DATA_DIR = '../../data/fasta/data.fasta.txt'

    # Load FASTA Dataset
    data = read_fasta(DATA_DIR)

    # Unit Test Functions
    server = AMPA(data)

    # Test 1: Generator Function Test
    # for i in server.batch(): print(i)

    # Test 2: Single Job Submission Test
    server.process_job(data[0:10])
