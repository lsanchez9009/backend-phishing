from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# --- INICIO DE LA SOLUCIÓN CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # El asterisco permite que cualquier web se conecte (ideal para pruebas/MVP)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- FIN DE LA SOLUCIÓN CORS ---

class EmailRequest(BaseModel):
    texto: str

PALABRAS_SOSPECHOSAS = ["urgente", "contraseña", "bloqueado", "banco", "verificar", "cuenta", "ganador"]

@app.post("/analizar")
async def analizar_correo(correo: EmailRequest):
    texto_minusculas = correo.texto.lower()
    coincidencias = [palabra for palabra en PALABRAS_SOSPECHOSAS if palabra in texto_minusculas]
    
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