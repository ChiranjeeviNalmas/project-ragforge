# defines the liveness check route used to confirm the backend is up

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def check_liveness():
    return {"status": "ok"}
