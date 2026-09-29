from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import Response

from app.core.storage.dependencies import get_object_storage
from app.core.storage.interface import AbstractObjectStorage

router = APIRouter(
    prefix="/local-storage",
    tags=["local-storage"],
)


@router.put(
    "/upload/{storage_key:path}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def upload_file(
    storage_key: str,
    request: Request,
    storage: AbstractObjectStorage = Depends(get_object_storage),
) -> Response:
    await storage.upload_object(
        storage_key=storage_key,
        data=request.stream(),
        mime_type=request.headers.get(
            "content-type",
            "application/octet-stream",
        ),
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
