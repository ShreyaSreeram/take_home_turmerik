from datetime import datetime
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")

def check_inclusion_criteria(patient_birthdate, trial_min_age, trial_max_age):
    """
    Checks if a patient's age falls within the inclusion age range for a clinical trial.

    Args:
        patient_birthdate (str or pd.Timestamp): The birthdate of the patient, can be a string or pandas timestamp.
        trial_min_age (str): The minimum age for the trial in years (e.g., '18 Years'). Defaults to 0 if not provided or invalid.
        trial_max_age (str): The maximum age for the trial in years (e.g., '65 Years'). Defaults to 120 if not provided or invalid.

    Returns:
        bool: True if the patient's age is within the trial's age range, False otherwise.
    """
    try:
        trial_min_age = int(trial_min_age.split()[0]) if trial_min_age else 0  # Default min age to 0
    except (ValueError, AttributeError):
        trial_min_age = 0  # If conversion fails, assume no lower age limit
    
    try:
        trial_max_age = int(trial_max_age.split()[0]) if trial_max_age else 120  # Default max age to 120
    except (ValueError, AttributeError):
        trial_max_age = 120  # If conversion fails, assume no upper age limit

    # Calculate the patient's age
    if pd.isna(patient_birthdate):
        return False
    birthdate = pd.to_datetime(patient_birthdate)
    age = (datetime.now() - birthdate).days // 365  # Convert days to years

    # Check if the age is within the trial's age range
    if trial_min_age <= age <= trial_max_age:
        return True
    return False


def extract_entities(text):
    """Extract medical conditions or medications using SpaCy's NER."""
    # Convert the input to a string and handle missing data
    if pd.isna(text):
        return []
    
    # Process the text with SpaCy
    doc = nlp(str(text))  # Ensure that text is passed as a string

    # Extract entities related to medical conditions and medications
    entities = [ent.text for ent in doc.ents if ent.label_ in ["DISEASE", "DRUG"]]
    return entities

def check_exclusion_criteria_spacy(patient_conditions, patient_medications, trial_excluded_conditions_text):
    """
    Checks if a patient is excluded from a trial based on their conditions or medications compared to the trial's exclusion criteria.

    Args:
        patient_conditions (str): A text description of the patient's medical conditions.
        patient_medications (str): A text description of the medications the patient is taking.
        trial_excluded_conditions_text (str): The text containing the trial's exclusion criteria related to conditions or medications.

    Returns:
        bool: False if the patient's conditions or medications match any of the trial's exclusion criteria, True if no matches are found.

   
    """
    patient_conditions_entities = extract_entities(patient_conditions)
    patient_medications_entities = extract_entities(patient_medications)
    trial_excluded_conditions_entities = extract_entities(trial_excluded_conditions_text)

    # Check if any of the patient's conditions or medications match the exclusion criteria
    for condition in patient_conditions_entities:
        if condition.lower() in trial_excluded_conditions_entities:
            return False  # Exclude patient
    for medication in patient_medications_entities:
        if medication.lower() in trial_excluded_conditions_entities:
            return False  # Exclude patient

    return True  # Patient is not excluded