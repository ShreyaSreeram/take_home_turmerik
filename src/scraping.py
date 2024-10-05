import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_clinical_trials(query, max_trials=100):
    base_url = f"https://clinicaltrials.gov/ct2/results?cond={query}&recrs=a&displayxml=true"
    response = requests.get(base_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'xml')
        trials = soup.find_all('clinical_study')[:max_trials]  # Limit number of trials

        # Extract relevant data
        trials_data = []
        for trial in trials:
            trial_id = trial.find('nct_id').text if trial.find('nct_id') else "No ID"
            title = trial.find('official_title').text if trial.find('official_title') else "No title"
            conditions = [cond.text for cond in trial.find_all('condition')]
            age_min = trial.find('minimum_age').text if trial.find('minimum_age') else "No min age"
            age_max = trial.find('maximum_age').text if trial.find('maximum_age') else "No max age"
            recruitment_status = trial.find('overall_status').text if trial.find('overall_status') else "No status"

            # Placeholder for inclusion/exclusion criteria (can be scraped from trial page if needed)
            included_conditions = conditions  # Simplified assumption
            excluded_conditions = []  # This would be scraped
            excluded_medications = []  # This would also be scraped
            
            trials_data.append({
                'trial_id': trial_id,
                'trial_name': title,
                'included_conditions': included_conditions,
                'excluded_conditions': excluded_conditions,
                'excluded_medications': excluded_medications,
                'age_min': age_min,
                'age_max': age_max,
                'recruitment_status': recruitment_status
            })
        
        return pd.DataFrame(trials_data)
    else:
        print("Failed to fetch data:", response.status_code)
        return pd.DataFrame()

# Example: Scrape recruiting trials for "diabetes"
trials_df = scrape_clinical_trials("diabetes", max_trials=50)