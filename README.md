# RAGForge GCP

## Setup

### 1. Install dependencies
```bash
make install
```

### 2. Set up environment
```bash
cp .env.example .env
# fill in your values in .env
```

### 3. Create GCS bucket
```bash
gcloud config set project project-orbit-490207
gcloud storage buckets create gs://ragforge-documents --location=us-central1
```

### 4. Run the server
```bash
make dev
```

---

## Cleanup

### Delete GCS bucket and all files inside it
```bash
gcloud storage rm -r gs://ragforge-documents
```

### Delete the bucket itself
```bash
gcloud storage buckets delete gs://ragforge-documents
```

---

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | check if server is running |
| POST | `/upload` | upload a PDF |
| POST | `/query` | ask a question |

## Test

```bash
# health
curl http://127.0.0.1:8000/health

# upload
curl -X POST http://127.0.0.1:8000/upload \
  -F "file=@/Users/ushanagallashashank/Downloads/your-file.pdf" \
  -F "pipeline_type=file_search"

# query
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "what is this about?", "doc_id": "paste-doc-id-here"}'
```
