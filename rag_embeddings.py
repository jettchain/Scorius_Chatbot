# rag_embeddings.py
import time, google.generativeai as genai
from langchain_core.embeddings import Embeddings
from google.api_core import retry
from google.api_core.exceptions import TooManyRequests, ServiceUnavailable

EMBED_MODEL = "models/gemini-embedding-exp-03-07"

# ① 指数退避，用来防 429 / 503
retry_429 = retry.Retry(
    initial=1.0, maximum=60.0, multiplier=2.0,
    deadline=300.0, predicate=retry.if_exception_type(
        TooManyRequests, ServiceUnavailable),
    jitter=0.1,
)

class GeminiEmbeddings(Embeddings):
    def __init__(self, model=EMBED_MODEL, task_type="CLASSIFICATION"):
        self.model, self.task_type = model, task_type

    def embed_query(self, text: str):
        return retry_429(genai.embed_content)(
            model=self.model, content=text, task_type=self.task_type
        )["embedding"]

    def embed_documents(self, texts, **_):
        try:
            resp = retry_429(genai.batch_embed_content)(
                model=self.model,
                requests=[{"content": t, "task_type": self.task_type} for t in texts],
            ).embeddings
            return [e.values for e in resp]
        except Exception:
            # 回退：逐条
            return [self.embed_query(t) for t in texts]
