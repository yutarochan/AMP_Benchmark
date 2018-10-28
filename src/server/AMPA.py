'''
AMPA - Batch Prediction Routine
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import sys
import math
import time
import requests
from bs4 import BeautifulSoup

# Application URL Parameters
ROOT_URL = 'http://tcoffee.crg.cat/apps/ampa/'
ACTION_URL = ROOT_URL + 'do:ampa'
STATUS_URL = ROOT_URL + 'status'
RESULT_URL = 'http://tcoffee.crg.cat/data/'

class AMPA(object):
    def __init__(self, fasta_data, batch_size=50, window=7, threshold=0.225, status_time=5, sleep=2):
        # Class Parameters
        self.data = fasta_data
        self.batch_size = batch_size * 2
        self.status_time = status_time
        self.sleep = sleep

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

    # Parse CSV String
    def _parse_csv(self, data):
        raw = data.split('\n')[:-1]
        return [r.split(',') for r in raw]

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
                    break

            # Obtain Prediction Results
            if self._checkJobStatus(job_id) == 'Done':
                # Note: Result set only provides positive examples.
                result = self._parse_csv(self._getResult(job_id))

                pos_res = {}
                for r in result:
                    if r[0] in pos_res:
                        if pos_res[r[0]] > 1 - (float(r[5][:-1]) / 100):
                            r[0] = 1 - (float(r[5][:-1]) / 100)
                    else:
                        pos_res[r[0]] = 1 - (float(r[5][:-1]) / 100)

                # Aggregate Results
                res = []
                for id in data[::2]:
                    label = 1 if id[1:] in pos_res else 0
                    prob = pos_res[id[1:]] if id[1:] in pos_res else 0.0
                    res.append([id[1:], label, prob])
                return res # [PepID, Label, Prob]

            # TODO: Throw exception here if it fails!
            # if self._checkJobStatus(job_id) == 'Failed':
            #    print('>> SUBMISSION FAILED!')

            return None
        except Exception as e:
            print(e)

    def _binf(self, data):
        res = self.process_job(data)
        if len(data) == 2 and res == None: return []
        if res != None: return res
        mid = int(len(data)/2) + 1 if int(len(data)/2) % 2 != 0 else int(len(data)/2)
        return self._binf(data[:mid]) + self._binf(data[mid:])

    # Prediction Function
    def predict(self):
        results = []
        for st, ed in self._batch():
            # Process Batch Job (Use Binary Filter for Robust Error-Handling Process)
            res = self._binf(self.data[st:ed])
            res_id = [i[0] for i in res]

            # Impute Unavailable Results (with -999)
            for id in self.data[st:ed][::2]:
                if id[1:] not in res_id: res.append([id[1:], -999, -999])

            results += res          # Append to Final Result Set
            time.sleep(self.sleep)  # Sleep to Avoid Overwhelming Server
        return results

def read_fasta(data_dir):
    return open(data_dir, 'r').read().split('\n')[:-1]

# Unit Testing
if __name__ == '__main__':
    # Application Parameters
    DATA_DIR = '../../data/fasta/data.fasta.txt'

    # Load FASTA Dataset
    data = read_fasta(DATA_DIR)

    # Unit Test Functions
    server = AMPA(data[:1000])
    # result = server.process_job(data[100:200])
    res = server.predict()
    print(res)
