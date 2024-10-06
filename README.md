Clinical Trial Eligibility Matching

This project checks patient eligibility for clinical trials based on their medical conditions, medications, and age. It fetches clinical trials that are actively recruiting, applies inclusion and exclusion criteria, and outputs the list of eligible patients for specific trials.

Project Structure: 
/project
    /src
        main.py                # Main entry point to execute the workflow
        load_data.py           # Module for loading and consolidating patient data
        criteria_check.py      # Functions to check inclusion and exclusion criteria
        api_fetch.py           # Fetches clinical trial data from the API
        criteria_check.py      # Uses SpaCy for natural language processing to check exclusions
    /tests
        test_criteria_check.py # Unit tests for inclusion and exclusion criteria checks
        test_load_data.py      # Unit test for data loading functionality
        test_api_fetch.py      # Unit test for API fetching functionality (mocked)
        test_integration.py    # Integration test for the entire project
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
```

2. Create a Virtual Environment

Create a virtual environment to manage dependencies:

```python 
python -m venv venv
source venv/bin/activate
```  

3. Install Dependencies

Install the required Python libraries:

```python 
pip install -r requirements.txt
```

4. Download SpaCy Language Model

The project uses SpaCy for natural language processing. Download the small English model:

```python 
python -m spacy download en_core_web_sm
```

5. Set Up ClinicalTrials.gov API

No setup is required for this, but ensure your internet connection is active, as the project fetches data from the ClinicalTrials.gov API.

6. Run the Main Workflow

To execute the main workflow and check patient eligibility for trials, run:
```python 
python src/main.py
This will:

	•	Load patient data.
	•	Fetch clinical trials from the API.
	•	Apply inclusion/exclusion criteria.
	•	Generate two output files:
	•	eligible_patients_and_trials.csv
	•	eligible_patients_and_trials.json

7. Run Unit and Integration Tests

To ensure that all components are functioning correctly, you can run the unit tests and integration tests using:

```python
python -m unittest discover -s tests
```

Project Files

1. main.py

The main entry point of the project. It orchestrates the data loading, trial fetching, inclusion/exclusion checks, and output generation.

2. load_data.py

Handles loading and consolidating patient data from multiple CSV files into a Pandas DataFrame.

3. criteria_check.py

Contains the core functions for:

	•	Inclusion criteria check: Verifies if a patient’s age falls within the trial’s specified age range.
	•	Exclusion criteria check: Uses SpaCy to analyze whether a patient’s medical conditions or medications match the trial’s exclusion criteria.

4. api_fetch.py

Responsible for fetching clinical trials data from ClinicalTrials.gov using the API. This fetches only recruiting trials and limits the number of trials fetched based on the project’s requirements.

5. spacy_check.py

Uses SpaCy’s Named Entity Recognition (NER) to extract medical conditions and medications from text and compares them with the trial’s exclusion criteria.

6. tests/

Contains unit and integration tests for the project. Each module has associated tests to ensure correctness and proper functionality.

Output Files

	•	eligible_patients_and_trials.csv: CSV file containing the list of eligible patients and their eligible trials.
	•	eligible_patients_and_trials.json: JSON file with the same information as the CSV, but in JSON format.


Contributing

Feel free to submit pull requests or open issues if you find any bugs or have suggestions for new features.

This README covers the setup, running instructions, testing process, and a brief description of each major component in the project. Let me know if you need any modifications or additional details!
