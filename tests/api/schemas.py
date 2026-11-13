PRODUCT = {
    "type": "object",
    "required": ["id", "name", "price", "in_stock", "category", "brand"],
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string", "minLength": 1},
        "description": {"type": "string"},
        "price": {"type": "number", "exclusiveMinimum": 0},
        "in_stock": {"type": "boolean"},
        "is_rental": {"type": "boolean"},
        "category": {"type": "object", "required": ["id", "name"]},
        "brand": {"type": "object", "required": ["id", "name"]},
    },
}

PRODUCT_PAGE = {
    "type": "object",
    "required": ["current_page", "data", "last_page", "per_page", "total"],
    "properties": {
        "current_page": {"type": "integer"},
        "last_page": {"type": "integer"},
        "per_page": {"type": "integer"},
        "total": {"type": "integer"},
        "data": {"type": "array", "items": PRODUCT},
    },
}

TOKEN = {
    "type": "object",
    "required": ["access_token", "token_type", "expires_in"],
    "properties": {
        "access_token": {"type": "string", "minLength": 20},
        "token_type": {"type": "string"},
        "expires_in": {"type": "integer"},
    },
}
