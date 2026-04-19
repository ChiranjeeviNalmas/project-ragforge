from fastapi import APIRouter
from app.schemas.query import QueryRequest, QueryResponse
from app.pipelines.factory import PipelineFactory

router = APIRouter()
factory = PipelineFactory()


# receives question + user_id, searches all of user's docs
@router.post("/query", response_model=QueryResponse)
async def query_document(request: QueryRequest):
    pipeline = factory.create(request.pipeline_type)
    answer = pipeline.query(request.question, request.user_id, request.doc_id)
    return QueryResponse(
        answer=answer,
        user_id=request.user_id,
        pipeline_used=pipeline.get_type()
    )
