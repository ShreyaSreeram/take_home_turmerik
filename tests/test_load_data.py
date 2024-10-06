import unittest
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from load_data import load_patient_data

class TestLoadData(unittest.TestCase):
    def test_load_data(self):
        #Call the function to load and consolidate data
        data = load_patient_data()
        
        #Ensure the returned data is a DataFrame
        self.assertIsInstance(data, pd.DataFrame)
        self.assertIn('PATIENT', data.columns)  #Ensure 'PATIENT' column exists

if __name__ == '__main__':
    unittest.main()