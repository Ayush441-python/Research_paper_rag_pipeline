from langchain_redis import RedisVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

from src.ingestion import ingest_documents

### docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
REDIS_URL = "redis://localhost:6379"
INDEX_NAME = "research_papers"

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


def load_vector_store():
    return RedisVectorStore(
        embeddings=embeddings,
        index_name=INDEX_NAME,
        redis_url=REDIS_URL
    )


def get_retriever(k=4):
    try:
        vector_store = load_vector_store()

        # Test if index exists by running a search
        vector_store.similarity_search("test", k=1)

        print("Loaded existing Redis index.")

    except Exception:
        print("Redis index not found.")
        print("Running ingestion...")

        ingest_documents()

        vector_store = load_vector_store()

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )