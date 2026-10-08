from pydantic import BaseModel, Field
from typing import List

class RAGResponse(BaseModel):
    respuesta: str = Field(
        description="Respuesta directa a la pregunta basada estrictamente en el contexto. Si no está en el texto, responder que no se cuenta con esa información."
    )
    referencias: List[str] = Field(
        default_factory=list,
        description="Lista con las rutas o nombres de los archivos fuente utilizados para responder."
    )