import requests
import time

def fetch_relevant_trials(limit=100):
    """
    Fetches a list of actively recruiting clinical trials from ClinicalTrials.gov using their API.

    The function retrieves trial data in pages, extracts relevant trial information such as trial ID, 
    age criteria, inclusion and exclusion criteria, and sex eligibility. The data collection stops once 
    the specified limit of trials is reached, or there are no more trials available.

    Args:
        limit (int): The maximum number of trials to fetch. Default is 100.

    Returns:
        list: A list of dictionaries, where each dictionary contains relevant information for a clinical trial, 
        including trial ID, age range, sex eligibility, inclusion criteria, and exclusion criteria.
    """
    
    base_url = "https://clinicaltrials.gov/api/v2/studies"
    fetched_trials = 0
    trials_data = []
    next_page_token = None

    while fetched_trials < limit:
        params = {
            "filter.overallStatus": "RECRUITING",
            "pageSize": 50,
            "pageToken": next_page_token
        }

        # Send GET request to fetch trial data
        response = requests.get(base_url, params=params)
        response.raise_for_status()  
        data = response.json()

        for trial in data.get('studies', []):
            protocol = trial.get('protocolSection', {})
            identification = protocol.get('identificationModule', {})
            eligibility = protocol.get('eligibilityModule', {})

            #Extract inclusion and exclusion criteria
            eligibility_criteria = eligibility.get('eligibilityCriteria', '')
            inclusion_criteria = ''
            exclusion_criteria = ''

            if eligibility_criteria:
               
                if "Inclusion Criteria:" in eligibility_criteria:
                    inclusion_part = eligibility_criteria.split("Inclusion Criteria:")[1]
                    inclusion_criteria = inclusion_part.split("Exclusion Criteria:")[0].strip()

                if "Exclusion Criteria:" in eligibility_criteria:
                    exclusion_part = eligibility_criteria.split("Exclusion Criteria:")[1]
                    exclusion_criteria = exclusion_part.strip()

   
            trial_info = {
                "trial_id": identification.get('nctId', 'Unknown'),
                "min_age": eligibility.get('minimumAge', 'N/A'),
                "max_age": eligibility.get('maximumAge', 'N/A'),
                "inclusion_criteria": inclusion_criteria,  
                "exclusion_criteria": exclusion_criteria,  
                "sex": eligibility.get('sex', 'N/A')
            }

    
            trials_data.append(trial_info)
            fetched_trials += 1

            if fetched_trials >= limit:
                break


        next_page_token = data.get('nextPageToken')
        if not next_page_token:
            break

        time.sleep(1) 

    return trials_data

#Fetch and print trial data for testing
trials_data = fetch_relevant_trials(limit=10)