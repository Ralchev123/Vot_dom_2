import jwt
import requests
from fastapi import HTTPException
from .config import Settings

settings = Settings()

def get_keycloak_public_key():
    try:
        url = f"{settings.keycloak_url}/realms/{settings.keycloak_realm}"
        response = requests.get(url)
        response.raise_for_status()
        public_key = response.json()['public_key']
        return f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not fetch public key: {str(e)}")

def verify_token(token: str):
    try:
        public_key = get_keycloak_public_key()
        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=settings.keycloak_client_id
        )
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token verification failed: {str(e)}")

def get_token(username: str, password: str):
    try:
        token_url = f"{settings.keycloak_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/token"
        payload = {
            'client_id': settings.keycloak_client_id,
            'client_secret': settings.keycloak_client_secret,
            'grant_type': 'password',
            'username': username,
            'password': password
        }
        response = requests.post(token_url, data=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")