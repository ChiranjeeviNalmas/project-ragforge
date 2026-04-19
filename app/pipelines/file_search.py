from typing import Optional
from google import genai
from app.pipelines.base import BaseRAGPipeline
from app.services.storage import GCSStorageService
from app.core.config import get_settings
from app.utils.gemini_store import get_or_create_store, upload_to_store, ask_gemini
from app.utils.metadata import save_metadata, load_store_name


# Type 1 RAG pipeline — one store per user, no doc_id needed for queries
class FileSearchPipeline(BaseRAGPipeline):

    def __init__(self):
        self.storage = GCSStorageService()
        self.client = genai.Client(api_key=get_settings().google_api_key)
        self.model = get_settings().gemini_model_name

    # uploads PDF to user's store, creates store if first time
    def upload(self, file_bytes: bytes, filename: str, user_id: str) -> str:
        store = get_or_create_store(self.client, user_id)
        self.storage.upload(file_bytes, f"users/{user_id}/{filename}")
        upload_to_store(self.client, file_bytes, filename, store.name)
        save_metadata(self.storage, user_id, store.name)
        return user_id

    # searches all user's docs, or specific doc if doc_id provided
    def query(self, question: str, user_id: str, doc_id: Optional[str] = None) -> str:
        store_name = load_store_name(self.storage, user_id)
        # if doc_id given, guide Gemini to focus on that specific file
        focused_question = f"From the document '{doc_id}', {question}" if doc_id else question
        return ask_gemini(self.client, self.model, focused_question, store_name)

    def get_type(self) -> str:
        return "file_search"
