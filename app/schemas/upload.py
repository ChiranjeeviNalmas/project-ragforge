from pydantic import BaseModel
from typing import Literal


# shape of the response sent back after a PDF is uploaded
class UploadResponse(BaseModel):
    user_id: str
    filename: str
    gcs_uri: str
    pipeline_type: Literal["file_search", "vector_search"]
    status: str = "processed"
