from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.user import router as user_router
from app.api.v1.endpoints.subscription import router as subscribe_router
from app.api.v1.endpoints.panel import router as panel_router
from app.api.v1.endpoints.payment import router as payment_router
from app.api.v1.endpoints.server import router as server_router

routers = APIRouter()
router_list = [
    auth_router,
    user_router,
    subscribe_router,
    panel_router,
    payment_router,
    server_router
]

for router in router_list:
    routers.include_router(router, tags=["v1"])
