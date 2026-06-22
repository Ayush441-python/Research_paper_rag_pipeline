# Research Paper RAG

FastAPI backend + Streamlit frontend + Pinecone + Groq.

## Project structure

```
.
├── app.py              # FastAPI (backend)
├── streamlit_app.py    # Streamlit (frontend)
├── src/
│   ├── chain.py
│   ├── embeddings.py
│   ├── ingestion.py
│   ├── retriever.py
│   └── vector_store.py
├── requirements.txt
├── render.yaml
└── .env.example
```

## Local setup

```bash
cp .env.example .env
# fill in GROQ_API_KEY and PINECONE_API_KEY

pip install -r requirements.txt

# Terminal 1 — FastAPI
uvicorn app:app --reload --port 8000

# Terminal 2 — Streamlit
streamlit run streamlit_app.py
```

Open `http://localhost:8501`

## Deploy to Render

Two services defined in `render.yaml`:

1. `research-rag-api` — FastAPI on Render
2. `research-rag-ui` — Streamlit on Render

Steps:
1. Push to GitHub → Render → **New → Blueprint** → connect repo (picks up `render.yaml` automatically)
2. Set `GROQ_API_KEY` and `PINECONE_API_KEY` as secret env vars
3. After the API service deploys, copy its URL into `API_BASE_URL` on the UI service
