import time, tempfile, os
from google import genai
from google.genai import types


# creates a new Gemini file search store for a session
def create_store(client: genai.Client, session_id: str):
    return client.file_search_stores.create(
        config={"display_name": f"ragforge-{session_id}"}
    )


# uploads PDF bytes to Gemini store and waits until processing is done
def upload_to_store(client: genai.Client, file_bytes: bytes, filename: str, store_name: str):
    with tempfile.NamedTemporaryFile(suffix=f"_{filename}", delete=False) as f:
        f.write(file_bytes)
        tmp_path = f.name
    operation = client.file_search_stores.upload_to_file_search_store(
        file=tmp_path, file_search_store_name=store_name, config={"display_name": filename}
    )
    while not operation.done:
        time.sleep(3)
        operation = client.operations.get(operation)
    os.unlink(tmp_path)


# sends question to Gemini using file search tool and returns the answer
def ask_gemini(client: genai.Client, model: str, question: str, store_name: str) -> str:
    response = client.models.generate_content(
        model=model,
        contents=question,
        config=types.GenerateContentConfig(
            tools=[types.Tool(file_search=types.FileSearch(file_search_store_names=[store_name]))]
        ),
    )
    return response.text
