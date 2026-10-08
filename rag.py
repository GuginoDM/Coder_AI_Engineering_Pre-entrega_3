import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv
from schemas import RAGResponse

load_dotenv()

VECTORSTORE_DIR = "./vectorstore"

# 1. Inicializar componentes
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(persist_directory=VECTORSTORE_DIR, embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser_llm = PydanticOutputParser(pydantic_object=RAGResponse)

# 2. Prompt estricto anti-alucinaciones con instrucciones de formato
prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "Eres un asistente técnico estricto. Responde a la pregunta del usuario utilizando EXCLUSIVAMENTE el CONTEXTO proporcionado.\n\n"
     "REGLAS OBLIGATORIAS:\n"
     "1. Si la respuesta no figura explícitamente en el CONTEXTO, debes responder exactamente: 'No tengo acceso a esa información en los documentos proporcionados.'\n"
     "2. No asumas, deduzcas ni inventes información fuera del texto.\n\n"
     "{format_instructions}\n\n"
     "CONTEXTO:\n{context}"),
    ("human", "{question}")
]).partial(format_instructions=parser_llm.get_format_instructions())

# Cadena LCEL: prompt -> llm -> parser (recibe contexto y pregunta ya armados)
chain = prompt | llm | parser_llm

async def get_rag_response(query: str) -> RAGResponse:
    """
    Función asíncrona que:
    a. Realiza una búsqueda de similitud en ChromaDB.
    b. Construye el contexto y las fuentes.
    c. Ejecuta la cadena LCEL asíncrona.
    d. Devuelve un objeto Pydantic RAGResponse validado.
    """
    # a. Recuperación asíncrona de fragmentos
    docs = await retriever.ainvoke(query)
    
    # Extraer texto de context y referencias únicas
    context_text = "\n\n".join([doc.page_content for doc in docs])
    sources = list(set([os.path.basename(doc.metadata.get("source", "Desconocido")) for doc in docs]))

    # b & c. Ejecutar cadena LCEL
    response: RAGResponse = await chain.ainvoke({
        "context": context_text,
        "question": query
    })
    
    # Si la respuesta es válida y no fue denegada por falta de información, adjuntar las referencias
    if "No tengo acceso" not in response.respuesta:
        response.referencias = sources
    else:
        response.referencias = []

    return response