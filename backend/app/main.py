# entrypoint that boots the fastapi app and mounts the api routes

from fastapi import FastAPI

from app.api.health import router as health_router
from app.db.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(health_router)
