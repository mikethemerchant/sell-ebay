import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

def get_access_token():
    client_id = os.getenv("EBAY_CLIENT_ID")
    client_secret = os.getenv("EBAY_CLIENT_SECRET")
    refresh_token = os.getenv("EBAY_REFRESH_TOKEN")
    env = os.getenv("EBAY_ENV", "PROD").upper()

    if not all([client_id, client_secret, refresh_token]):
        raise RuntimeError("Missing eBay OAuth environment variables")

    token_url = (
        "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
        if env == "SANDBOX"
        else "https://api.ebay.com/identity/v1/oauth2/token"
    )

    auth = f"{client_id}:{client_secret}"
    encoded = base64.b64encode(auth.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": (
            "https://api.ebay.com/oauth/api_scope "
            "https://api.ebay.com/oauth/api_scope/sell.inventory "
            "https://api.ebay.com/oauth/api_scope/sell.account"
        )
    }

    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()

    return response.json()["access_token"]
