from asgi_correlation_id import correlation_id
from fastapi import Request
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import Resource, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def configure_tracer(service_name: str, host: str, port: int) -> None:
    trace.set_tracer_provider(TracerProvider(resource=Resource(attributes={"service.name": service_name})))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=host,
                agent_port=port,
            ),
        ),
    )


def get_tracer() -> trace.Tracer:
    return trace.get_tracer(__name__)


tracer = get_tracer()


async def jaeger_middleware(request: Request, call_next):
    with tracer.start_span(str(correlation_id.get())) as span:
        span.set_attribute("http.request_id", str(correlation_id.get()))
        response = await call_next(request)
        return response
