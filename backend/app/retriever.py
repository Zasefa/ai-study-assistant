from langchain_chroma import Chroma

from app.embeddings import embeddings


# Load existing vector database
vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)


# Create retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


# Test question
question = "What is the main objective of this project?"


# Retrieve relevant chunks
results = retriever.invoke(question)


print(f"Number of chunks retrieved: {len(results)}")

for i, document in enumerate(results):
    print(f"\n--- Chunk {i + 1} ---")
    print(document.page_content)