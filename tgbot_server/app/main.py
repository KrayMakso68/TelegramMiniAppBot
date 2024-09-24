import uvicorn
from fastapi import FastAPI

from app.api.v1.routes import routers as v1_routers


app = FastAPI(
    title="Упрощенный аналог Jira/Asana"
)


for router in v1_routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)