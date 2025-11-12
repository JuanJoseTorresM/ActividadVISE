"""
Configuración de OpenTelemetry para integración con Grafana Cloud
"""
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import logging

logger = logging.getLogger(__name__)

def setup_tracing(app):
    """
    Configura OpenTelemetry para enviar trazas a Grafana Cloud (Tempo)
    """
    # Definir el nombre del servicio
    resource = Resource(attributes={
        SERVICE_NAME: "vise-api"
    })
    
    # Crear el TracerProvider
    provider = TracerProvider(resource=resource)
    
    # Configurar el exportador OTLP para Grafana Cloud
    # NOTA: Reemplaza con tus credenciales de Grafana Cloud si las tienes
    # Por ahora usamos una configuración local/de consola
    try:
        # Para desarrollo local, puedes comentar el exportador OTLP
        # y usar ConsoleSpanExporter para ver las trazas en consola
        from opentelemetry.sdk.trace.export import ConsoleSpanExporter
        console_exporter = ConsoleSpanExporter()
        processor = BatchSpanProcessor(console_exporter)
        provider.add_span_processor(processor)
        logger.info("✅ Trazas configuradas para imprimirse en consola (desarrollo local)")
    except Exception as e:
        logger.error(f"❌ Error configurando trazas: {e}")
    
    # Establecer como proveedor global
    trace.set_tracer_provider(provider)
    
    # Instrumentar FastAPI
    FastAPIInstrumentor.instrument_app(app)
    
    return provider
