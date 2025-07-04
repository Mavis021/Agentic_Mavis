import os 
import requests
from dotenv import load_dotenv

load_dotenv()

def get_linkedin_profile(linkedin_url: str, mock: bool = False):

    """
    Fetches the LinkedIn profile data from the given URL.
    
    Args:
        linkedin_url (str): The LinkedIn profile URL.
        
    Returns:
        dict: The JSON response containing the profile data.
    """
    if mock:
        linkedin_url = "https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/5eaf8e46dc29a98612c8fe0c774123a7a2ac4575/eden-marco-scrapin.json"
        response = requests.get(linkedin_url, timeout=10)
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "linkedInUrl": linkedin_url,
            "apikey": os.getenv("SCRAPIN_API_KEY")
        }
        response = requests.get(
            api_endpoint, 
            params=params,
            timeout=10
        )

    data = response.json().get("person")
    data= {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["certifications"]
    }
    return data

if __name__ == "__main__":
    linkedin_url = "https://api.linkedin.com/in/mamatamaharjan"
    try:
        profile_data = get_linkedin_profile(linkedin_url, mock=False)
        print(profile_data)
    except Exception as e:
        print(f"Error fetching LinkedIn profile: {e}")