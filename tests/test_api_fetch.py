import unittest
from unittest.mock import patch
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from api_fetch import fetch_relevant_trials

class TestApiFetch(unittest.TestCase):
    @patch('api_fetch.requests.get')
    def test_fetch_relevant_trials(self, mock_get):
        #Mocking the API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "studies": [
                {"protocolSection": {"identificationModule": {"nctId": "NCT001"}, "eligibilityModule": {"minimumAge": "18", "maximumAge": "65"}}},
                {"protocolSection": {"identificationModule": {"nctId": "NCT002"}, "eligibilityModule": {"minimumAge": "25", "maximumAge": "70"}}}
            ]
        }

        trials = fetch_relevant_trials(limit=2)
        self.assertEqual(len(trials), 2)
        self.assertEqual(trials[0]['trial_id'], 'NCT001')
        self.assertEqual(trials[1]['trial_id'], 'NCT002')

if __name__ == '__main__':
    unittest.main()