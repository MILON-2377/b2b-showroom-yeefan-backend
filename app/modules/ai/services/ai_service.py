import json
import logging
from collections.abc import AsyncIterator
from typing import Any

from app.core.contracts.ai.provider import AbstractAIProvider
from app.core.contracts.ai.service import AbstractAIService
from app.core.contracts.services.catalog import AbstractCatalogService
from app.core.contracts.services.collection import AbstractCollectionService
from app.core.contracts.services.company_knowledge import (
    AbstractCompanyKnowledgeService,
)
from app.core.contracts.services.product import AbstractProductService
from app.modules.ai.dtos import AIChatDTO, AIResponseDTO
from app.modules.ai.tools.catalog import CatalogTool
from app.modules.ai.tools.collection import CollectionTool
from app.modules.ai.tools.company_knowledge import CompanyKnowledgeTool
from app.modules.ai.tools.product_detail import ProductDetailTool
from app.modules.ai.tools.product_search import ProductSearchTool
from app.modules.ai.tools.schemas import get_ai_tools

logger = logging.getLogger(__name__)


class AIService(AbstractAIService):
    MAX_TOOL_ROUNDS = 5

    SYSTEM_PROMPT = """
        You are the YIFAN BRIDAL customer assistant.

        YIFAN BRIDAL is a B2B bridal fashion brand serving global clients.

        Rules:
        - Be professional, natural, helpful, and concise.
        - Respond in the language used by the customer.
        - Support Chinese, English, and other languages when possible.
        - Answer directly. Do not describe your internal tools, backend, database, or search process.
        - Use backend tools whenever factual YIFAN BRIDAL information is needed.
        - Use search_products for product-related questions.
        - Use get_product for detailed information about a specific product.
        - Use search_collections for collection-related questions.
        - Use search_catalogs for catalog-related questions.
        - Use search_company_knowledge for company policies, MOQ, wholesale terms,
        customization, manufacturing, production lead times, sample terms,
        shipping terms, certifications, fabrics, materials, and other company information.
        - Treat backend tool results as the source of truth.
        - Never invent products, availability, prices, policies, MOQ, lead times,
        certifications, fabrics, materials, or other company facts.
        - If the requested information is not available in the backend, simply say
        that the information is not currently available and, when appropriate,
        suggest contacting YIFAN BRIDAL.
        - Do not say that information is "missing from the backend", "not listed in
        our database", or similar technical wording.
        - Do not provide unnecessary disclaimers or repeat limitations.
        - Do not speculate or make assumptions from missing information.
        - When the backend provides relevant information, answer using that information
        directly and confidently.
        - Combine information from multiple tool results when necessary.
        - For catalogs, provide the returned PDF URL when relevant.
        - Never claim that an inquiry, quotation, or order has been submitted unless
        the system explicitly confirms it.
        - Keep answers focused on the customer's question.
        """

    def __init__(
        self,
        *,
        provider: AbstractAIProvider,
        product_service: AbstractProductService,
        collection_service: AbstractCollectionService,
        catalog_service: AbstractCatalogService,
        company_knowledge_service: AbstractCompanyKnowledgeService,
    ) -> None:
        self.provider = provider

        self.tools = {
            "search_products": ProductSearchTool(product_service),
            "get_product": ProductDetailTool(product_service),
            "search_collections": CollectionTool(collection_service),
            "search_catalogs": CatalogTool(catalog_service),
            "search_company_knowledge": CompanyKnowledgeTool(company_knowledge_service),
        }

    async def chat(
        self,
        data: AIChatDTO,
    ) -> AIResponseDTO:
        messages = self._build_messages(data)

        for _ in range(self.MAX_TOOL_ROUNDS):
            response = await self.provider.generate(
                messages=messages,
                tools=get_ai_tools(),
            )

            logger.info(
                "AI response: content=%s, tool_calls=%s",
                response.content,
                [
                    {
                        "id": call.id,
                        "name": call.name,
                        "arguments": call.arguments,
                    }
                    for call in response.tool_calls
                ],
            )

            if not response.tool_calls:
                return response

            self._append_assistant_tool_calls(
                messages=messages,
                response=response,
            )

            for tool_call in response.tool_calls:
                result = await self._execute_tool(
                    name=tool_call.name,
                    arguments=tool_call.arguments,
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(
                            result,
                            ensure_ascii=False,
                        ),
                    }
                )

        return AIResponseDTO(
            content=(
                "I couldn't complete that request right now. "
                "Please try again or contact YIFAN BRIDAL."
            ),
            tool_calls=[],
        )

    async def chat_stream(
        self,
        data: AIChatDTO,
    ) -> AsyncIterator[str]:
        messages = self._build_messages(data)

        for _ in range(self.MAX_TOOL_ROUNDS):
            response = await self.provider.generate(
                messages=messages,
                tools=get_ai_tools(),
            )

            if not response.tool_calls:
                break

            self._append_assistant_tool_calls(
                messages=messages,
                response=response,
            )

            for tool_call in response.tool_calls:
                result = await self._execute_tool(
                    name=tool_call.name,
                    arguments=tool_call.arguments,
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(
                            result,
                            ensure_ascii=False,
                        ),
                    }
                )
        else:
            yield (
                "I couldn't complete that request right now. "
                "Please try again or contact YIFAN BRIDAL."
            )
            return

        async for chunk in self.provider.generate_stream(
            messages=messages,
        ):
            yield chunk

    def _build_messages(
        self,
        data: AIChatDTO,
    ) -> list[dict[str, Any]]:
        return [
            {
                "role": "system",
                "content": self.SYSTEM_PROMPT,
            },
            *[
                {
                    "role": message.role,
                    "content": message.content,
                }
                for message in data.messages
            ],
        ]

    @staticmethod
    def _append_assistant_tool_calls(
        *,
        messages: list[dict[str, Any]],
        response: AIResponseDTO,
    ) -> None:
        messages.append(
            {
                "role": "assistant",
                "content": response.content,
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.name,
                            "arguments": json.dumps(
                                tool_call.arguments,
                                ensure_ascii=False,
                            ),
                        },
                    }
                    for tool_call in response.tool_calls
                ],
            }
        )

    async def _execute_tool(
        self,
        *,
        name: str,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        logger.info("Executing AI tool: %s", name)

        tool = self.tools.get(name)

        if tool is None:
            logger.warning("AI tool not found: %s", name)
            return {
                "success": False,
                "error": "The requested tool is unavailable.",
            }

        try:
            result = await tool.execute(arguments)

            logger.info("AI tool completed successfully: %s", name)

            return {
                "success": True,
                "data": result,
            }

        except (ValueError, KeyError, TypeError):
            logger.exception(
                "Invalid arguments while executing AI tool: %s",
                name,
            )
            return {
                "success": False,
                "error": "The tool arguments are invalid.",
            }

        except Exception:
            logger.exception(
                "Unexpected error while executing AI tool: %s",
                name,
            )
            return {
                "success": False,
                "error": ("The requested information is temporarily unavailable."),
            }
