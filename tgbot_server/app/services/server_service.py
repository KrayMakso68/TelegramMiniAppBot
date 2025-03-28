from app.repository.interfaces import IServerRepository
from app.schema.server_schema import ServerInfo


class ServerService:
    def __init__(self, server_repository: IServerRepository):
        self.repository = server_repository

    async def get_servers_short_info(self) -> list[ServerInfo]:
        return await self.repository.get_all_short_info()
