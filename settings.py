from pydantic import BaseSettings


class Settings(BaseSettings):

    MONGO_URI: str = "mongodb://localhost:27017/"
    APP_DB: str = "ultraapp"

    JWT_SECRET: str = "S3CR3T"  # jwt secret
    JWT_LIFETIME: int = 3600 * 24


settings = Settings()
