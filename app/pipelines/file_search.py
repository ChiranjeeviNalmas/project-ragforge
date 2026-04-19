import uuid
from typing import Optional
from google import genai
from app.pipelines.base import BaseRAGPipeline
from app.services.storage import GCSStorageService
from app.core.config import get_settings
from app.utils.gemini_store import create_store, upload_to_store, ask_gemini
from app.utils.metadata import save_metadata, load_store_name


# Type 1 RAG pipeline — stores PDF in GCS, searches via Gemini File Search Store
class FileSearchPipeline(BaseRAGPipeline):

    def __init__(self):
        self.storage = GCSStorageService()
        self.client = genai.Client(api_key=get_settings().google_api_key)
        self.model = get_settings().gemini_model_name


    # saves PDF to GCS and Gemini store, returns session_id
    def upload(self, file_bytes: bytes, filename: str) -> str:
        session_id = str(uuid.uuid4())
        self.storage.upload(file_bytes, f"{session_id}/{filename}")
        store = create_store(self.client, session_id)
        upload_to_store(self.client, file_bytes, filename, store.name)
        save_metadata(self.storage, session_id, store.name, filename)
        return session_id


    # loads store name from GCS and asks Gemini the question
    def query(self, question: str, doc_id: Optional[str] = None) -> str:
        store_name = load_store_name(self.storage, doc_id)
        return ask_gemini(self.client, self.model, question, store_name)


    def get_type(self) -> str:
        return "file_search"
