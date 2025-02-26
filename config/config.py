from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DB_PORT: int
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    PRODUCT_URL: str = "uploads/products/"
    SOCIAL_URL: str = "uploads/socials/"
    PROMOTION_URL: str = "uploads/promotions/"
    NEWS_URL: str = "uploads/news/"

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    KEY: str = "QWERTY123321"
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env_prod")

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()

print(settings)
