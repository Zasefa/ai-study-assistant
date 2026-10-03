from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# 1. Load PDF
loader = PyPDFLoader("documents/ntcc final presentation.pdf")

documents = loader.load()

print(f"Number of pages loaded: {len(documents)}")


# 2. Create text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)


# 3. Split documents into chunks
chunks = text_splitter.split_documents(documents)

print(f"Number of chunks created: {len(chunks)}")


# 4. Show first chunk
print("\nFirst chunk:\n")
print(chunks[0].page_content)