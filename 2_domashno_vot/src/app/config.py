from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    keycloak_url: str
    keycloak_realm: str
    keycloak_client_id: str
    keycloak_client_secret: str
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str

    class Config:
        env_file = ".env"