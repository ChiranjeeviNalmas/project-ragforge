import json
from app.services.storage import GCSStorageService


# saves store name to GCS keyed by user_id
def save_metadata(storage: GCSStorageService, user_id: str, store_name: str):
    metadata = json.dumps({"store_name": store_name})
    storage.upload(metadata.encode(), f"users/{user_id}/metadata.json")


# reads store name from GCS for this user
def load_store_name(storage: GCSStorageService, user_id: str) -> str:
    meta = storage.download(f"gs://{storage.bucket.name}/users/{user_id}/metadata.json")
    return json.loads(meta)["store_name"]
