from fastapi import FastAPI
from app.routes import router
from app.tracing import setup_tracing
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from app.exporter import provider  # ✅ configuración de OpenTelemetry para Axiom
import logging
import sys

# -------------------------------------
# 🧠 Configuración de Logging para Loki
# -------------------------------------
logger = logging.getLogger("vise_api")
logger.setLevel(logging.INFO)

# Imprimir también en consola
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# -------------------------------------
# 🚀 Inicialización de la aplicación FastAPI
# -------------------------------------
app = FastAPI(
    title="VISE API",
    description="""## API para gestión de clientes, tarjetas y compras de VISE
    
    Esta API permite:
    - 📝 *Registrar clientes* con validación completa de datos  
    - 💳 *Procesar compras* con tarjetas VISE  
    - 🎯 *Aplicar descuentos automáticos* para miembros del VISE Club  
    - 📊 *Monitoreo y trazabilidad* con OpenTelemetry y Grafana Cloud  
    - 🧩 *Exportación de trazas a Axiom* mediante OpenTelemetry  
    
    ### Tipos de tarjeta disponibles:
    - *Classic*: Tarjeta básica  
    - *Gold*: Tarjeta premium con beneficios adicionales  
    - *Platinum*: Tarjeta exclusiva con máximos beneficios  
    
    ### Descuentos VISE Club:
    Los miembros del VISE Club reciben descuentos automáticos en sus compras.
    """,
    version="1.0.0",
    contact={
        "name": "Equipo VISE",
        "email": "support@vise.com",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=[
        {"name": "Clientes", "description": "Gestión de clientes VISE"},
        {"name": "Compras", "description": "Procesamiento de transacciones con tarjetas VISE"},
    ]
)

# -------------------------------------
# ⚙ Configurar OpenTelemetry para Grafana Cloud
# -------------------------------------
setup_tracing(app)
logger.info("✅ OpenTelemetry configurado correctamente con Grafana Cloud (Tempo/Prometheus/Loki)")

# -------------------------------------
# 📡 Integración adicional: Exportación de trazas a Axiom
# -------------------------------------
try:
    FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)
    logger.info("✅ Integración de OpenTelemetry con Axiom activada correctamente.")
except Exception as e:
    logger.error(f"❌ Error al configurar Axiom: {e}")

# -------------------------------------
# 🔗 Registrar las rutas de la API
# -------------------------------------
app.include_router(router)

# -------------------------------------
# 🌐 Endpoint raíz
# -------------------------------------
@app.get(
    "/",
    tags=["General"],
    summary="Endpoint raíz",
    description="Confirma que la API está funcionando correctamente y lista para monitoreo."
)
def root():
    logger.info("🏁 Petición al endpoint raíz /")
    return {
        "message": "Bienvenido a la API de VISE",
        "version": "1.0.0",
        "status": "active",
        "observability": {
            "metrics": "Prometheus (Grafana Cloud)",
            "traces": {
                "grafana": "Tempo",
                "axiom": "OpenTelemetry Exporter"
            },
            "logs": "Loki (Grafana Cloud)"
        },
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        }
    }