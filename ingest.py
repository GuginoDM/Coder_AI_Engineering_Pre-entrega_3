import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = "./data"
VECTORSTORE_DIR = "./vectorstore"

def run_ingestion():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Verificar si la base de datos ya existe para no re-indexar
    if os.path.exists(VECTORSTORE_DIR) and os.listdir(VECTORSTORE_DIR):
        print("ℹ️ La base de datos vectorial ya existe en ./vectorstore. Omitiendo ingesta.")
        return Chroma(persist_directory=VECTORSTORE_DIR, embedding_function=embeddings)

    print("🔄 Procesando documentos e iniciando ingesta en ChromaDB...")
    
    # 1. Cargar documentos desde la carpeta /data
    loader = DirectoryLoader(
        DATA_DIR, 
        glob="**/*.*", 
        loader_cls=TextLoader, 
        loader_kwargs={"encoding": "utf-8"}
    )
    docs = loader.load()

    if not docs:
        raise ValueError("❌ No se encontraron archivos en la carpeta /data.")

    # 2. Chunking estratégico basado en tokens de OpenAI (tiktoken)
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-4o-mini",
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(docs)
    print(f"📄 Cargados {len(docs)} documentos y divididos en {len(chunks)} fragmentos (chunks).")

    # 3. Guardar y persistir en ChromaDB
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTORSTORE_DIR
    )
    print("✅ Ingesta completada con éxito y persistida en ./vectorstore")
    return vectorstore

if __name__ == "__main__":
    run_ingestion()