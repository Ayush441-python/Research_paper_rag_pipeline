from langchain_huggingface import HuggingFaceEmbeddings

# Singleton: initialised once, reused across retriever + vector_store
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)
