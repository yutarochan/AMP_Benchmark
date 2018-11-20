'''
ADAM - Batch Prediction Routine
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import time
import requests
from bs4 import BeautifulSoup

# Application Parameters
ROOT_URL = 'http://bioinformatics.cs.ntou.edu.tw/ADAM/'
ACTION_URL_SVM = ROOT_URL + 'svm_predict.php'
ACTION_URL_HMM = ROOT_URL + 'hmm_predict.php'
ACTION_URL = ACTION_URL_SVM

class ADAM(object):
    def __init__(self, fasta_data, mode='SVM', batch_size=50, sleep=10):
        # Class Parameters
        self.data = fasta_data
        self.batch_size = batch_size * 2
        self.mode = mode    # SVM or HMM
        self.sleep = sleep

        if self.mode == 'SVM': ACTION_URL = ACTION_URL_SVM
        elif self.mode == 'HMM': ACTION_URL = ACTION_URL_HMM

    def _batch(self):
        for i in range(0, len(self.data), self.batch_size):
             yield (i, min(i + self.batch_size, len(self.data)))

    def process_job(self, data):
        # Build Payload and Header
        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"text\"\r\n\r\n" + '\n'.join(data) + "\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'cache-control': "no-cache",
            'postman-token': "f04216f8-10de-d91a-2935-cc8fc01edb95"
        }

        out = []
        try:
            # Submit POST Request - Return JobID
            req = requests.post(ACTION_URL, data=payload, headers=headers)

            # Extract Results Table
            soup = BeautifulSoup(req.text, features="html5lib")
            if len(list(soup.find_all('tbody'))) == 1: return None
            table = list(soup.find_all('tbody')[1])[1:]

            # Format Result
            ids = list(map(lambda x: x[1:], data[::2]))
            print(ids)
            for t in table:
                row = [i.text for i in t.find_all('td')]
                if row[0] not in ids: continue
                if row[3] == 'AMP': out.append([row[0], 1, 1.0])
                elif row[3] == 'Non AMP': out.append([row[0], 0, 0.0])

        except Exception as e:
            print(e)

        return out  # [PepID, Label, Prob]

    def _binf(self, data):
        res = self.process_job(data)
        if len(data) == 2 and res == None: return []
        if res != None: return res
        mid = int(len(data)/2) + 1 if int(len(data)/2) % 2 != 0 else int(len(data)/2)
        return self._binf(data[:mid]) + self._binf(data[mid:])

    # Prediction Function
    # TODO: Add sleep function so we won't overwhelm the server
    def predict(self):
        results = []
        for i, (st, ed) in enumerate(self._batch()):
            print('> PROCESSING BATCH #' + str(i))

            # Process Batch Job (Use Binary Filter for Robust Error-Handling Process)
            res = self._binf(self.data[st:ed])
            res_id = [i[0] for i in res]

            # Impute Unavailable Results (with -999)
            for id in self.data[st:ed][::2]:
                if id[1:] not in res_id: res.append([id[1:], -999, -999])

            results += res
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
    server = ADAM(data, mode='SVM')
    server.predict()
    # server.process_job(data[10240:10244])
