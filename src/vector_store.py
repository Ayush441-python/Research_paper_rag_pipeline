from langchain_redis import RedisVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

### docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest

REDIS_URL = "redis://localhost:6379"
INDEX_NAME = "research_papers"

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


def create_vector_store(chunks):
    vector_store = RedisVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        redis_url=REDIS_URL,
        index_name=INDEX_NAME
    )

    return vector_store
