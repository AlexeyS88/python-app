from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    database_url: str
    redis_url: str
    cache_ttl_seconds: int
    cache_task_key: str
    cors_allowed_origin: list[str]

def get_settings() -> Settings:
    pg_user = os.environ["POSTGRES_USER"]
    pg_pass = os.environ["POSTGRES_PASSWORD"]
    pg_host = os.getenv("POSTGRES_HOST", "localhost")

    redis_pass = os.environ["REDIS_PASSWORD"]
    redis_host = os.getenv("REDIS_HOST", "localhost")

    app_port = os.getenv("APP_PUBLIC_PORT",  "8080")

    return Settings(
        database_url=f"postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:5432/postgres",
        redis_url=f"redis://default:{redis_pass}@{redis_host}:6379/0",
        cache_ttl_seconds=3600,
        cache_task_key="cache:tasks_list",
        cors_allowed_origin=[f"http://localhost:{app_port}"]
    )

settings = get_settings()