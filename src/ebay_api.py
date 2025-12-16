import requests


def get_seller_account(access_token: str):
	"""Fetch a simple account resource to verify API access.

	Uses the Sell Account `privilege` endpoint which requires an OAuth token
	and returns details about the seller's privileges. This is lightweight
	and suitable for a connectivity check.
	"""
	headers = {
		"Authorization": f"Bearer {access_token}",
		"Content-Type": "application/json",
		"Accept": "application/json",
	}

	url = "https://api.ebay.com/sell/account/v1/privilege"
	resp = requests.get(url, headers=headers, timeout=30)
	resp.raise_for_status()
	return resp.json()

