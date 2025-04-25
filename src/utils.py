import os
import tempfile


def setup_telemetry():
    from openinference.instrumentation.smolagents import SmolagentsInstrumentor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor

    # Create a TracerProvider for OpenTelemetry
    trace_provider = TracerProvider()

    # Add a SimpleSpanProcessor with the OTLPSpanExporter to send traces
    trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))

    # Set the global default tracer provider
    from opentelemetry import trace

    trace.set_tracer_provider(trace_provider)

    # Instrument smolagents with the configured provider
    SmolagentsInstrumentor().instrument(tracer_provider=trace_provider)


def save_temp_file(content, task_id):
    """
    Save a task file to a temporary location
    """
    if not content:
        return None

    # Create a temporary file
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, f"hf_gaia_task_{task_id}.txt")

    with open(file_path, "w") as f:
        f.write(content)
    
    return file_path
