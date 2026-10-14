from uuid import uuid4

from app.shared.exceptions import (
    AppError,
    ConflictError,
    NotFoundError,
    ProductNotFoundError,
    ValidationError,
)


def test_app_error_contains_message_and_code():
    error = AppError(
        "Something went wrong",
        code="SOMETHING_WRONG",
    )

    assert str(error) == "Something went wrong"
    assert error.message == "Something went wrong"
    assert error.code == "SOMETHING_WRONG"


def test_not_found_error_is_app_error():
    error = NotFoundError(
        "Resource not found",
        code="RESOURCE_NOT_FOUND",
    )

    assert isinstance(error, AppError)


def test_conflict_error_is_app_error():
    error = ConflictError(
        "Resource already exists",
        code="RESOURCE_EXISTS",
    )

    assert isinstance(error, AppError)


def test_validation_error_is_app_error():
    error = ValidationError(
        "Invalid value",
        code="INVALID_VALUE",
    )

    assert isinstance(error, AppError)


def test_product_not_found_error():
    product_id = uuid4()

    error = ProductNotFoundError(product_id)

    assert isinstance(error, NotFoundError)
    assert isinstance(error, AppError)
    assert error.code == "PRODUCT_NOT_FOUND"
    assert error.message == "Product not found"
    assert error.product_id == product_id


def test_not_found_error_has_404_status():
    error = NotFoundError(
        "Resource not found",
        code="RESOURCE_NOT_FOUND",
    )

    assert error.status_code == 404


def test_conflict_error_has_409_status():
    error = ConflictError(
        "Resource already exists",
        code="RESOURCE_ALREADY_EXISTS",
    )

    assert error.status_code == 409
