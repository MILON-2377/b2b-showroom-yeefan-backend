import secrets
import string

from app.shared.utils.slug import create_slug


def create_product_code(product_name: str) -> str:
    slug = create_slug(product_name)

    if not slug:
        prefix = "PRODUCT"
    else:
        prefix = slug.replace("-", "")[:8].upper()

    suffix = "".join(
        secrets.choice(string.ascii_uppercase + string.digits) for _ in range(4)
    )

    return f"{prefix}-{suffix}"
