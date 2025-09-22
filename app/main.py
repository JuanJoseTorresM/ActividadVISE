from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="VISE API",
    description="API para gestión de clientes, tarjetas y compras de VISE",
    version="1.0.0"
)

# Incluir las rutas
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de VISE"}
