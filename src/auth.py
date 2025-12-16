import os
import base64
import requests
from dotenv import load_dotenv, find_dotenv

# Load .env from repo root regardless of current working directory
_env_path = find_dotenv(usecwd=True)
if _env_path:
    load_dotenv(_env_path)
else:
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

    skip_ssl_verify = os.getenv("EBAY_SKIP_SSL_VERIFY", "false").lower() in {"1", "true", "yes"}

    response = requests.post(
        token_url,
        headers=headers,
        data=data,
        verify=not skip_ssl_verify
    )

    if not response.ok:
        # Include body to help diagnose invalid_client/invalid_grant
        raise requests.HTTPError(
            f"Token request failed ({response.status_code}): {response.text}",
            response=response,
        )

    return response.json()["access_token"]
