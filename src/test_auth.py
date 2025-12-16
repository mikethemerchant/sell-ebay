try:
	# Prefer package imports when run from repo root
	from src.auth import get_access_token
	from src.ebay_api import get_seller_account
except ModuleNotFoundError:
	# Fallback for running from inside src directory
	from auth import get_access_token
	from ebay_api import get_seller_account

token = get_access_token()
print("ACCESS TOKEN OK")

account = get_seller_account(token)
print("EBAY API ACCESS OK")
print(account)
