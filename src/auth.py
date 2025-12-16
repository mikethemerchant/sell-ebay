import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

def get_access_token():
    client_id = os.getenv("EBAY_CLIENT_ID")
    client_secret = os.getenv("EBAY_CLIENT_SECRET")
    refresh_token = os.getenv("EBAY_REFRESH_TOKEN")

    if not client_id or not client_secret or not refresh_token:
        raise ValueError(
            "Missing eBay OAuth credentials. Set EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, and EBAY_REFRESH_TOKEN."
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
        "scope": "https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account"
    }

    skip_ssl_verify = os.getenv("EBAY_SKIP_SSL_VERIFY", "false").lower() in {"1", "true", "yes"}

    response = requests.post(
        "https://api.ebay.com/identity/v1/oauth2/token",
        headers=headers,
        data=data,
        verify=not skip_ssl_verify
    )

    response.raise_for_status()
    return response.json()["access_token"]
