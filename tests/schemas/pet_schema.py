PET_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "category": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"}
            },
            "additionalProperties": False
        },
        "name": {"type": "string"},
        "photoUrls": {
            "type": "array",
            "items": {"type": "string"}
        },
        "tags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"}
                }
            }
        },
        "status": {
            "type": "string",
            "enum": ["available", "pending", "sold"]
        }
    },
    "required": ["id", "name", "status"],
    "additionalProperties": False
}
