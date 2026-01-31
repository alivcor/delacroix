from __future__ import annotations

from typing import Dict, Type

from .base import BasePlatform
from .chicago import ChicagoPlatform
from .louvre import LouvrePlatform
from .met import MetMuseumPlatform
from .nga import NGAPlatform
from .rijksmuseum import RijksmuseumPlatform


PLATFORM_REGISTRY: Dict[str, Type[BasePlatform]] = {
    MetMuseumPlatform.name: MetMuseumPlatform,
    NGAPlatform.name: NGAPlatform,
    LouvrePlatform.name: LouvrePlatform,
    RijksmuseumPlatform.name: RijksmuseumPlatform,
    ChicagoPlatform.name: ChicagoPlatform,
}


def get_platform(name: str) -> BasePlatform:
    if name not in PLATFORM_REGISTRY:
        available = ", ".join(sorted(PLATFORM_REGISTRY))
        raise KeyError(f"Unknown platform '{name}'. Available: {available}")
    return PLATFORM_REGISTRY[name]()
