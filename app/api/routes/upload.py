from fastapi import APIRouter, UploadFile, File, Form
from typing import Literal
from app.schemas.upload import UploadResponse
from app.pipelines.factory import PipelineFactory

router = APIRouter()
factory = PipelineFactory()


# receives PDF + user_id, uploads to user's Gemini store
@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    pipeline_type: Literal["file_search", "vector_search"] = Form("file_search"),
):
    file_bytes = await file.read()
    pipeline = factory.create(pipeline_type)
    pipeline.upload(file_bytes, file.filename, user_id)
    return UploadResponse(
        user_id=user_id,
        filename=file.filename,
        gcs_uri=f"gs://ragforge-documents/users/{user_id}/{file.filename}",
        pipeline_type=pipeline_type,
    )
