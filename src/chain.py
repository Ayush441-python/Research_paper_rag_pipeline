from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import os
from dotenv import load_dotenv

load_dotenv()
# print("GROQ_API_KEY =", os.getenv("GROQ_API_KEY"))
# print("LANGCHAIN_API_KEY =", os.getenv("LANGCHAIN_API_KEY"))
# print("LANGCHAIN_PROJECT =", os.getenv("LANGCHAIN_PROJECT"))

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

prompt = ChatPromptTemplate.from_template("""
Answer the question using only the provided context.
If the answer is not in the context, say:
"I couldn't find that information in the documents."
                                          
Context:
{context}

Question:
{question}
""")

parser = StrOutputParser()

chain = prompt | llm | parser