from pydantic import BaseModel
from typing import Literal, Optional


# shape of data the user sends when asking a question
class QueryRequest(BaseModel):
    question: str
    user_id: str
    doc_id: Optional[str] = None
    pipeline_type: Literal["file_search", "vector_search"] = "file_search"


# shape of the response sent back with Gemini's answer
class QueryResponse(BaseModel):
    answer: str
    user_id: str
    pipeline_used: str
