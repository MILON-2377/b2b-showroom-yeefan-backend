from uuid import UUID, uuid4


def generate_storage_key(
    *,
    namespace: str,
    entity_id: UUID,
) -> str:
    return f"{namespace}/{entity_id}/{uuid4()}"
