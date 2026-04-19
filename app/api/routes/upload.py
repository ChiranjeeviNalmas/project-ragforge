from fastapi import APIRouter, UploadFile, File, Form  # APIRouter groups routes, UploadFile handles PDF
from typing import Literal  # Literal restricts value to specific options
from app.schemas.upload import UploadResponse  # response shape
from app.pipelines.factory import PipelineFactory  # creates the right pipeline

router = APIRouter()  # create a router — routes are registered on this, not directly on app
factory = PipelineFactory()  # create factory once, reuse for every request


@router.post("/upload", response_model=UploadResponse)  # POST /upload returns UploadResponse shape
async def upload_pdf(
    file: UploadFile = File(...),  # the PDF file sent by user
    pipeline_type: Literal["file_search", "vector_search"] = Form("file_search"),  # which RAG type
):
    file_bytes = await file.read()  # read PDF as bytes
    pipeline = factory.create(pipeline_type)  # get the right pipeline from factory
    doc_id = pipeline.upload(file_bytes, file.filename)  # upload to GCS, get doc_id back
    return UploadResponse(  # send back the response
        doc_id=doc_id,
        filename=file.filename,
        gcs_uri=f"gs://ragforge-documents/{doc_id}/{file.filename}",
        pipeline_type=pipeline_type,
    )
