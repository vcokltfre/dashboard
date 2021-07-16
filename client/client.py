from aiohttp import ClientSession


class Dashclient:
    def __init__(self, url: str, token: str) -> None:
        self._url = url
        self._token = token
        self._session = None

    @property
    def session(self) -> ClientSession:
        if self._session is None or self._session.closed:
            self._session = ClientSession(headers={
                "Authroization": self._token
            })
        return self._session

    def url(self, path: str, **params) -> str:
        return self._url + path.format(**params)

    async def create_guild(self, guild: int, icon_url: str, name: str) -> None:
        await self.session.post(
            self.url("/api/guilds/{guild_id}", guild_id=guild),
            params={
                "icon_url": icon_url,
                "name": name,
            }
        )

    async def authorize_user(self, guild: int, user: int) -> None:
        await self.session.post(self.url(
            "/api/guilds/{guild_id}/access/{user_id}",
            guild_id=guild,
            user_id=user
        ))

    async def revoke_user(self, guild: int, user: int) -> None:
        await self.session.delete(self.url(
            "/api/guilds/{guild_id}/access/{user_id}",
            guild_id=guild,
            user_id=user
        ))
