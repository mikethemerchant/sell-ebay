import os
import requests
from dotenv import load_dotenv, find_dotenv

# Load .env from repo root regardless of current working directory
_env_path = find_dotenv(usecwd=True)
if _env_path:
    load_dotenv(_env_path)
else:
    load_dotenv()

def _get_base_url():
    env = os.getenv("EBAY_ENV", "SANDBOX").upper()
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

    skip_ssl_verify = os.getenv("EBAY_SKIP_SSL_VERIFY", "false").lower() in {"1", "true", "yes"}
    response = requests.get(url, headers=headers, verify=not skip_ssl_verify)
    response.raise_for_status()
    return response.json()


# Backwards-compatible name expected by test_auth.py
def get_seller_account(access_token: str) -> dict:
    return get_seller_privileges(access_token)
