'''
AMPA - Batch Prediction Routine
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import math
import time
import requests
from bs4 import BeautifulSoup

# Application URL Parameters
ROOT_URL = 'http://tcoffee.crg.cat/apps/ampa/'
ACTION_URL = ROOT_URL + 'do:ampa'
STATUS_URL = ROOT_URL + 'status'
RESULT_URL = 'http://tcoffee.crg.cat/data/'

class AMPA:
    def __init__(self, fasta_data, batch_size=50, window=7, threshold=0.225, status_time=10):
        # Class Parameters
        self.data = fasta_data
        self.batch_size = batch_size
        self.status_time = status_time

        # Server Parameters
        self.window = window
        self.threshold = threshold

    # Server accepts at most 50, batch data into chunks via generator func.
    def _batch(self):
        for i in range(0, len(self.data), self.batch_size):
             yield (i, min(i + self.batch_size, len(self.data)))

    # Extract JobID from Page
    def _extJID(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup.find('h2').text.split(' ')[-1][:-1]

    # Extract Job Status
    def _checkJobStatus(self, job_id):
        req = requests.get(STATUS_URL+'?rid='+job_id)
        return req.text

    # Extract CSV Tabular Results
    def _getResult(self, job_id):
        req = requests.get(RESULT_URL + job_id + '/data.csv')
        return req.text

    # Single Job Submission Function
    def process_job(self, data):
        # Build Payload
        body_data = {
            'protein' : '\n'.join(data),
            'window' : self.window,
            'threshold' : self.threshold
        }

        try:
            # Submit POST Request - Return JobID
            req = requests.post(ACTION_URL, params=body_data)
            job_id = self._extJID(req.text)

            print('> PROCESSING JOB: ' + job_id)

            # Check Job Status
            while self._checkJobStatus(job_id) == 'Running':
                time.sleep(self.status_time)  # Wait 10 Seconds
                if self._checkJobStatus(job_id) == 'Done' or self._checkJobStatus(job_id) == 'Failed':
                    print(self._checkJobStatus(job_id))
                    break

            # Obtain Prediction Results
            # TODO: Implement CSV Parser and Return as List
            if self._checkJobStatus(job_id) == 'Done':
                return self._getResult(job_id)

            # TODO: Throw exception here if it fails!
            return None
        except Exception as e:
            print(e)

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
