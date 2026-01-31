from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from PIL import Image

from .platforms.base import Artwork, BasePlatform


@dataclass(frozen=True)
class HarvestResult:
    platform: str
    downloaded: int
    skipped_vertical: int
    skipped_missing_image: int
    failed: int


class Harvester:
    def __init__(self, platform: BasePlatform, *, aspect_ratio: float = 16 / 9) -> None:
        if aspect_ratio <= 0:
            raise ValueError("aspect_ratio must be > 0")
        self.platform = platform
        self.aspect_ratio = aspect_ratio

    def harvest(
        self,
        output_dir: Path,
        *,
        max_items: int = 50,
        tags: Optional[list[str]] = None,
        types: Optional[list[str]] = None,
    ) -> HarvestResult:
        output_dir.mkdir(parents=True, exist_ok=True)
        downloaded = 0
        skipped_vertical = 0
        skipped_missing_image = 0
        failed = 0

        # Keep fetching until we get max_items successful downloads
        for artwork in self.platform.list_artworks(tags=tags, types=types):
            if downloaded >= max_items:
                break
                
            if not artwork.image_url:
                skipped_missing_image += 1
                continue
            try:
                image_path = self.platform.download_image(artwork, output_dir)
                if image_path is None:
                    skipped_missing_image += 1
                    continue
                if not self._is_landscape(image_path):
                    skipped_vertical += 1
                    image_path.unlink(missing_ok=True)
                    # Also delete the JSON metadata file if it exists
                    json_path = image_path.with_suffix('.json')
                    json_path.unlink(missing_ok=True)
                    continue
                self._crop_to_aspect(image_path, self.aspect_ratio)
                downloaded += 1
            except Exception:
                failed += 1

        return HarvestResult(
            platform=self.platform.name,
            downloaded=downloaded,
            skipped_vertical=skipped_vertical,
            skipped_missing_image=skipped_missing_image,
            failed=failed,
        )

    @staticmethod
    def _limited(items: Iterable[Artwork], max_items: int) -> Iterable[Artwork]:
        count = 0
        for item in items:
            if count >= max_items:
                break
            yield item
            count += 1

    @staticmethod
    def _is_landscape(image_path: Path) -> bool:
        with Image.open(image_path) as img:
            width, height = img.size
        return width >= height

    @staticmethod
    def _crop_to_aspect(image_path: Path, aspect_ratio: float) -> None:
        with Image.open(image_path) as img:
            width, height = img.size
            target_width = width
            target_height = int(width / aspect_ratio)
            if target_height > height:
                target_height = height
                target_width = int(height * aspect_ratio)
            left = (width - target_width) // 2
            upper = (height - target_height) // 2
            right = left + target_width
            lower = upper + target_height
            cropped = img.crop((left, upper, right, lower))
            cropped.save(image_path, quality=95)
