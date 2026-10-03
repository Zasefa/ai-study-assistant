from langchain_chroma import Chroma

from app.embeddings import embeddings


vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)


results = vector_store.similarity_search(
    "project objective",
    k=3
)


for i, document in enumerate(results):

    print(f"\n--- Result {i + 1} ---")

    print("Content:")
    print(document.page_content[:300])

    print("\nMetadata:")
    print(document.metadata)