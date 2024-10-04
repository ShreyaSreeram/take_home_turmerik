import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

##Data preparation: 
# Load patients CSV
patients_file_path = '/Users/Shreya1/Downloads/csv/patients.csv'  
patients_df = pd.read_csv(patients_file_path)

# Step 1: Extract relevant columns for patient demographics
def extract_patient_demographics(patients_df):
    # Keep only the columns needed: Id, BIRTHDATE, GENDER
    demographics_df = patients_df[['Id', 'BIRTHDATE', 'GENDER']].copy()
    
    # Step 2: Calculate the age of the patient using the current date
    # Convert BIRTHDATE to datetime
    demographics_df['BIRTHDATE'] = pd.to_datetime(demographics_df['BIRTHDATE'])
    
    # Calculate age by subtracting the birth year from the current year
    demographics_df['AGE'] = demographics_df['BIRTHDATE'].apply(lambda x: datetime.now().year - x.year)
    
    return demographics_df

# Extract patient demographics
patient_demographics = extract_patient_demographics(patients_df)

# Display the resulting DataFrame
print(patient_demographics.head())

# Step 3: Save the demographics data if needed
#patient_demographics.to_csv('patient_demographics.csv', index=False)


#Next step: link patients with conditions and medications
conditions_file_path = '/path/to/conditions.csv'  
medications_file_path = '/path/to/medications.csv' 
conditions_df = pd.read_csv(conditions_file_path)
medications_df = pd.read_csv(medications_file_path)
