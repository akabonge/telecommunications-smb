from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from openai import OpenAI
from pinecone import Pinecone


SYSTEM_PROMPT = (
    "You are a cybersecurity assistant for small and medium-sized telecommunications businesses. "
    "Be practical, specific, and calm. "
    "Focus on cybersecurity controls, vendor risk, supply chain risk, access control, resilience, and incident response. "
    "Never invent requirements, laws, or standards. "
    "When evidence is insufficient, say so clearly and recommend a safe next step."
)

FT_PROMPT = (
    "Use the fine-tuned behavior for concise, operations-focused guidance. "
    "Keep recommendations realistic for small and medium-sized telecommunications organizations."
)

RAG_PROMPT = (
    "Use the supplied excerpts as evidence. "
    "Cite claims inline using [1], [2], and so on. "
    "Answer only from the evidence and do not speculate beyond it. "
    "If evidence is partial, say what is known and what is uncertain."
)


@dataclass(frozen=True)
class BotConfig:
    openai_api_key: str
    pinecone_api_key: str
    pinecone_index_host: str = ""
    pinecone_index: str = ""
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int | None = 1536
    chat_model: str = "gpt-4.1-mini"
    finetuned_model: str = ""
    min_source_score: float = 0.0


def _metadata_value(metadata: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        value = metadata.get(key)
        if value not in (None, ""):
            return value
    return default


def _openai_client(config: BotConfig) -> OpenAI:
    if not config.openai_api_key:
        raise RuntimeError("Missing OPENAI_API_KEY. Add it to Streamlit secrets.")
    return OpenAI(api_key=config.openai_api_key)


def _pinecone_index(config: BotConfig):
    if not config.pinecone_api_key:
        raise RuntimeError("Missing PINECONE_API_KEY. Add it to Streamlit secrets.")

    pc = Pinecone(api_key=config.pinecone_api_key)
    if config.pinecone_index_host:
        return pc.Index(host=config.pinecone_index_host)
    if config.pinecone_index:
        return pc.Index(config.pinecone_index)
    raise RuntimeError("Set PINECONE_INDEX_HOST or PINECONE_INDEX in Streamlit secrets.")


def _embed_text(client: OpenAI, config: BotConfig, text: str) -> list[float]:
    kwargs: dict[str, Any] = {
        "model": config.embedding_model,
        "input": [text],
    }
    if config.embedding_dimensions:
        kwargs["dimensions"] = config.embedding_dimensions
    response = client.embeddings.create(**kwargs)
    return response.data[0].embedding


def _retrieve(question: str, namespace: str, top_k: int, config: BotConfig) -> list[dict[str, Any]]:
    client = _openai_client(config)
    index = _pinecone_index(config)
    query_vector = _embed_text(client, config, question)

    result = index.query(
        vector=query_vector,
        top_k=max(top_k, 1),
        include_metadata=True,
        namespace=namespace,
    )
    matches = result.get("matches", []) if isinstance(result, dict) else getattr(result, "matches", []) or []

    records: list[dict[str, Any]] = []
    for match in matches:
        metadata = match.get("metadata", {}) if isinstance(match, dict) else getattr(match, "metadata", {}) or {}
        score = match.get("score") if isinstance(match, dict) else getattr(match, "score", None)
        score_value = float(score or 0.0)
        if score_value < config.min_source_score:
            continue
        allowed = metadata.get("allowed_for_answers")
        if allowed is False or str(allowed).lower() == "false":
            continue
        records.append({"score": score_value, "metadata": dict(metadata)})

    return records


def _format_context(results: list[dict[str, Any]]) -> str:
    blocks: list[str] = []
    for index, item in enumerate(results, start=1):
        metadata = item["metadata"]
        blocks.append(
            f"[{index}] title={_metadata_value(metadata, 'title', default='Untitled')} | "
            f"source_id={_metadata_value(metadata, 'source_id', 'source_key', 'source', 'location', default='unknown')} | "
            f"authority_level={_metadata_value(metadata, 'authority_level', default='unknown')} | "
            f"page={_metadata_value(metadata, 'page_start', 'page', default='n/a')}\n"
            f"content={_metadata_value(metadata, 'content', 'text', default='')}"
        )
    return "\n\n".join(blocks)


def _chat(client: OpenAI, model: str, messages: list[dict[str, str]]) -> str:
    response = client.responses.create(model=model, input=messages)
    return response.output_text.strip()


def _citations(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    citations: list[dict[str, Any]] = []
    for rank, item in enumerate(results, start=1):
        metadata = item["metadata"]
        page = _metadata_value(metadata, "page_start", "page")
        pages = str(page) if page not in (None, "") else "n/a"
        citations.append(
            {
                "rank": rank,
                "title": str(_metadata_value(metadata, "title", default="Untitled")),
                "source_id": str(_metadata_value(metadata, "source_id", "source_key", "source", "location", default="")),
                "section": str(_metadata_value(metadata, "section", "chunk_index", default="")),
                "pages": pages,
                "score": item["score"],
                "authority_level": _metadata_value(metadata, "authority_level"),
                "source": _metadata_value(metadata, "source", "location"),
            }
        )
    return citations


def answer_question(
    question: str,
    namespace: str,
    mode: str,
    top_k: int,
    config: BotConfig,
    model_override: str | None = None,
) -> dict[str, Any]:
    mode = (mode or "hybrid").lower()
    client = _openai_client(config)

    model = model_override or config.chat_model
    if mode in {"finetuned", "hybrid"}:
        model = model_override or config.finetuned_model or config.chat_model

    if mode == "base":
        answer = _chat(
            client,
            model,
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
        )
        return {"answer": answer, "model": model, "citations": [], "mode": mode}

    if mode == "finetuned":
        answer = _chat(
            client,
            model,
            [
                {"role": "system", "content": f"{SYSTEM_PROMPT} {FT_PROMPT}"},
                {"role": "user", "content": question},
            ],
        )
        return {"answer": answer, "model": model, "citations": [], "mode": mode}

    results = _retrieve(question, namespace, top_k, config)
    if not results:
        return {
            "answer": "I could not find enough trusted source material for that question in the current corpus.",
            "model": model,
            "citations": [],
            "mode": mode,
        }

    prompt = (
        f"Question:\n{question}\n\n"
        f"Indexed corpus excerpts:\n{_format_context(results)}\n\n"
        "Write a grounded answer with inline citations like [1] and [2]. "
        "Prefer practical recommendations a telecommunications SMB can act on."
    )
    system_prompt = f"{SYSTEM_PROMPT} {RAG_PROMPT}"
    if mode == "hybrid":
        system_prompt = f"{SYSTEM_PROMPT} {FT_PROMPT} {RAG_PROMPT}"

    answer = _chat(
        client,
        model,
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )
    return {"answer": answer, "model": model, "citations": _citations(results), "mode": mode}
