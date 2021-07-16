from os import getenv
from secrets import token_hex

from dotenv import load_dotenv


load_dotenv()


class Site:
    name: str = getenv("SITE_NAME", "Dashboard")
    icon: str = getenv("SITE_ICON", "https://avatars.githubusercontent.com/u/16879430?v=4")
    repo: str = getenv("SITE_REPO", "https://github.com/vcokltfre/dashboard")
    link: str = getenv("SITE_BASE", "http://localhost:8000")


class Database:
    uri: str = getenv("DATABASE_URI", "postgres://root:password@localhost:5432/dashboard")


class Redis:
    uri: str = getenv("REDIS_URI", "redis://localhost:6379")


class Auth:
    admins: list = getenv("SITE_ADMINS", "").split(";")
    salt: str = getenv("SITE_SALT", token_hex(16))
    internal: str = getenv("INTERNAL_TOKEN")


class Discord:
    client_id: str = getenv("DISCORD_CLIENT_ID")
    client_secret: str = getenv("DISCORD_CLIENT_SECRET")
