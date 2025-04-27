from app.core.exceptions import NotFoundError
from app.repository.interfaces import IServerRepository
from app.schema.server_schema import ServerInfo


class ServerService:
    def __init__(self, server_repository: IServerRepository):
        self.repository = server_repository

    async def get_servers_short_info(self) -> list[ServerInfo]:
        return await self.repository.get_all_short_info()

    async def get_server_short_info_by_id(self, server_id: int) -> ServerInfo:
        server = await self.repository.get_by_id(server_id)
        if server is None:
            raise NotFoundError(detail="Server not found.")
        return ServerInfo.model_validate(server)
