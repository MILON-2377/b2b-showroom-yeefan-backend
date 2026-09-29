import pytest

from app.shared.utils.slug import create_slug


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Spring Summer 2024", "spring-summer-2024"),
        ("Pearl Coast", "pearl-coast"),
        ("  Modern & Luxury  ", "modern-luxury"),
        ("Holy Girl!", "holy-girl"),
        ("Multiple   Spaces", "multiple-spaces"),
        ("Already-a-slug", "already-a-slug"),
        ("Special @#$ Characters", "special-characters"),
        ("UPPER CASE NAME", "upper-case-name"),
    ],
)
def test_create_slug(value: str, expected: str) -> None:
    assert create_slug(value) == expected
