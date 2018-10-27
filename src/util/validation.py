'''
Result Validation Assertion
Given original dataset file and folder of results, report any missing samples.

Author: Yuya Jeremy Ong
'''
from __future__ import print_function
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orig", type=str, required=True, help="Original dataset to assert from.")
    parser.add_argument("--data", type=str, required=True, help="Input data to assert against.")
    return parser.parse_args()
