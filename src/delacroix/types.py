"""Artwork type mappings for filtering."""

from __future__ import annotations

from typing import Dict, List

# Common artwork types that users can filter by
ARTWORK_TYPES = {
    "painting": ["painting", "paintings"],
    "drawing": ["drawing", "drawings"],
    "photograph": ["photograph", "photographs", "photography"],
    "print": ["print", "prints", "printmaking"],
    "sculpture": ["sculpture", "sculptures", "statue", "statues", "statuette"],
    "textile": ["textile", "textiles", "tapestry", "fabric"],
    "ceramic": ["ceramic", "ceramics", "pottery", "porcelain"],
    "furniture": ["furniture", "chair", "table", "cabinet"],
    "jewelry": ["jewelry", "jewellery", "necklace", "ring", "bracelet"],
    "metalwork": ["metalwork", "metal", "bronze", "silver", "gold"],
    "glass": ["glass", "glassware"],
    "manuscript": ["manuscript", "manuscripts", "illuminated"],
    "book": ["book", "books", "album"],
}

# Platform-specific type mappings
PLATFORM_TYPE_FIELDS = {
    "met": {
        "field_names": ["classification", "objectName", "medium"],
        "available_types": [
            "painting",
            "drawing",
            "photograph",
            "print",
            "sculpture",
            "textile",
            "ceramic",
            "furniture",
            "jewelry",
            "metalwork",
            "glass",
            "manuscript",
            "book",
        ],
    },
    "nga": {
        "field_names": ["classification", "medium"],
        "available_types": [
            "painting",
            "drawing",
            "photograph",
            "print",
            "sculpture",
        ],
    },
    "louvre": {
        "field_names": ["objectType", "category"],
        "available_types": [
            "painting",
            "drawing",
            "sculpture",
            "ceramic",
            "furniture",
            "jewelry",
            "textile",
        ],
    },
}


def normalize_type(type_str: str) -> str:
    """Normalize a type string to a canonical form."""
    type_lower = type_str.lower().strip()
    for canonical, variants in ARTWORK_TYPES.items():
        if type_lower in variants or type_lower == canonical:
            return canonical
    return type_lower


def get_type_keywords(type_filter: str) -> List[str]:
    """Get all keyword variants for a given type filter."""
    type_lower = type_filter.lower().strip()
    for canonical, variants in ARTWORK_TYPES.items():
        if type_lower in variants or type_lower == canonical:
            return variants
    return [type_lower]


def list_available_types(platform: str = None) -> List[str]:
    """List available artwork types for a platform or all types."""
    if platform and platform in PLATFORM_TYPE_FIELDS:
        return PLATFORM_TYPE_FIELDS[platform]["available_types"]
    return list(ARTWORK_TYPES.keys())
