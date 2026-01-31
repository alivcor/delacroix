from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


@dataclass(frozen=True)
class Artwork:
    id: str
    title: str
    artist: str
    image_url: Optional[str]
    date: Optional[str] = None
    culture: Optional[str] = None
    classification: Optional[str] = None


class BasePlatform:
    name: str = "base"

    def list_artworks(self, tags: Optional[list[str]] = None, types: Optional[list[str]] = None) -> Iterable[Artwork]:
        raise NotImplementedError

    def download_image(self, artwork: Artwork, output_dir: Path) -> Optional[Path]:
        raise NotImplementedError
