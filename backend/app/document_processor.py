from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.vector_store import get_vector_store


def process_pdf(file_path: str, document_id: str):

    loader = PyPDFLoader(file_path)

    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)

    for chunk in chunks:

        chunk.metadata["document_id"] = document_id

    vector_store = get_vector_store()

    vector_store.add_documents(chunks)

    return {
        "pages": len(documents),
        "chunks": len(chunks)
    }