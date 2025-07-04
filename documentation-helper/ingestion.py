from dotenv import load_dotenv

load_dotenv()

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

def ingest_docs():
    import os
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    docs_path = os.getenv("DOCS_PATH", "/home/mavis021/udemy/documentation-helper/langchain-docs/api.python.langchain.com/en/latest/memory")
    loader = ReadTheDocsLoader(docs_path, encoding="latin-1")

    raw_documents = loader.load()
    print(f"loaded {len(raw_documents)} documents")
    if not raw_documents:
        print("No documents loaded. Please check the docs_path and encoding.")
        return

    print(type(raw_documents[0]))
    print(raw_documents[0])
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    documents = text_splitter.split_documents(raw_documents)
    print(f"Split into {len(documents)} documents")
    if not documents:
        print("Text splitting failed. Please check the format of raw_documents.")
        return
    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace(
            "/home/mavis021/udemy/documentation-helper/langchain-docs",
            "https://api.python.langchain.com/en/latest"
        )
        new_url = new_url.replace("langchain-docs", "https:/")
        doc.metadata.update({"source": new_url})

    max_bytes = 3_194_304  # 4 MB
    filtered_docs = [doc for doc in documents if len(doc.page_content.encode('utf-8')) < max_bytes]

    print(f"Going to add {len(filtered_docs)} to Pinecone")
    try:
        PineconeVectorStore.from_documents(
            filtered_docs, embeddings, index_name="langchain-doc-index"
        )
        print("****Loading to vectorstore done ***")
    except Exception as e:
        print(f"Error loading documents to Pinecone: {e}")


if __name__ == "__main__":
    ingest_docs()