from google import genai
from google.genai import types
from google.cloud import storage
from app.core.config import get_settings


# deletes all Gemini file search stores
def delete_all_stores(client):
    stores = list(client.file_search_stores.list())
    if not stores:
        print("No Gemini stores found.")
        return
    for store in stores:
        # delete documents inside store first before deleting store
        for doc in client.file_search_stores.documents.list(parent=store.name):
            print(f"Deleting document: {doc.display_name}")
            # force=True deletes document even if it has content inside
            client.file_search_stores.documents.delete(name=doc.name, config=types.DeleteDocumentConfig(force=True))
        print(f"Deleting store: {store.display_name}")
        client.file_search_stores.delete(name=store.name)
        print(f"Deleted ✅")


# deletes all files inside the GCS bucket
def delete_all_gcs_files():
    settings = get_settings()
    gcs = storage.Client(project=settings.gcp_project_id)
    bucket = gcs.bucket(settings.gcs_bucket_name)
    blobs = list(bucket.list_blobs())
    if not blobs:
        print("No GCS files found.")
        return
    for blob in blobs:
        print(f"Deleting GCS file: {blob.name}")
        blob.delete()
        print(f"Deleted ✅")


if __name__ == "__main__":
    client = genai.Client(api_key=get_settings().google_api_key)
    delete_all_stores(client)
    delete_all_gcs_files()
