from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.vector_store import upsert_chunks


_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)


def ingest_single_pdf(file_path: str, source_name: str = "") -> int:
    """
    Load, split, and upsert one PDF.
    Returns the number of chunks indexed.
    """
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # Tag each chunk with the original filename for traceability
    if source_name:
        for doc in docs:
            doc.metadata["source"] = source_name

    chunks = _splitter.split_documents(docs)
    return upsert_chunks(chunks)
