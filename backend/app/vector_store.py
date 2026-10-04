from langchain_chroma import Chroma
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


class ChromaEmbeddingAdapter:

    def __init__(self):
        self.embedding_function = DefaultEmbeddingFunction()

    def embed_documents(self, texts):
        return self.embedding_function(texts)

    def embed_query(self, text):
        return self.embedding_function([text])[0]


embedding_function = ChromaEmbeddingAdapter()


def get_vector_store():

    return Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding_function
    )


def get_retriever(k=3, document_id=None):

    vector_store = get_vector_store()

    search_kwargs = {
        "k": k
    }

    if document_id:

        search_kwargs["filter"] = {
            "document_id": document_id
        }

    return vector_store.as_retriever(
        search_kwargs=search_kwargs
    )


def search_with_scores(
    query,
    k=3,
    document_id=None
):

    vector_store = get_vector_store()

    filter_value = None

    if document_id:

        filter_value = {
            "document_id": document_id
        }

    results = vector_store.similarity_search_with_score(
        query,
        k=k,
        filter=filter_value
    )

    return results