from abc import ABC, abstractmethod
from typing import Optional


# contract that every RAG pipeline must follow
class BaseRAGPipeline(ABC):

    # store the PDF and return a doc_id
    @abstractmethod
    def upload(self, file_bytes: bytes, filename: str) -> str:
        pass

    # answer the question using the stored document
    @abstractmethod
    def query(self, question: str, doc_id: Optional[str] = None) -> str:
        pass

    # return pipeline name eg. "file_search" or "vector_search"
    @abstractmethod
    def get_type(self) -> str:
        pass
