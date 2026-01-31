from __future__ import annotations

import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Iterable, Optional

import requests
from PIL import Image

from .base import Artwork, BasePlatform


class LouvrePlatform(BasePlatform):
    name = "louvre"

    def list_artworks(self, tags: Optional[list[str]] = None, types: Optional[list[str]] = None) -> Iterable[Artwork]:
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        index_url = "https://collections.louvre.fr/sitemap.xml"
        index_xml = requests.get(index_url, timeout=30).text
        index_root = ET.fromstring(index_xml)
        sitemap_urls = [loc.text for loc in index_root.findall("s:sitemap/s:loc", ns)]

        for sitemap_url in sitemap_urls:
            sitemap_xml = requests.get(sitemap_url, timeout=30).text
            sitemap_root = ET.fromstring(sitemap_xml)
            for loc in sitemap_root.findall("s:url/s:loc", ns):
                url = loc.text
                if not url or "/ark:/" not in url:
                    continue
                json_url = url + ".json"
                try:
                    data = requests.get(json_url, timeout=30).json()
                except Exception:
                    continue
                artwork = self._louvre_artwork_from_json(data)
                if artwork:
                    # Filter by tags if provided
                    if tags and not self._matches_tags(artwork, tags):
                        continue
                    # Filter by types if provided
                    if types and not self._matches_types(artwork, types):
                        continue
                    yield artwork
                time.sleep(0.1)

    def download_image(self, artwork: Artwork, output_dir: Path) -> Optional[Path]:
        if not artwork.image_url:
            return None
        
        filename = self._safe_filename(f"louvre-{artwork.id}-{artwork.title}") + ".jpg"
        destination = output_dir / filename
        
        response = requests.get(artwork.image_url, timeout=60)
        response.raise_for_status()
        destination.write_bytes(response.content)
        self._embed_metadata(destination, artwork.artist, artwork.title)
        
        # Save metadata to JSON
        import json
        from dataclasses import asdict
        json_file = output_dir / (self._safe_filename(f"louvre-{artwork.id}-{artwork.title}") + ".json")
        json_file.write_text(json.dumps(asdict(artwork), indent=2), encoding="utf-8")
        
        return destination

    def _louvre_artwork_from_json(self, data: Dict) -> Optional[Artwork]:
        images = data.get("image") or []
        if not isinstance(images, list) or not images:
            return None

        image_url = None
        for img in images:
            if not isinstance(img, dict):
                continue
            copyright_text = (img.get("copyright") or "").lower()
            if copyright_text and not self._looks_public_domain(copyright_text):
                continue
            image_url = img.get("urlImage")
            if image_url:
                break

        if not image_url:
            return None

        creator = data.get("creator") or []
        artist = self._louvre_artist(creator)
        ark_id = (data.get("arkId") or "").replace("ark:/", "ark-")

        return Artwork(
            id=ark_id,
            title=(data.get("title") or "").strip() or "Untitled",
            artist=artist,
            image_url=image_url,
        )

    @staticmethod
    def _louvre_artist(creator) -> str:
        if isinstance(creator, list) and creator:
            first = creator[0]
            if isinstance(first, dict):
                return (first.get("label") or first.get("name") or first.get("value") or "Unknown").strip()
            return str(first).strip()
        if isinstance(creator, dict):
            return (creator.get("label") or creator.get("name") or creator.get("value") or "Unknown").strip()
        if isinstance(creator, str):
            return creator.strip()
        return "Unknown"

    @staticmethod
    def _looks_public_domain(text: str) -> bool:
        text = text.lower()
        return "domaine public" in text or "public domain" in text

    @staticmethod
    def _safe_filename(value: str) -> str:
        value = value.encode("ascii", "ignore").decode("ascii")
        value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-")
        return value.lower() or "artwork"

    @staticmethod
    def _embed_metadata(image_path: Path, artist: str, title: str) -> None:
        # Metadata is saved in accompanying JSON file
        pass

    def _matches_tags(self, artwork: Artwork, tags: list[str]) -> bool:
        """Check if artwork matches the provided tags."""
        searchable_text = " ".join([
            artwork.title,
            artwork.artist,
        ]).lower()
        
        for tag in tags:
            if tag.lower() in searchable_text:
                return True
        return False

    def _matches_types(self, artwork: Artwork, types: list[str]) -> bool:
        """Check if artwork matches the provided type filters."""
        from ..types import get_type_keywords
        
        searchable_text = artwork.title.lower()
        
        for type_filter in types:
            keywords = get_type_keywords(type_filter)
            for keyword in keywords:
                if keyword.lower() in searchable_text:
                    return True
        return False
