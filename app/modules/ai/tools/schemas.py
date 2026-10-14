from typing import Any


def search_products_tool_schema() -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": (
                "Search published bridal products. "
                "Use this when the customer asks to find products, "
                "searches by product name, product code, or keyword."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "search": {
                        "type": "string",
                        "description": (
                            "Keyword to search for in product name, "
                            "description, or product code."
                        ),
                    },
                    "page": {
                        "type": "integer",
                        "minimum": 1,
                        "default": 1,
                    },
                    "page_size": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 20,
                        "default": 10,
                    },
                },
                "required": [],
                "additionalProperties": False,
            },
        },
    }


def get_product_tool_schema() -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": "get_product",
            "description": (
                "Get detailed information about a specific published bridal product."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "UUID of the product.",
                    },
                },
                "required": ["product_id"],
                "additionalProperties": False,
            },
        },
    }


def search_collections_tool_schema() -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": "search_collections",
            "description": (
                "Search published bridal collections by keyword. "
                "Use this when the customer asks about collections "
                "or wants to find a particular collection."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "search": {
                        "type": "string",
                        "description": "Keyword to search for in collections.",
                    },
                    "page": {
                        "type": "integer",
                        "minimum": 1,
                        "default": 1,
                    },
                    "page_size": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 20,
                        "default": 10,
                    },
                },
                "required": [],
                "additionalProperties": False,
            },
        },
    }


def search_catalogs_tool_schema() -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": "search_catalogs",
            "description": (
                "Search published bridal catalogs. "
                "Catalogs are PDF files. "
                "Use this when the customer asks for catalogs, "
                "lookbooks, or downloadable collection catalogs."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "search": {
                        "type": "string",
                        "description": (
                            "Keyword to search for in catalog title or description."
                        ),
                    },
                    "page": {
                        "type": "integer",
                        "minimum": 1,
                        "default": 1,
                    },
                    "page_size": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 20,
                        "default": 10,
                    },
                },
                "required": [],
                "additionalProperties": False,
            },
        },
    }


def search_company_knowledge_tool_schema() -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": "search_company_knowledge",
            "description": (
                "Search published YIFAN BRIDAL company knowledge, including "
                "MOQ, wholesale terms, sample policies, customization, "
                "production lead times, shipping terms, and company policies. "
                "Use this when answering company-related questions that "
                "cannot be answered reliably from product, collection, "
                "or catalog data."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "The company information the customer is asking about, "
                            "such as custom OEM MOQ or wholesale discounts."
                        ),
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 10,
                        "default": 5,
                    },
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    }


def get_ai_tools() -> list[dict[str, Any]]:
    return [
        search_products_tool_schema(),
        get_product_tool_schema(),
        search_collections_tool_schema(),
        search_catalogs_tool_schema(),
        search_company_knowledge_tool_schema(),
    ]
