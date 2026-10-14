from app.shared.schemas import ErrorDetail, ErrorResponse


def test_error_detail():
    detail = ErrorDetail(
        code="PRODUCT_NOT_FOUND",
        message="Product not found",
    )

    assert detail.code == "PRODUCT_NOT_FOUND"
    assert detail.message == "Product not found"
    assert detail.details is None


def test_error_detail_with_details():
    detail = ErrorDetail(
        code="INVALID_PRODUCT",
        message="Product data is invalid",
        details={
            "field": "product_code",
            "reason": "Product code is required",
        },
    )

    assert detail.details == {
        "field": "product_code",
        "reason": "Product code is required",
    }


def test_error_response():
    response = ErrorResponse(
        error=ErrorDetail(
            code="PRODUCT_NOT_FOUND",
            message="Product not found",
        )
    )

    assert response.error.code == "PRODUCT_NOT_FOUND"
    assert response.error.message == "Product not found"
