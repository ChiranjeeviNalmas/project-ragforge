from fastapi import APIRouter

router = APIRouter()


# confirms the app is running
@router.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}
