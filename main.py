from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.upload import router as upload_router
from app.api.routes.query import router as query_router

# main FastAPI app — all routers are registered here
app = FastAPI(title="RAGForge", version="1.0.0")

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(query_router)
