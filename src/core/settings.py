from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database URL for connecting to the database
    DATABASE_URL: str = ""

    # Access token expiry time
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    #  secret key
    SECRET_KEY: str = ""

    # algorithm
    ALGORITHM: str = "HS256"

    # Refresh Token
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        # Specify the .env file to load environment variables from
        env_file = ".env"
        #  Specify the encoding of the .env file
        env_file_encoding = "utf-8"


#  Create an instance of the Settings class to access configuration values
settings = Settings()
