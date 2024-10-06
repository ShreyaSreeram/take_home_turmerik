import pandas as pd
import json
from load_data import load_patient_data
from criteria_check import check_inclusion_criteria, check_exclusion_criteria_spacy 
from api_fetch import fetch_relevant_trials

def main():
    #Load and consolidate patient data
    print("Loading and consolidating patient data...")
    patient_data = load_patient_data()

    #Fetch relevant clinical trials (limit to 10 for testing)
    print("Fetching clinical trials data...")
    trials_data = fetch_relevant_trials(limit=10)

    results = []

    #Process each patient and compare with clinical trials
    print("Checking eligibility...")
    for index, patient in patient_data.iterrows():
        patient_id = patient['PATIENT']
        patient_birthdate = patient['BIRTHDATE']
        patient_conditions = patient.get('CONDITION_DESCRIPTION', '')
        patient_medications = patient.get('MEDICATION_DESCRIPTION', '')

  
        eligible_trials = []

        for trial in trials_data:
           
            is_included = check_inclusion_criteria(patient_birthdate, trial['min_age'], trial['max_age'])
            if not is_included:
                continue

         
            is_excluded = not check_exclusion_criteria_spacy(
                patient_conditions, 
                patient_medications, 
                trial['exclusion_criteria']
            )
            if is_excluded:
                continue

            eligible_trials.append(trial['trial_id'])

        #Store the patient ID and their list of eligible trials
        if eligible_trials:
            results.append({
                'patient_id': patient_id,
                'eligible_trials': eligible_trials  
            })

    
    results_df = pd.DataFrame(results)

    #Saving the results as CSV
    results_df.to_csv('eligible_patients_and_trials.csv', index=False)
    print(f"Eligible patients saved to eligible_patients_and_trials.csv.")

    #Saving the results as JSON
    with open('eligible_patients_and_trials.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)
    print(f"Eligible patients saved to eligible_patients_and_trials.json.")

if __name__ == "__main__":
    main()