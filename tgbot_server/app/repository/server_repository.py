from sqlalchemy import select, Result
from sqlalchemy.exc import DatabaseError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import DBError
from app.model import Server
from app.repository.interfaces import IServerRepository
from app.schema.server_schema import ServerSchema


class ServerRepository(IServerRepository):
    def __init__(self, async_session: AsyncSession):
        self.session = async_session

    async def get_all(self) -> list[ServerSchema]:
        try:
            stmt = select(Server)
            result: Result = await self.session.execute(stmt)
            servers = result.scalars().all()
            return [ServerSchema.model_validate(server) for server in servers]
        except NoResultFound:
            return []

    async def get_by_id(self, id: int) -> ServerSchema | None:
        try:
            result: Server | None = await self.session.get(Server, id)
            return ServerSchema.model_validate(result)
        except NoResultFound:
            return None
        except DatabaseError:
            raise DBError(detail="Database error occurred.")
