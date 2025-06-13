# ── tracing_bootstrap.py  (可独立成文件，最先 import) ─────────────
import os
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.flask import FlaskInstrumentor

project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({"service.name": "scorius-chatbot"}))
)
span_processor = BatchSpanProcessor(CloudTraceSpanExporter(project_id=project_id))
trace.get_tracer_provider().add_span_processor(span_processor)

# 自动打点第三方库
RequestsInstrumentor().instrument()
FlaskInstrumentor().instrument()   # ❗️不传入 app，让它延迟补丁
# ────────────────────────────────────────────────────────────────
