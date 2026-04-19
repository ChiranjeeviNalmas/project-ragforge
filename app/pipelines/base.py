from abc import ABC, abstractmethod
from typing import Optional


# contract that every RAG pipeline must follow
class BaseRAGPipeline(ABC):

    # store the PDF for a user and return user_id
    @abstractmethod
    def upload(self, file_bytes: bytes, filename: str, user_id: str) -> str:
        pass

    # answer the question — doc_id optional, falls back to searching all user's docs
    @abstractmethod
    def query(self, question: str, user_id: str, doc_id: Optional[str] = None) -> str:
        pass

    # return pipeline name eg. "file_search" or "vector_search"
    @abstractmethod
    def get_type(self) -> str:
        pass
