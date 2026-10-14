import re
import unicodedata
from uuid import uuid4


def slug_generator(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")

    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value)
    value = value.strip("-")

    unique_suffix = uuid4().hex[:8]

    if not value:
        return unique_suffix

    return f"{value}-{unique_suffix}"