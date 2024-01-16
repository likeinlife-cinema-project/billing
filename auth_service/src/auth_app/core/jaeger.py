from asgi_correlation_id import correlation_id
from fastapi import FastAPI, Request
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import Resource, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def configure_tracer(app: FastAPI, service_name: str, host: str, port: int) -> None:
    tracer = TracerProvider(resource=Resource(attributes={"service.name": service_name}))
    trace.set_tracer_provider(tracer)

    tracer.add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=host,
                agent_port=port,
            ),
        ),
    )

    FastAPIInstrumentor.instrument_app(app=app, tracer_provider=tracer)


def get_tracer() -> trace.Tracer:
    return trace.get_tracer(__name__)


async def jaeger_middleware(request: Request, call_next):
    with get_tracer().start_as_current_span(request.url.path) as span:
        span.set_attribute("http.request_id", str(correlation_id.get()))
        response = await call_next(request)
        return response
