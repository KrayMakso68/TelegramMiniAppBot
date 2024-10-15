import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

        # CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


app_creator = AppCreator()
app = app_creator.app

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)

# allow_methods=["GET", "POST", "OPTIONS", "PATCH", "DELETE", "PUT"],
#             allow_headers=["Content-Type",
#                            "Authorization",
#                            "Set-Cookie",
#                            "Access-Control-Allow-Headers",
#                            "Access-Control-Allow-Origin"
#                            ],