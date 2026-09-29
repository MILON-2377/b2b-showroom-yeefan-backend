from dataclasses import dataclass


@dataclass(frozen=True)
class ObjectMetadata:
    storage_key: str
    mime_type: str
    size: int
