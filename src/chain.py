import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
    temperature=0.2,
)

prompt = ChatPromptTemplate.from_template("""
You are a precise AI Research Assistant.

Use ONLY the information provided in the context below to answer the question.

Rules:
- Answer clearly and accurately based solely on the context.
- Use bullet points when the answer has multiple parts.
- Never fabricate or infer beyond what the context states.
- If the answer is not in the context, respond exactly with:
  "I couldn't find that information in the uploaded documents."

Context:
{context}

Question:
{question}

Answer:
""")

chain = prompt | llm | StrOutputParser()
