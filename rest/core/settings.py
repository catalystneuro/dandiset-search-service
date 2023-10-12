from pydantic import BaseSettings
import os


def safe_int(value, default: int=0):
    try:
        return int(value)
    except Exception as e:
        return int(default)


class Settings(BaseSettings):
    # General app config
    VERSION: str = "0.1.0"
    APP_TITLE: str = "Dandiset Search"

    QDRANT_HOST: str = os.environ.get('QDRANT_HOST', "http://qdrant")
    QDRANT_PORT: int = safe_int(os.environ.get('QDRANT_PORT'), 6333)
    QDRANT_COLLECTION_NAME: str = os.environ.get('QDRANT_COLLECTION_NAME', "dandi_collection")
    QDRANT_VECTOR_SIZE: int = safe_int(os.environ.get('QDRANT_VECTOR_SIZE'), 1536)
    QDRANT_API_KEY: str = os.environ.get('QDRANT_API_KEY', None)

    OPENAI_API_KEY: str = os.environ.get('OPENAI_API_KEY', None)

    DANDI_API_KEY: str = os.environ.get('DANDI_API_KEY', None)


class DevSettings(Settings):
    SERVER_HOST: str = "0.0.0.0"
    DEBUG: bool = True
    PORT: int = 8050
    RELOAD: bool = True
    CORS: dict = {
        "origins": [
            "*",
        ],
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }
    REDIRECT_HTTPS: bool = False
    API_BASE_URL: str = os.environ.get('API_BASE_URL', "http://localhost:8000")


class DockerDevSettings(DevSettings):
    API_BASE_URL: str = 'http://rest-api:80'


class ProdSettings(Settings):
    SERVER_HOST: str = "0.0.0.0"
    DEBUG: bool = False
    PORT: int = 8050
    RELOAD: bool = False
    API_BASE_URL: str = os.environ.get('API_BASE_URL', "http://localhost:8000")



def get_settings():
    env = os.getenv("DEPLOY_ENV", "dev")
    settings_type = {
        "dev": DevSettings(),
        "docker-dev": DockerDevSettings(),
        "prod": ProdSettings(),
    }
    return settings_type[env]


settings: Settings = get_settings()