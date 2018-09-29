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
from selenium.webdriver.support import expected_conditions as EC

# Application URL Parameters
ROOT_URL = 'https://dbaasp.org/'
FORM_URL = ROOT_URL + 'prediction'
ACTION_URL = ROOT_URL + 'utility/general-prediction'

class DBAASP:
    def __init__(self, fasta_data, batch_size=50, wait=5):
        # Class Parameters
        self.data = fasta_data
        self.batch_size = batch_size * 2
        self.wait_time = wait

    def _batch(self):
        for i in range(0, len(self.data), self.batch_size):
             yield (i, min(i + self.batch_size, len(self.data)))

    def process_job(self, data):
        # Initialize Selenium Web Driver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(FORM_URL)

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

    def predict(self):
        results = []
        for i, (st, ed) in enumerate(self._batch()):
            print('> PROCESSING BATCH #' + str(i))
            results.append(self.process_job(self.data[st:ed]))
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
    result = server.predict()
