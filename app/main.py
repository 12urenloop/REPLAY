from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.routing import APIRoute
from app.core.config import settings
from app.api.routes import router
from app.core.db import init_db
from app.core.state import load_state


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    await load_state()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)


app.include_router(router)
