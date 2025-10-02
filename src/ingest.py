import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH", "../document.pdf")

def ingest_pdf():
    for k in (
        "GOOGLE_EMBEDDING_MODEL",
        "OPENAI_API_KEY",
        "OPENAI_EMBEDDING_MODEL",
        "DATABASE_URL",
        "PG_VECTOR_COLLECTION_NAME",
        "PDF_PATH",
        "PGVECTOR_COLLECTION",
        "PGVECTOR_URL"
     ):
        if not os.getenv(k):
            raise RuntimeError(f"Environment variable {k} is not set")

    docs = PyPDFLoader(str(PDF_PATH)).load()

    splits = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150, add_start_index=False).split_documents(docs)

    enriched = [
    Document(
        page_content=d.page_content,
        metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
    )
        for d in splits
    ]

    ids = [f"doc-{i}" for i in range(len(enriched))]

    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL",
    "text-embedding-3-small"))

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PGVECTOR_COLLECTION"),
        connection=os.getenv("PGVECTOR_URL"),
        use_jsonb=True,
    )

    store.add_documents(documents=enriched, ids=ids)

    if not splits:
        raise SystemExit(0)

if __name__ == "__main__":
    ingest_pdf()