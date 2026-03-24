from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

DB_DIR = "db/chroma_db"


def get_retriever():
    print("ADA error in get_retriever function")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vectorstore = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings
    )

    return vectorstore.as_retriever(search_kwargs={"k": 1})