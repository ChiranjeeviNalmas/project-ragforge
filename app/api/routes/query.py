from fastapi import APIRouter
from app.schemas.query import QueryRequest, QueryResponse
from app.pipelines.factory import PipelineFactory

router = APIRouter()
factory = PipelineFactory()


# receives a question and returns Gemini's answer using the right pipeline
@router.post("/query", response_model=QueryResponse)
async def query_document(request: QueryRequest):
    pipeline = factory.create(request.pipeline_type)
    answer = pipeline.query(request.question, request.doc_id)
    return QueryResponse(
        answer=answer,
        doc_id=request.doc_id,
        pipeline_used=pipeline.get_type()
    )
