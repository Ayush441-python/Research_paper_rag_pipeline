from langchain_text_splitters import RecursiveCharacterTextSplitter


def text_splitter(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(documents)
    return chunks


# from loader import load_pdf


# docs = load_pdf("../data")
# chunks = text_splitter(docs)
# print(chunks[1])
# print(f"Number of chunks: {len(chunks)}")