from src.vector_store import get_vector_store


def get_retriever(k: int = 4):
    """Return a retriever backed by Pinecone."""
    store = get_vector_store()
    return store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )
