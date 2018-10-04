'''
CAMPR3 - Batch Prediction Routine
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Application Parameters
ROOT_URL = 'http://www.camp.bicnirrh.res.in/predict/'

class CAMPR3:
    def __init__(self, fasta_data, mode='SVM', batch_size=50, sleep=5):
        # Class Parameters
        self.data = fasta_data
        self.batch_size = batch_size * 2
        self.mode = mode    # SVM, RF, ANN, DA
        self.sleep = sleep

    def _get_ids(self, data):
        return data[::2]

    def _batch(self):
        for i in range(0, len(self.data), self.batch_size):
             yield (i, min(i + self.batch_size, len(self.data)))

    def process_job(self, data):
        # Initialize Selenium Web Driver
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")
        driver = webdriver.Chrome()
        driver.get(ROOT_URL)

        res = []
        try:
            # Locate Web Elements
            textarea =  driver.find_element_by_name('S1')
            cbs = driver.find_elements_by_name('algo[]')
            submit = driver.find_element_by_name('B1')

            # Populate Form
            textarea.send_keys('\n'.join(data))
            if self.mode == 'SVM': cbs[0].click()
            elif self.mode == 'RF': cbs[1].click()
            elif self.mode == 'ANN': cbs[2].click()
            elif self.mode == 'DA': cbs[3].click()

            submit.click()  # Submit Form

            # Extract Results Table
            res_tbl = driver.find_elements_by_tag_name('tbody')
            table = res_tbl[3].text.split('\n')

            # Check for warning signal for index errors.
            if 'Warning' in table[1]: table = table[5:]
            else: table = table[4:]


            # Build Index Based Dictionary
            if self.mode == 'ANN':
                score_dict = {int(t.split(' ')[0]) : t.split(' ')[1] for t in table}
            else:
                score_dict = {int(t.split(' ')[0]) : [t.split(' ')[1], t.split(' ')[2]] for t in table}

            # Process Table Results
            for i, id in enumerate(data[::2]):
                if i+1 in score_dict:
                    if self.mode == 'ANN':
                        label = 1 if score_dict[i+1] == 'AMP' else 0
                        res.append([id[1:], label, float(label)])
                    else:
                        label = 1 if score_dict[i+1][0] == 'AMP' else 0
                        res.append([id[1:], label, float(score_dict[i+1][1])])
                else:
                    res.append([id[1:], -999, -999])

        except Exception as e:
            print(e)
            time.sleep(15)
        finally:
             driver.close()

        return res

    # Prediction Function
    def predict(self):
        results = []
        for i, (st, ed) in enumerate(self._batch()):
            print('> PROCESSING BATCH #' + str(i))
            results += self.process_job(self.data[st:ed])
            time.sleep(self.sleep)
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
    server = CAMPR3(data, mode='SVM')
    server.predict()
