import uvicorn
from fastapi import FastAPI

from app.api.v1.routes import routers as v1_routers
from app.core.config import settings


class AppCreator:
    def __init__(self):
        self.app = FastAPI(
            title=settings.PROJECT_NAME,
            version=settings.APP_VERSION
        )

        # routers
        self.app.include_router(v1_routers, prefix=settings.API_V1_STR)


app_creator = AppCreator()
app = app_creator.app

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
