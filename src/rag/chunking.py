def chunk_text(text: str, size: int = 500, overlap: int = 80) -> list[str]:
    """Split text into chunks of roughly `size` characters, packing whole paragraphs
    and carrying `overlap` characters of context into the next chunk."""
    if size <= overlap:
        raise ValueError("size must be greater than overlap")
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    cur = ""
    for p in paragraphs:
        while len(p) > size:  # very long paragraph: hard split with overlap
            head, p = p[:size], p[size - overlap:]
            if cur:
                chunks.append(cur)
                cur = ""
            chunks.append(head)
        if len(cur) + len(p) + 2 <= size:
            cur = f"{cur}\n\n{p}" if cur else p
        else:
            tail = cur[-overlap:] if cur and overlap else ""
            if cur:
                chunks.append(cur)
            cur = f"{tail} {p}".strip() if tail else p
    if cur:
        chunks.append(cur)
    return chunks
