from os import getenv

from dotenv import load_dotenv


load_dotenv()


class Site:
    name: str = getenv("SITE_NAME", "Dashboard")
    icon: str = getenv("SITE_ICON", "https://avatars.githubusercontent.com/u/16879430?v=4")
    repo: str = getenv("SITE_REPO", "https://github.com/vcokltfre/dashboard")
