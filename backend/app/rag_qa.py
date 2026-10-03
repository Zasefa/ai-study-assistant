from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate

from app.embeddings import embeddings
from app.llm import model


# Load existing vector database
vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)


# Create retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


# Prompt for RAG
rag_prompt = PromptTemplate.from_template(
    """
You are an AI Study Assistant.

Answer the user's question using ONLY the context provided below.

If the answer is not present in the context, say:
"I could not find this information in the provided document."

Context:
{context}

Question:
{question}

Give a clear and beginner-friendly answer.
"""
)


# Ask a question
question = "What is the main objective of this project?"


# Retrieve relevant chunks
documents = retriever.invoke(question)


# Combine chunks into one context
context = "\n\n".join(
    document.page_content
    for document in documents
)


# Create final prompt
prompt = rag_prompt.format(
    context=context,
    question=question
)


# Ask Gemini
response = model.invoke(prompt)


print("\nAnswer:\n")
print(response.content)