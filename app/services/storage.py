from abc import ABC, abstractmethod
from google.cloud import storage
from app.core.config import get_settings


# contract that any storage implementation must follow
class BaseStorageService(ABC):

    # upload file bytes to storage, return the URI
    @abstractmethod
    def upload(self, file_bytes: bytes, destination: str) -> str:
        pass

    # download file from storage, return raw bytes
    @abstractmethod
    def download(self, gcs_uri: str) -> bytes:
        pass


# Google Cloud Storage implementation
class GCSStorageService(BaseStorageService):

    def __init__(self):
        settings = get_settings()
        self.client = storage.Client(project=settings.gcp_project_id)
        self.bucket = self.client.bucket(settings.gcs_bucket_name)

    # uploads bytes to GCS and returns the gs:// URI
    def upload(self, file_bytes: bytes, destination: str) -> str:
        blob = self.bucket.blob(destination)
        blob.upload_from_string(file_bytes)
        return f"gs://{self.bucket.name}/{destination}"

    # downloads a file from GCS using its gs:// URI
    def download(self, gcs_uri: str) -> bytes:
        blob_name = gcs_uri.replace(f"gs://{self.bucket.name}/", "")
        return self.bucket.blob(blob_name).download_as_bytes()
