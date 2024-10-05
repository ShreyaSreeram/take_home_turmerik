import requests
import pandas as pd

def fetch_clinical_trials_v2(query, fields, page=1, size=10):
    """
    Fetch clinical trials using the new ClinicalTrials.gov API (version 2.0).
    
    Parameters:
    - query: Search term (e.g., "diabetes")
    - fields: List of fields to return (e.g., ["NCTId", "EligibilityCriteria", "Conditions"])
    - page: Page number for pagination (default is 1)
    - size: Number of studies per page (default is 10)
    
    Returns:
    - A pandas DataFrame with the requested trial data.
    """
    
    # Base URL for querying studies
    base_url = "https://clinicaltrials.gov/api/v2/studies"
    
    # Define the parameters for the API request
    params = {
        'query.term': query,       # The search term (e.g., "diabetes")
        'fields': ','.join(fields), # Join the list of fields into a comma-separated string
        'page': page,               # Page number for pagination
        'size': size,               # Number of results per page
        'format': 'json'            # Return results in JSON format
    }
    
    # Send the HTTP GET request to the API
    response = requests.get(base_url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response into a pandas DataFrame
        trials_data = response.json()['data']
        trials_df = pd.json_normalize(trials_data)
        return trials_df
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return pd.DataFrame()

def check_patient_eligibility(patient, trial):
    """
    Check if a patient is eligible for a specific clinical trial based on conditions and age.
    
    Parameters:
    - patient: A dictionary containing the patient's age, conditions, and medications.
    - trial: A dictionary or DataFrame row containing the trial's conditions and eligibility criteria.
    
    Returns:
    - True if the patient is eligible, False otherwise.
    """
    patient_age = patient['age']
    patient_conditions = set(patient['conditions'])
    patient_medications = set(patient['medications'])
    
    # Extract the trial's age range and conditions
    trial_min_age = int(trial['MinimumAge'].split()[0]) if pd.notna(trial['MinimumAge']) else None
    trial_max_age = int(trial['MaximumAge'].split()[0]) if pd.notna(trial['MaximumAge']) else None
    trial_conditions = set(trial['Conditions']) if pd.notna(trial['Conditions']) else set()
    
    # Check age eligibility
    age_eligible = (trial_min_age is None or patient_age >= trial_min_age) and \
                   (trial_max_age is None or patient_age <= trial_max_age)
    
    # Check conditions eligibility (assuming patients must have one of the conditions listed)
    condition_eligible = bool(patient_conditions & trial_conditions)
    
    # Optionally, check exclusion based on medications in trial's eligibility criteria (if available)
    exclusion_criteria = trial.get('EligibilityCriteria', "").lower()
    medication_eligible = not any(med in exclusion_criteria for med in patient_medications)
    
    return age_eligible and condition_eligible and medication_eligible

def match_patients_to_trials(patients, trials_df):
    """
    Match a list of patients to eligible clinical trials.
    
    Parameters:
    - patients: A list of patient dictionaries with attributes 'age', 'conditions', and 'medications'.
    - trials_df: A pandas DataFrame containing clinical trial data.
    
    Returns:
    - A list of results for each patient, showing eligible trials.
    """
    results = []
    for patient in patients:
        eligible_trials = []
        for _, trial in trials_df.iterrows():
            if check_patient_eligibility(patient, trial):
                eligible_trials.append({
                    "trialId": trial['NCTId'],
                    "trialName": trial.get('OfficialTitle', 'No Title'),
                    "eligibilityCriteriaMet": trial['EligibilityCriteria']
                })
        
        results.append({
            "patientId": patient['id'],
            "eligibleTrials": eligible_trials
        })
    
    return results

# Example patient data
patients = [
    {"id": "patient_001", "age": 45, "conditions": ["Diabetes"], "medications": ["Metformin"]},
    {"id": "patient_002", "age": 60, "conditions": ["Hypertension"], "medications": ["Aspirin"]},
]

# Fetch trials for the condition "diabetes"
fields_to_fetch = ["NCTId", "EligibilityCriteria", "Conditions", "MinimumAge", "MaximumAge", "OfficialTitle"]
trials_df = fetch_clinical_trials_v2("diabetes", fields_to_fetch, page=1, size=10)

# Match patients to trials
matches = match_patients_to_trials(patients, trials_df)

# Output the matching results
for match in matches:
    print(f"Patient {match['patientId']} is eligible for the following trials:")
    for trial in match['eligibleTrials']:
        print(f"  Trial ID: {trial['trialId']}, Trial Name: {trial['trialName']}")
        print(f"  Eligibility Criteria Met: {trial['eligibilityCriteriaMet']}\n")

#If we wanted to scale the data and use paginated API calls: 
def fetch_all_trials(query, fields, batch_size=100, max_pages=5):
    """
    Fetch all trials related to a query in batches using pagination.
    
    Parameters:
    - query: Search term (e.g., "diabetes")
    - fields: List of fields to return (e.g., ["NCTId", "EligibilityCriteria", "Conditions"])
    - batch_size: Number of studies per page
    - max_pages: Maximum number of pages to retrieve (for scaling)
    
    Returns:
    - A pandas DataFrame containing all trials fetched in batches.
    """
    all_trials = pd.DataFrame()  # To store all fetched trial data
    
    for page in range(1, max_pages + 1):
        # Fetch the trials for the current page
        trials_df = fetch_clinical_trials_v2(query, fields, page=page, size=batch_size)
        
        # If no data is returned, break the loop (we've fetched all available data)
        if trials_df.empty:
            break
        
        # Append the current batch of trials to the cumulative DataFrame
        all_trials = pd.concat([all_trials, trials_df], ignore_index=True)
    
    return all_trials

# Example usage:
fields_to_fetch = ["NCTId", "EligibilityCriteria", "Conditions", "MinimumAge", "MaximumAge", "OfficialTitle"]
all_trials_df = fetch_all_trials("diabetes", fields_to_fetch, batch_size=100, max_pages=5)

# Process the trials as needed (e.g., match to patients)
print(f"Fetched {len(all_trials_df)} trials")