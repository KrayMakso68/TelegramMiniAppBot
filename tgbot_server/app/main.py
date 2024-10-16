import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.routes import routers as v1_routers
from app.core.config import settings

ORIGINS = [
    "*",
]


class AppCreator:
    def __init__(self):
        self.app = FastAPI(
            title=settings.PROJECT_NAME,
            version=settings.APP_VERSION,
        )

        # routers
        self.app.include_router(v1_routers, prefix=settings.API_V1_STR)

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


app_creator = AppCreator()
app = app_creator.app

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
