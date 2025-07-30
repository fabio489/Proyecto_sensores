from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

app = FastAPI()

class Medicion(BaseModel):
    planta: str
    temperatura: float
    timestamp: str

# Historial en memoria
historial: List[Dict[str, Any]] = []

@app.post("/api/temperatura")
async def recibir_dato(data: Medicion):
    registro = data.dict()
    historial.append(registro)
    return {"ok": True, "mensaje": "Medición guardada"}

@app.get("/api/temperatura")
async def consultar_historial(planta: Optional[str] = None):
    if planta:
        filtradas = [med for med in historial if med["planta"] == planta]
        return {"mediciones": filtradas}
    return {"mediciones": historial}