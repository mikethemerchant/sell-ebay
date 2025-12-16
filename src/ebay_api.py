import os
import requests
from dotenv import load_dotenv

load_dotenv()

def _get_base_url():
    env = os.getenv("EBAY_ENV", "PROD").upper()
    return (
        "https://api.sandbox.ebay.com"
        if env == "SANDBOX"
        else "https://api.ebay.com"
    )

def get_seller_privileges(access_token: str) -> dict:
    """
    Read-only call to verify OAuth token works.
    Does NOT create or modify anything.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    url = f"{_get_base_url()}/sell/account/v1/privilege"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
