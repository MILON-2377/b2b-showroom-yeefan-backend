from uuid import UUID, uuid4


def generate_storage_key(
    *,
    namespace: str,
    entity_id: UUID,
    filename: str,
) -> str:
    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    unique_id = uuid4()

    key = f"{namespace}/{entity_id}/{unique_id}"

    if extension:
        key += f".{extension}"

    return key
