import base64
import binascii
import json
from uuid import UUID

from app.modules.products.dtos import (
    ProductCursor,
    ProductSortBy,
    ProductSortOrder,
)
from app.modules.products.exceptions import InvalidProductCursorError


class ProductCursorCodec:
    @staticmethod
    def encode(cursor: ProductCursor) -> str:
        payload = {
            "sort_by": cursor.sort_by.value,
            "sort_order": cursor.sort_order.value,
            "value": cursor.value,
            "product_id": str(cursor.product_id),
        }

        raw = json.dumps(
            payload,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")

        return base64.urlsafe_b64encode(raw).decode("ascii")

    @staticmethod
    def decode(cursor: str) -> ProductCursor:
        try:
            raw = base64.urlsafe_b64decode(
                cursor.encode("ascii"),
            )

            payload = json.loads(
                raw.decode("utf-8"),
            )

            sort_by = ProductSortBy(
                payload["sort_by"],
            )

            sort_order = ProductSortOrder(
                payload["sort_order"],
            )

            value = payload["value"]
            product_id = UUID(
                payload["product_id"],
            )

        except (
            ValueError,
            TypeError,
            KeyError,
            UnicodeDecodeError,
            json.JSONDecodeError,
            binascii.Error,
        ) as exc:
            raise InvalidProductCursorError() from exc

        if not isinstance(value, str) or not value:
            raise InvalidProductCursorError()

        return ProductCursor(
            sort_by=sort_by,
            sort_order=sort_order,
            value=value,
            product_id=product_id,
        )
