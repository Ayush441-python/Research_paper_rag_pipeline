import os
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

from src.embeddings import embeddings

# ── Config from env ──────────────────────────────────────────────────────────
PINECONE_API_KEY   = os.getenv["PINECONE_API_KEY"]
PINECONE_INDEX     = os.getenv("PINECONE_INDEX", "rag-research")
PINECONE_CLOUD     = os.getenv("PINECONE_CLOUD", "aws")
PINECONE_REGION    = os.getenv("PINECONE_REGION", "us-east-1")
EMBEDDING_DIM      = 384   # bge-small-en-v1.5 output dim

_pc = Pinecone(api_key=PINECONE_API_KEY)


def _ensure_index():
    """Create the Pinecone serverless index if it doesn't exist yet."""
    existing = [idx.name for idx in _pc.list_indexes()]
    if PINECONE_INDEX not in existing:
        _pc.create_index(
            name=PINECONE_INDEX,
            dimension=EMBEDDING_DIM,
            metric="cosine",
            spec=ServerlessSpec(cloud=PINECONE_CLOUD, region=PINECONE_REGION),
        )


def get_vector_store() -> PineconeVectorStore:
    """Return a LangChain PineconeVectorStore connected to our index."""
    _ensure_index()
    return PineconeVectorStore(
        index_name=PINECONE_INDEX,
        embedding=embeddings,
        pinecone_api_key=PINECONE_API_KEY,
    )


def upsert_chunks(chunks: list) -> int:
    """Embed and upsert document chunks. Returns number of chunks added."""
    store = get_vector_store()
    store.add_documents(chunks)
    return len(chunks)
