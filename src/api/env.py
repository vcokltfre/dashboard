from os import getenv

from dotenv import load_dotenv


load_dotenv()


class Site:
    name: str = getenv("SITE_NAME", "Dashboard")
