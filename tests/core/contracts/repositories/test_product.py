import inspect
from abc import ABC

import pytest

from app.core.contracts.repositories.product import AbstractProductRepository
from app.modules.products.query import ProductListQuery, ProductListResult


def test_product_repository_is_abstract():
    assert issubclass(AbstractProductRepository, ABC)


def test_product_repository_cannot_be_instantiated():
    with pytest.raises(TypeError):
        AbstractProductRepository()


def test_product_repository_list_contract():
    method = AbstractProductRepository.list

    signature = inspect.signature(method)

    assert "query" in signature.parameters

    query_parameter = signature.parameters["query"]

    assert query_parameter.annotation is ProductListQuery
    assert signature.return_annotation is ProductListResult
