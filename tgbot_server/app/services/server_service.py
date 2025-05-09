from app.core.exceptions import NotFoundError
from app.repository.interfaces import IServerRepository
from app.schema.server_schema import ServerInfo


class ServerService:
    def __init__(self, server_repository: IServerRepository):
        self.repository = server_repository

    async def get_active_servers_short_info(self) -> list[ServerInfo]:
        all_servers_info = await self.repository.get_all_short_info()
        return [server_info for server_info in all_servers_info if server_info.is_active]

    async def get_server_short_info_by_id(self, server_id: int) -> ServerInfo:
        server = await self.repository.get_by_id(server_id)
        if server is None:
            raise NotFoundError(detail="Server not found.")
        return ServerInfo.model_validate(server)
