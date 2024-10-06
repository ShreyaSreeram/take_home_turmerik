import pandas as pd

def load_patient_data():
    # Load the CSV files
    print("Loading and merging patient data...")
    patients = pd.read_csv('/Users/Shreya1/Downloads/csv/patients.csv')
    conditions = pd.read_csv('/Users/Shreya1/Downloads/csv/conditions.csv')
    medications = pd.read_csv('/Users/Shreya1/Downloads/csv/medications.csv')
    allergies = pd.read_csv('/Users/Shreya1/Downloads/csv/allergies.csv')
    immunizations = pd.read_csv('/Users/Shreya1/Downloads/csv/immunizations.csv')
    procedures = pd.read_csv('/Users/Shreya1/Downloads/csv/procedures.csv')

   # Rename 'Id' to 'PATIENT' in patients to match other tables
    patients.rename(columns={'Id': 'PATIENT'}, inplace=True)

    # Group by 'PATIENT' and aggregate descriptions into a single string per patient
    conditions_grouped = conditions.groupby('PATIENT')['DESCRIPTION'].apply(lambda x: ', '.join(x.dropna().unique())).reset_index()
    medications_grouped = medications.groupby('PATIENT')['DESCRIPTION'].apply(lambda x: ', '.join(x.dropna().unique())).reset_index()
    allergies_grouped = allergies.groupby('PATIENT')['DESCRIPTION'].apply(lambda x: ', '.join(x.dropna().unique())).reset_index()
    immunizations_grouped = immunizations.groupby('PATIENT')['DESCRIPTION'].apply(lambda x: ', '.join(x.dropna().unique())).reset_index()
    procedures_grouped = procedures.groupby('PATIENT')['DESCRIPTION'].apply(lambda x: ', '.join(x.dropna().unique())).reset_index()

    # Rename the description columns after aggregation
    conditions_grouped.rename(columns={'DESCRIPTION': 'CONDITION_DESCRIPTION'}, inplace=True)
    medications_grouped.rename(columns={'DESCRIPTION': 'MEDICATION_DESCRIPTION'}, inplace=True)
    allergies_grouped.rename(columns={'DESCRIPTION': 'ALLERGY_DESCRIPTION'}, inplace=True)
    immunizations_grouped.rename(columns={'DESCRIPTION': 'IMMUNIZATION_DESCRIPTION'}, inplace=True)
    procedures_grouped.rename(columns={'DESCRIPTION': 'PROCEDURE_DESCRIPTION'}, inplace=True)

    # Merge the grouped tables back with the patients table
    merged_data = patients.copy()
    merged_data = merged_data.merge(conditions_grouped, on='PATIENT', how='left')
    merged_data = merged_data.merge(medications_grouped, on='PATIENT', how='left')
    merged_data = merged_data.merge(allergies_grouped, on='PATIENT', how='left')
    merged_data = merged_data.merge(immunizations_grouped, on='PATIENT', how='left')
    merged_data = merged_data.merge(procedures_grouped, on='PATIENT', how='left')

    return merged_data

# Run the function to load, consolidate, and merge the data
merged_patient_data = load_patient_data()

merged_patient_data.to_csv('merged_patient_data.csv', index=False)