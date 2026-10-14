from app.core.errors.base import NotFoundError


class CompanyKnowledgeNotFoundError(NotFoundError):
    def __init__(self) -> None:
        super().__init__("Company knowledge not found")
