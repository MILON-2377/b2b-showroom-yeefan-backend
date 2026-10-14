from unittest.mock import Mock
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from app.modules.products.dependencies import get_product_service
from app.shared.exceptions import ProductNotFoundError


class FakeProductService:
    async def get_by_id(self, product_id):
        raise ProductNotFoundError(product_id)


def test_get_product_returns_404_when_not_found():
    app.dependency_overrides[get_product_service] = lambda: FakeProductService()

    try:
        client = TestClient(app)

        product_id = uuid4()

        response = client.get(f"/products/{product_id}")

        assert response.status_code == 404

        assert response.json() == {
            "error": {
                "code": "PRODUCT_NOT_FOUND",
                "message": "Product not found",
                "details": None,
            }
        }

    finally:
        app.dependency_overrides.clear()


def test_get_product():
    product_id = uuid4()
    brand_id = uuid4()
    collection_id = uuid4()
    category_id = uuid4()

    product = Mock()
    product.id = product_id
    product.brand_id = brand_id
    product.collection_id = collection_id
    product.category_id = category_id
    product.product_code = "K5368"
    product.name = "Test Dress"
    product.slug = "test-dress"
    product.description = "Test description"
    product.status.value = "DRAFT"
    product.published_at = None

    class FakeProductService:
        async def get_by_id(self, requested_product_id):
            assert requested_product_id == product_id
            return product

    app.dependency_overrides[get_product_service] = lambda: FakeProductService()

    try:
        client = TestClient(app)

        response = client.get(f"/products/{product_id}")

        assert response.status_code == 200

        assert response.json() == {
            "id": str(product_id),
            "brand_id": str(brand_id),
            "collection_id": str(collection_id),
            "category_id": str(category_id),
            "product_code": "K5368",
            "name": "Test Dress",
            "slug": "test-dress",
            "description": "Test description",
            "status": "DRAFT",
            "published_at": None,
        }

    finally:
        app.dependency_overrides.clear()


def test_create_product():
    expected_brand_id = uuid4()
    expected_collection_id = uuid4()
    expected_category_id = uuid4()
    product_id = uuid4()

    product = Mock()
    product.id = product_id
    product.brand_id = expected_brand_id
    product.collection_id = expected_collection_id
    product.category_id = expected_category_id
    product.product_code = "K5368"
    product.name = "Test Dress"
    product.slug = "test-dress"
    product.description = "Test description"
    product.status.value = "DRAFT"
    product.published_at = None

    class FakeProductService:
        async def create(
            self,
            *,
            brand_id,
            collection_id,
            category_id,
            product_code,
            name,
            description,
        ):
            assert brand_id == expected_brand_id
            assert collection_id == expected_collection_id
            assert category_id == expected_category_id
            assert product_code == "K5368"
            assert name == "Test Dress"
            assert description == "Test description"

            return product

    app.dependency_overrides[get_product_service] = lambda: FakeProductService()

    try:
        client = TestClient(app)

        response = client.post(
            "/products",
            json={
                "brand_id": str(expected_brand_id),
                "collection_id": str(expected_collection_id),
                "category_id": str(expected_category_id),
                "product_code": "K5368",
                "name": "Test Dress",
                "description": "Test description",
            },
        )

        assert response.status_code == 201

        assert response.json() == {
            "id": str(product_id),
            "brand_id": str(expected_brand_id),
            "collection_id": str(expected_collection_id),
            "category_id": str(expected_category_id),
            "product_code": "K5368",
            "name": "Test Dress",
            "slug": "test-dress",
            "description": "Test description",
            "status": "DRAFT",
            "published_at": None,
        }

    finally:
        app.dependency_overrides.clear()


def test_create_product_rejects_missing_brand_id():
    client = TestClient(app)

    response = client.post(
        "/products",
        json={
            "collection_id": str(uuid4()),
            "category_id": str(uuid4()),
            "product_code": "K5368",
            "name": "Test Dress",
        },
    )

    assert response.status_code == 422


def test_create_product_rejects_invalid_brand_id():
    client = TestClient(app)

    response = client.post(
        "/products",
        json={
            "brand_id": "not-a-uuid",
            "collection_id": str(uuid4()),
            "category_id": str(uuid4()),
            "product_code": "K5368",
            "name": "Test Dress",
        },
    )

    assert response.status_code == 422


def test_create_product_rejects_empty_product_code():
    client = TestClient(app)

    response = client.post(
        "/products",
        json={
            "brand_id": str(uuid4()),
            "collection_id": str(uuid4()),
            "category_id": str(uuid4()),
            "product_code": "",
            "name": "Test Dress",
        },
    )

    assert response.status_code == 422


def test_create_product_rejects_empty_name():
    client = TestClient(app)

    response = client.post(
        "/products",
        json={
            "brand_id": str(uuid4()),
            "collection_id": str(uuid4()),
            "category_id": str(uuid4()),
            "product_code": "K5368",
            "name": "",
        },
    )

    assert response.status_code == 422


def test_create_product_rejects_product_code_over_100_characters():
    client = TestClient(app)

    response = client.post(
        "/products",
        json={
            "brand_id": str(uuid4()),
            "collection_id": str(uuid4()),
            "category_id": str(uuid4()),
            "product_code": "K" * 101,
            "name": "Test Dress",
        },
    )

    assert response.status_code == 422
