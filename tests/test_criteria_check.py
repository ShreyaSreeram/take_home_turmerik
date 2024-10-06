import unittest
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from criteria_check import check_inclusion_criteria, check_exclusion_criteria_spacy

import pandas as pd

class TestInclusionCriteria(unittest.TestCase):
    def test_valid_age_range(self):
        #Ensuring the patient is within the trial's age range
        birthdate = '1980-01-01'
        min_age = '30 Years'
        max_age = '60 Years'
        self.assertTrue(check_inclusion_criteria(birthdate, min_age, max_age))

    def test_age_below_min(self):
        #Ensuring the patient is too young for the trial
        birthdate = '2010-01-01'
        min_age = '30 Years'
        max_age = '60 Years'
        self.assertFalse(check_inclusion_criteria(birthdate, min_age, max_age))

    def test_age_above_max(self):
        #Ensuring the patient is too old for the trial
        birthdate = '1930-01-01'
        min_age = '30 Years'
        max_age = '60 Years'
        self.assertFalse(check_inclusion_criteria(birthdate, min_age, max_age))

    def test_missing_birthdate(self):
        #Ensuring the patient has no birthdate (NaN or None)
        birthdate = None
        min_age = '30 Years'
        max_age = '60 Years'
        self.assertFalse(check_inclusion_criteria(birthdate, min_age, max_age))

if __name__ == '__main__':
    unittest.main()



class TestExclusionCriteria(unittest.TestCase):
    def test_no_exclusion(self):
        patient_conditions = "Diabetes"
        patient_medications = "Insulin"
        trial_excluded_conditions = "Cancer, HIV"

        #Ensuring the patient should not be excluded
        self.assertTrue(check_exclusion_criteria_spacy(patient_conditions, patient_medications, trial_excluded_conditions))

    def test_excluded_due_to_condition(self):
        patient_conditions = "Diabetes"
        patient_medications = "Insulin"
        trial_excluded_conditions = "Diabetes, Cancer"

        #Ensuring the patient should be excluded due to matching condition
        self.assertFalse(check_exclusion_criteria_spacy(patient_conditions, patient_medications, trial_excluded_conditions))

if __name__ == '__main__':
    unittest.main()