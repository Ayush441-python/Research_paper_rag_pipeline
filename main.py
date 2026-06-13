from src.retriever import get_retriever
from src.chain import chain

retriever = get_retriever()

query = input("Ask a question: ")

docs = retriever.invoke(query)

context = "\n\n".join(
    doc.page_content for doc in docs
)

response = chain.invoke({
    "context": context,
    "question": query
})

print("\nAnswer:")
print(response)