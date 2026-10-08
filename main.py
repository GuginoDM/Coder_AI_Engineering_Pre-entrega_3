import asyncio
from ingest import run_ingestion
from rag import get_rag_response

async def run_tests():
    run_ingestion()

    print("\n" + "="*60)
    print("INICIANDO PRUEBAS DEL SISTEMA RAG ASÍNCRONO")
    print("="*60)

    # Prueba 1: Pregunta cuya respuesta se encuentra en los documentos
    pregunta_valida = "¿Cada cuánto tiempo deben cambiarse las contraseñas y a través de qué portal se piden accesos?"
    print(f"\n [PRUEBA 1 - Respuesta esperada en contexto]: '{pregunta_valida}'")
    
    res1 = await get_rag_response(pregunta_valida)
    print(f" Respuesta: {res1.respuesta}")
    print(f" Referencias: {res1.referencias}")

    # Prueba 2: Pregunta Trampa (NO esta en los documentos)
    pregunta_trampa = "¿Cuál es el presupuesto anual asignado a las licencias de software para el año 2026?"
    print(f"\n [PRUEBA 2 - Pregunta Trampa / Sin Contexto]: '{pregunta_trampa}'")
    
    res2 = await get_rag_response(pregunta_trampa)
    print(f" Respuesta: {res2.respuesta}")
    print(f" Referencias: {res2.referencias}")

if __name__ == "__main__":
    asyncio.run(run_tests())
