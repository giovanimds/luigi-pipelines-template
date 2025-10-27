import hashlib
import logging
import unicodedata

logger = logging.getLogger("luigi-interface")


def compute_file_hash(content):
    """Calcula o hash do conteúdo para unicidade. Aceita str ou bytes."""
    try:
        if isinstance(content, str):
            hash_input = content.encode("utf-8")
        elif isinstance(content, bytes):
            hash_input = content
        else:
            raise ValueError("Content must be str or bytes")
        return hashlib.sha256(hash_input).hexdigest()[:8]
    except Exception as e:
        logger.error(f"Erro ao calcular hash: {e}")
        return "error"


def _normalize_title(s: str) -> str:
    """Normalize sheet titles for robust comparison: remove accents, upper, collapse separators."""
    if s is None:
        return ""
    # Remove accents
    nfkd = unicodedata.normalize("NFD", s)
    s_no_accents = "".join(c for c in nfkd if not unicodedata.combining(c))
    # Uppercase and standardize separators
    s_up = s_no_accents.upper()
    for ch in [" ", "-", ".", "__"]:
        s_up = s_up.replace(ch, "_")
    while "__" in s_up:
        s_up = s_up.replace("__", "_")
    return s_up.strip("_")
