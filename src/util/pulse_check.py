'''
Server Pulse Check: Check if a server is back up for ADAM
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import time
import notify2
import requests
from bs4 import BeautifulSoup

# Application Parameters
ROOT_URL = 'http://bioinformatics.cs.ntou.edu.tw/ADAM/'
ACTION_URL_SVM = ROOT_URL + 'svm_predict.php'
ACTION_URL_HMM = ROOT_URL + 'hmm_predict.php'
ACTION_URL = ACTION_URL_SVM

class ADAM(object):
    def __init__(self, fasta_data, mode='SVM', batch_size=50, sleep=0):
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
            # Process Batch Job (Use Binary Filter for Robust Error-Handling Process)
            res = self._binf(self.data[st:ed])
            res_id = [i[0] for i in res]

            # Impute Unavailable Results (with -999)
            for id in self.data[st:ed][::2]:
                if id[1:] not in res_id: res.append([id[1:], -999, -999])

            results += res

        return results

def out_message(message, face=0):
    print('(\__/)')
    if face == 0: print('(•ㅅ•)    -\t' + message)
    elif face == 1: print('(TㅅT)    -\t' + message)
    elif face == 2: print('(>ㅅ<)    -\t' + message)
    print('/ 　 づ')
    print('\n')

if __name__ == '__main__':
    # Setup Notification Object
    notify2.init("PulseCheck")
    n = notify2.Notification(None)
    n.set_urgency(notify2.URGENCY_NORMAL)
    n.set_timeout(15000)

    timeout = 900    # 15 Min (in sec)
    payload = ['>TEST1','AAAAGSVWGAVNYTSDCNGECKRRGYKGGYCGSFANVNCWCET']

    # Pulse Check Loop
    while True:
        out_message('I\'m gonna test the server...', 0)

        server = ADAM(payload, mode='SVM')
        res = server.predict()

        if res[0][1] == -999:
            n.update('Server Puse Check', 'ADAM is currently OFFLINE')
            out_message('Looks like Adam is dead...', 1)
        else:
            n.update('Server Puse Check', 'ADAM is currently ONLINE')
            out_message('Adam is alive!', 2)

        n.show()

        time.sleep(timeout)
