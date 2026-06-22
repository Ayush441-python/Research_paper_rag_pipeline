import os
import shutil
import tempfile

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.chain import chain
from src.retriever import get_retriever
from src.ingestion import ingest_single_pdf

app = FastAPI(title="Research Paper RAG API")

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str


@app.post("/ask")
def ask_question(request: QueryRequest):
    try:
        retriever = get_retriever(k=4)
        docs = retriever.invoke(request.question)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Vector store unavailable: {str(e)}")

    if not docs:
        return {
            "question": request.question,
            "answer": "I couldn't find relevant information in the uploaded documents."
        }

    context = "\n\n".join(doc.page_content for doc in docs)

    response = chain.invoke({
        "context": context,
        "question": request.question
    })

    return {
        "question": request.question,
        "answer": response
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        chunks_added = ingest_single_pdf(tmp_path, source_name=file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")
    finally:
        os.remove(tmp_path)

    return {
        "message": f"'{file.filename}' uploaded and indexed successfully.",
        "chunks_indexed": chunks_added
    }


@app.get("/health")
def health():
    return {"status": "ok"}
