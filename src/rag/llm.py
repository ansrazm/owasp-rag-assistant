import httpx

from . import config


class LLMNotConfigured(RuntimeError):
    pass


def generate(messages: list[dict], temperature: float = 0.2) -> str:
    """Call OpenRouter's OpenAI-compatible chat completions endpoint."""
    if not config.OPENROUTER_API_KEY:
        raise LLMNotConfigured("OPENROUTER_API_KEY is not set")
    r = httpx.post(
        config.OPENROUTER_URL,
        headers={"Authorization": f"Bearer {config.OPENROUTER_API_KEY}"},
        json={
            "model": config.OPENROUTER_MODEL,
            "messages": messages,
            "temperature": temperature,
            # reasoning models spend tokens on thinking first; leave room for the answer
            "max_tokens": 1500,
        },
        timeout=120,
    )
    if r.status_code >= 400:
        # surface OpenRouter's own error message instead of a bare status code
        raise httpx.HTTPError(f"{r.status_code} model={config.OPENROUTER_MODEL}: {r.text[:300]}")
    content = r.json()["choices"][0]["message"].get("content") or ""
    return content.strip()
