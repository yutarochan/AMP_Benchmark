'''
DBAASP - Batch Prediction Routine
Author: Yuya Jeremy Ong (jyo5006@psu.edu)
'''
from __future__ import print_function
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

# Application URL Parameters
ROOT_URL = 'https://dbaasp.org/'
FORM_URL = ROOT_URL + 'prediction'
ACTION_URL = ROOT_URL + 'utility/general-prediction'

class DBAASP:
    def __init__(self, fasta_data, batch_size=50, wait=5, sleep=5):
        # Class Parameters
        self.data = fasta_data
        self.batch_size = batch_size * 2
        self.wait_time = wait
        self.sleep = sleep

    def _batch(self):
        for i in range(0, len(self.data), self.batch_size):
             yield (i, min(i + self.batch_size, len(self.data)))

    def process_job(self, data):
        # Initialize Selenium Web Driver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(FORM_URL)

        time.sleep(5)

        res = []
        try:
            # Locate Web Elements
            textarea = driver.find_element_by_id('data')
            submit = driver.find_element_by_class_name('btn-primary')

            textarea.send_keys('\n'.join(data)) # Populate Form
            submit.click()                      # Submit Form

            # Wait Until Table Populated
            WebDriverWait(driver, self.wait_time).until(EC.presence_of_element_located((By.TAG_NAME, "th")))
            res_table = driver.find_elements_by_tag_name('tbody')   # Extract Result Table

            # Process Results to Defined Format
            output = ' '.join([e.text for e in res_table]).split('\n')
            for o in output:
                if o.split(' ')[1] == 'AMP':
                    res.append([o.split(' ')[0], 1, 1.0])
                elif o.split(' ')[1] == 'Non-AMP':
                    res.append([o.split(' ')[0], 0, 0.0])
        except Exception as e:
            print(e)
        finally:
            driver.close()

        return res

    def _binf(self, data):
        data_id = [i[1:] for i in data[::2]]
        print('>> IDs: ' + str(data_id))
        res = self.process_job(data)
        if len(data) == 2 and len(res) == 0: return []
        if len(res) > 0: return res

        time.sleep(self.sleep)
        mid = int(len(data)/2) + 1 if int(len(data)/2) % 2 != 0 else int(len(data)/2)
        return self._binf(data[:mid]) + self._binf(data[mid:])

    def predict(self):
        results = []
        for i, (st, ed) in enumerate(self._batch()):
            print('> PROCESSING BATCH #' + str(i))
            res = self._binf(self.data[st:ed])
            res_id = [i[0] for i in res]

            # Impute Unavailable Results (with -999)
            for id in self.data[st:ed][::2]:
                if id[1:] not in res_id: res.append([id[1:], -999, -999])

            results += res
        return results

def read_fasta(data_dir):
    return open(data_dir, 'r').read().split('\n')[:-1]

if __name__ == '__main__':
    # Application Parameters
    DATA_DIR = '../../data/fasta/data.fasta.txt'

    # Load FASTA Dataset
    data = read_fasta(DATA_DIR)

    # Unit Test Functions
    server = DBAASP(data)
    # result = server.predict()
