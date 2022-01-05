from fastapi import FastAPI

from app.core.shop_core import ShopCore
from app.infra.api import shop_api


def setup() -> FastAPI:
    app: FastAPI = FastAPI()
    app.include_router(shop_api)
    app.state.core = ShopCore()

    return app
