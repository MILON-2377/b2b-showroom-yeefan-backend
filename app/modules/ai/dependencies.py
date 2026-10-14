from fastapi import Depends

from app.core.contracts.ai.service import AbstractAIService
from app.core.contracts.services.catalog import AbstractCatalogService
from app.core.contracts.services.collection import AbstractCollectionService
from app.core.contracts.services.company_knowledge import (
    AbstractCompanyKnowledgeService,
)
from app.core.contracts.services.product import AbstractProductService
from app.modules.ai.providers.ollama import OllamaProvider
from app.modules.ai.services.ai_service import AIService
from app.modules.catalogs.dependencies import get_catalog_service
from app.modules.collections.dependencies import get_collection_service
from app.modules.company_knowledge.dependencies import get_company_knowledge_service
from app.modules.products.dependencies import get_product_service


def get_ai_service(
    product_service: AbstractProductService = Depends(get_product_service),
    collection_service: AbstractCollectionService = Depends(get_collection_service),
    catalog_service: AbstractCatalogService = Depends(get_catalog_service),
    company_knowledge_service: AbstractCompanyKnowledgeService = Depends(
        get_company_knowledge_service
    ),
) -> AbstractAIService:
    return AIService(
        provider=OllamaProvider(),
        product_service=product_service,
        collection_service=collection_service,
        catalog_service=catalog_service,
        company_knowledge_service=company_knowledge_service,
    )
