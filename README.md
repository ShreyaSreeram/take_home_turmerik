Clinical Trial Eligibility Matching

This project checks patient eligibility for clinical trials based on their medical conditions, medications, and age. It fetches clinical trials that are actively recruiting, applies inclusion and exclusion criteria, and outputs the list of eligible patients for specific trials.

Project Structure: 

/project
    /src
        main.py                # Main entry point to execute the workflow
        load_data.py            # Module for loading and consolidating patient data
        criteria_check.py       # Functions to check inclusion and exclusion criteria
        api_fetch.py            # Fetches clinical trial data from the API
        criteria_check.py          # Uses SpaCy for natural language processing to check exclusions
    /tests
        test_criteria_check.py  # Unit tests for inclusion and exclusion criteria checks
        test_load_data.py       # Unit test for data loading functionality
        test_api_fetch.py       # Unit test for API fetching functionality (mocked)
        test_integration.py     # Integration test for the entire project
    eligible_patients_and_trials.csv  # Output CSV file containing eligible patients and trials
    eligible_patients_and_trials.json # Output JSON file containing eligible patients and trials

Features

	•	Fetches clinical trials data from ClinicalTrials.gov API.
	•	Applies inclusion criteria based on patient age.
	•	Applies exclusion criteria based on patient conditions and medications using SpaCy.
	•	Outputs eligible patients and the trials they are eligible for in both CSV and JSON formats.
	•	Includes unit tests for each component and integration tests for the full workflow.

Setup Instructions

1. Clone the Repository

First, clone this repository to your local machine:

```python
git clone https://github.com/your-repo/clinical-trial-matching.git
cd clinical-trial-matching
