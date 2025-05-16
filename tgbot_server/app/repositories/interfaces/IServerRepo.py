from abc import ABC, abstractmethod

from app.schema.server_schema import ServerSchema, ServerInfo


class IServerRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[ServerSchema]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> ServerSchema | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_short_info(self) -> list[ServerInfo]:
        raise NotImplementedError
