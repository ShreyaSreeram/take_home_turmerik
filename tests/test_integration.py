import unittest
import pandas as pd
import json
from unittest.mock import patch
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import main
class TestIntegration(unittest.TestCase):
    @patch('api_fetch.requests.get')
    def test_integration_workflow(self, mock_get):
        # Mock the API response for clinical trials
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "studies": [
                {"protocolSection": {"identificationModule": {"nctId": "NCT001"}, "eligibilityModule": {"minimumAge": "18", "maximumAge": "65"}, "eligibilityModule": {"exclusionCriteria": "Diabetes"}}},
                {"protocolSection": {"identificationModule": {"nctId": "NCT002"}, "eligibilityModule": {"minimumAge": "25", "maximumAge": "70"}, "eligibilityModule": {"exclusionCriteria": "HIV"}}}
            ]
        }

        # Simulate a run of the entire workflow
        main()

        # Check if the CSV and JSON files are generated
        csv_file = 'eligible_patients_and_trials.csv'
        json_file = 'eligible_patients_and_trials.json'

        # Check CSV output
        df = pd.read_csv(csv_file)
        self.assertGreater(len(df), 0)  # Ensure data exists in CSV

        # Check JSON output
        with open(json_file, 'r') as f:
            data = json.load(f)
            self.assertGreater(len(data), 0)  # Ensure data exists in JSON

if __name__ == '__main__':
    unittest.main()