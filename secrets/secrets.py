# secrets.py
# This file exposes different types of secrets for testing purposes only.
# Do NOT use real secrets in production code.

# Hardcoded API key
API_KEY = "12345-ABCDEYDKDL-SECRET-API-KEY"


github_token = "ghp_1234567890abcdef1234567890abcdef12345678"  # Example GitHub token
# Hardcoded password
DB_PASSWORD = "SuperSecretPassword123!"

# Hardcoded token
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.SECRET_PAYLOAD.SIGNATURE"


# Hardcoded private key (example, not real)
PRIVATE_KEY = """
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA7v8wF+SECRETKEYEXAMPLE+QIDAQABAoIBAQC0
-----END RSA PRIVATE KEY-----
"""

# Hardcoded secret in a dictionary
secrets_dict = {
    "client_id": "my-client-id",
    "client_secret": "my-client-secret-SECRET"
}

def get_api_key():
    return API_KEY

def get_db_password():
    return DB_PASSWORD

def get_access_token():
    return ACCESS_TOKEN

def get_private_key():
    return PRIVATE_KEY

def get_secrets_dict():
    return secrets_dict