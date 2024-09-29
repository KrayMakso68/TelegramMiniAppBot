from typing import Any, Protocol


class RepositoryProtocol(Protocol):
    async def create(self) -> int: ...

    # async def read(self) -> Any: ...


class BaseService:
    def __init__(self, repository: RepositoryProtocol) -> None:
        self._repository = repository

    async def add(self) -> Any:
        return self._repository.create()
