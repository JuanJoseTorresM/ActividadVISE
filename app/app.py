# app.py
from flask import Flask
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry import trace
import app.exporter as exporter
import requests

# Crear app Flask
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

# Tracer de Axiom
tracer = trace.get_tracer(__name__)
# URL base de tu API FastAPI
API_URL = "http://127.0.0.1:8000"

# ---- Endpoint de prueba 1: Crear cliente ----
@app.route("/test_crear_cliente")
def test_crear_cliente():
    with tracer.start_as_current_span("test_crear_cliente"):
        payload = {
            "nombre": "Juan Torres",
            "email": "juan@example.com",
            "tipo_tarjeta": "Gold",
            "miembro_club": True
        }
        response = requests.post(f"{API_URL}/clientes", json=payload)
        return {
            "endpoint": "/clientes",
            "status_code": response.status_code,
            "response": response.json()
        }

# ---- Endpoint de prueba 2: Hacer compra ----
@app.route("/test_hacer_compra")
def test_hacer_compra():
    with tracer.start_as_current_span("test_hacer_compra"):
        payload = {
            "cliente_id": 1,
            "monto": 250.00,
            "descripcion": "Compra en tienda VISE",
            "tarjeta": "Gold"
        }
        response = requests.post(f"{API_URL}/compras", json=payload)
        return {
            "endpoint": "/compras",
            "status_code": response.status_code,
            "response": response.json()
        }

if __name__ == "__main__":
    app.run(port=8080, debug=True)