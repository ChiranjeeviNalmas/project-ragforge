# defines the liveness check route used to confirm the backend and db are up

from fastapi import APIRouter, Response

from app.db.health_check import check_database_connection

router = APIRouter()


@router.get("/health")
async def check_liveness(response: Response):
    try:
        await check_database_connection()
        db_status = "ok"
    except Exception:
        response.status_code = 503
        db_status = "error"
    return {"status": "ok", "db": db_status}
