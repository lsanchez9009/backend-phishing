from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Modelo de datos que esperamos recibir del Frontend
class EmailRequest(BaseModel):
    texto: str

# Lista básica de palabras clave sospechosas (para el caso de estudio)
PALABRAS_SOSPECHOSAS = ["urgente", "contraseña", "bloqueado", "banco", "verificar", "cuenta", "ganador"]

@app.post("/analizar")
async def analizar_correo(correo: EmailRequest):
    texto_minusculas = correo.texto.lower()
    coincidencias = [palabra for palabra in PALABRAS_SOSPECHOSAS if palabra in texto_minusculas]
    
    if coincidencias:
        return {
            "riesgo": "ALTO",
            "mensaje": "Se detectaron posibles indicadores de phishing.",
            "palabras_clave_encontradas": coincidencias
        }
    
    return {
        "riesgo": "BAJO",
        "mensaje": "No se detectaron indicadores obvios de riesgo.",
        "palabras_clave_encontradas": []
    }