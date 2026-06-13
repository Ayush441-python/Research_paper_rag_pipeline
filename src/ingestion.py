from loader import load_pdf
from splitter import text_splitter
from vector_store import create_vector_store

import os

DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data"
)


def ingest_documents():
    print("Loading PDFs...")
    docs = load_pdf(DATA_PATH)
    print(f"Loaded {len(docs)} pages")

    print("Splitting documents...")
    chunks = text_splitter(docs)
    print(f"Created {len(chunks)} chunks")

    print("Creating vector store...")
    create_vector_store(chunks)

    print("Ingestion completed successfully!")


if __name__ == "__main__":
    ingest_documents()


    