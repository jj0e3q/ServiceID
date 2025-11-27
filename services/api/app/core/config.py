from shared.core.config import BaseAppSettings


class Settings(BaseAppSettings):
    SERVICE_NAME: str = "gateway-api"


settings = Settings()