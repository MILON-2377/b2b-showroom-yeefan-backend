from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.exception_handlers import app_error_handler
from app.shared.exceptions import AppError


def test_app_error_handler_is_registered():
    app = FastAPI()

    app.add_exception_handler(
        AppError,
        app_error_handler,
    )

    @app.get("/test-error")
    async def test_error():
        from app.shared.exceptions import ProductNotFoundError

        raise ProductNotFoundError("product-id")

    client = TestClient(app)

    response = client.get("/test-error")

    assert response.status_code == 404

    assert response.json() == {
        "error": {
            "code": "PRODUCT_NOT_FOUND",
            "message": "Product not found",
            "details": None,
        }
    }
