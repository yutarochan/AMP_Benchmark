'''
MLAMP - Batch Prediction Routine
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import sys
import time

# Application Parameters
ROOT_URL = 'http://www.camp.bicnirrh.res.in/predict/'

class MLAMP:
    def __init__(self, fasta_data, batch_size=50, sleep=5):
        # Class Parameters
        self.data = fasta_data
        self.batch_size = batch_size * 2
        self.sleep = sleep

    def _get_ids(self, data):
        return data[::2]

    def _batch(self):
        for i in range(0, len(self.data), self.batch_size):
             yield (i, min(i + self.batch_size, len(self.data)))

    def process_job(self, data):
        # Initialize Selenium Web Driver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(ROOT_URL)

        res = []
        try:
            # Locate Web Elements
            textarea =  driver.find_element_by_name('S1')
            cbs = driver.find_elements_by_name('algo[]')
            submit = driver.find_element_by_name('B1')

        except Exception as e:
            print(e)
            time.sleep(15)
        finally:
             driver.close()

        sys.exit()
        return res

    # Prediction Function
    def predict(self):
        results = []
        for i, (st, ed) in enumerate(self._batch()):
            print('> PROCESSING BATCH #' + str(i))
            results += self.process_job(self.data[st:ed])
            sys.exit()
            time.sleep(self.sleep)
        return results

def read_fasta(data_dir):
    return open(data_dir, 'r').read().split('\n')[:-1]

if __name__ == '__main__':
    # Application Parameters
    DATA_DIR = '../../data/fasta/data.fasta.txt'

    # Load FASTA Dataset
    data = read_fasta(DATA_DIR)

    # Unit Test Functions
    server = MLAMP(data)
    server.predict()
