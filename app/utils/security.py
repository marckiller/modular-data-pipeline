import secrets

def generate_api_key(length: int = 16) -> str:
    return secrets.token_hex(length)