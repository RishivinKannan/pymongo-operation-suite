"""
Observability configuration for PyMongo testing
Integrates OpenTelemetry, Datadog, and Atatus
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor

from atatus.contrib.flask import Atatus

def setup_opentelemetry():
    """Initialize OpenTelemetry with Jaeger exporter"""
    service_name = os.getenv('OTEL_SERVICE_NAME', 'pymongo-testing')
    otlp_endpoint = os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://localhost:4317')
    
    # Create resource with service name
    resource = Resource.create({
        "service.name": service_name,
        "service.version": "1.0.0",
        "deployment.environment": "development"
    })
    
    # Set up tracer provider
    tracer_provider = TracerProvider(resource=resource)
    
    # Configure OTLP exporter for Jaeger
    otlp_exporter = OTLPSpanExporter(
        endpoint=otlp_endpoint,
        insecure=True
    )
    
    # Add span processor
    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)
    
    # Set global tracer provider
    trace.set_tracer_provider(tracer_provider)
    
    # Instrument pymongo
    PymongoInstrumentor().instrument()
    
    print(f"✓ OpenTelemetry configured - Service: {service_name}, Endpoint: {otlp_endpoint}")
    return tracer_provider


def setup_datadog():
    """Initialize Datadog APM if API key is provided"""
    dd_api_key = os.getenv('DD_API_KEY')
    
    if dd_api_key:
        try:
            from ddtrace import tracer
            from ddtrace import patch
            
            # Patch pymongo
            patch(pymongo=True)
            
            service = os.getenv('DD_SERVICE', 'pymongo-testing')
            env = os.getenv('DD_ENV', 'development')
            version = os.getenv('DD_VERSION', '1.0.0')
            
            tracer.configure(
                hostname=os.getenv('DD_AGENT_HOST', 'localhost'),
                port=8126,
            )
            
            tracer.set_tags({
                'service': service,
                'env': env,
                'version': version
            })
            
            print(f"✓ Datadog APM configured - Service: {service}, Env: {env}")
            return True
        except Exception as e:
            print(f"⚠ Datadog setup failed: {e}")
            return False
    else:
        print("ℹ Datadog API key not provided - skipping Datadog integration")
        return False


def setup_atatus(app):
    """Initialize Atatus monitoring if license key is provided"""
    try:
        app_name = os.environ.get('ATATUS_APP_NAME', 'pymongo-operations-suite')
        app.config['ATATUS'] = {
            'APP_NAME': app_name,
            'LICENSE_KEY': os.environ.get('ATATUS_LICENSE_KEY'),
            'TRACING': True,
            'ANALYTICS': True,
            'ANALYTICS_CAPTURE_OUTGOING': True,
            'LOG_BODY': 'all',
            # 'LOG_FILE': '/home/namlabs/development/testing/pymongo-test/atatus.log',
            # 'LOG_LEVEL': 'debug',
            'DEBUG': True
        }
        atatus = Atatus(app)
        
        print(f"✓ Atatus configured - App: {app_name}")
        return True
    except Exception as e:
        print(f"⚠ Atatus setup failed: {e}")
        return False



def initialize_observability(app):
    """Initialize all observability platforms"""
    print("\n" + "="*60)
    print("Initializing Observability Platforms")
    print("="*60)
    
    # Always set up OpenTelemetry (required)
    tracer_provider = setup_opentelemetry()
    
    # Optional integrations
    datadog_enabled = setup_datadog()
    atatus_enabled = setup_atatus(app)
    
    print("="*60)
    print(f"Observability Status:")
    print(f"  - OpenTelemetry: ✓ Enabled (Jaeger UI: http://localhost:16686)")
    print(f"  - Datadog: {'✓ Enabled' if datadog_enabled else '✗ Disabled'}")
    print(f"  - Atatus: {'✓ Enabled' if atatus_enabled else '✗ Disabled'}")
    print("="*60 + "\n")
    
    return {
        'opentelemetry': tracer_provider,
        'datadog': datadog_enabled,
        'atatus': atatus_enabled
    }


def get_tracer():
    """Get OpenTelemetry tracer for manual instrumentation"""
    return trace.get_tracer(__name__)
