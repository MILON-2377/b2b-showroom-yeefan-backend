from typing import Any

from app.core.contracts.services.company_knowledge import (
    AbstractCompanyKnowledgeService,
)


class CompanyKnowledgeTool:
    def __init__(
        self,
        company_knowledge_service: AbstractCompanyKnowledgeService,
    ) -> None:
        self.company_knowledge_service = company_knowledge_service

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        query = arguments.get("query", "").strip()
        limit = arguments.get("limit", 5)

        if not query:
            return {
                "success": False,
                "error": "A search query is required.",
            }

        items = await self.company_knowledge_service.search_published(
            query=query,
            limit=limit,
        )

        return {
            "success": True,
            "data": [
                {
                    "title": item.title,
                    "category": item.category,
                    "content": item.content,
                }
                for item in items
            ],
        }
