import json
from app.services.storage import GCSStorageService


# saves store name and filename to GCS so query can find it later
def save_metadata(storage: GCSStorageService, session_id: str, store_name: str, filename: str):
    metadata = json.dumps({"store_name": store_name, "filename": filename})
    storage.upload(metadata.encode(), f"{session_id}/metadata.json")


# reads store name from GCS metadata file
def load_store_name(storage: GCSStorageService, session_id: str) -> str:
    meta = storage.download(f"gs://{storage.bucket.name}/{session_id}/metadata.json")
    return json.loads(meta)["store_name"]
