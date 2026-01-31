from __future__ import annotations

import json
import re
from dataclasses import asdict
from pathlib import Path
from typing import Iterable, Optional

import requests
from PIL import Image

from .base import Artwork, BasePlatform
from ..knowledge_base import is_artist_famous


class RijksmuseumPlatform(BasePlatform):
    name = "rijksmuseum"
    base_url = "https://www.rijksmuseum.nl/api/en/collection"
    # Public API key for demo purposes
    api_key = "0fiuZFh4"

    def list_artworks(self, tags: Optional[list[str]] = None, types: Optional[list[str]] = None) -> Iterable[Artwork]:
        """List artworks from Rijksmuseum."""
        
        # Build query
        query_parts = []
        if types and "painting" in types[0].lower():
            query_parts.append("painting")
        
        # Rijksmuseum specializes in Dutch art
        if tags:
            for tag in tags:
                if any(term in tag.lower() for term in ["dutch", "netherlands", "rembrandt", "vermeer"]):
                    query_parts.append(tag)
        
        query = " ".join(query_parts) if query_parts else "painting"
        
        print(f"🇳🇱 Searching Rijksmuseum for: {query}")
        
        params = {
            "key": self.api_key,
            "q": query,
            "imgonly": "true",
            "ps": 100,  # results per page
            "p": 0,
        }
        
        famous_artworks = []
        regular_artworks = []
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            art_objects = data.get("artObjects", [])
            
            for obj in art_objects:
                artwork = self._parse_artwork(obj)
                if artwork and artwork.image_url:
                    if is_artist_famous(artwork.artist):
                        famous_artworks.append(artwork)
                        print(f"✓ Found: {artwork.title} by {artwork.artist}")
                    else:
                        regular_artworks.append(artwork)
                    
                    if len(famous_artworks) >= 20:
                        break
        
        except Exception as e:
            print(f"Error fetching from Rijksmuseum: {e}")
        
        print(f"📊 Rijksmuseum: {len(famous_artworks)} famous, {len(regular_artworks)} others")
        
        # Yield famous first
        for art in famous_artworks:
            yield art
        for art in regular_artworks:
            yield art

    def _parse_artwork(self, obj: dict) -> Optional[Artwork]:
        """Parse Rijksmuseum API object into Artwork."""
        try:
            # Get image URL
            image_url = obj.get("webImage", {}).get("url")
            if not image_url:
                return None
            
            return Artwork(
                id=obj.get("objectNumber", ""),
                title=obj.get("title", "Untitled"),
                artist=obj.get("principalOrFirstMaker", "Unknown"),
                image_url=image_url,
                date=obj.get("dating", {}).get("presentingDate"),
                culture="Dutch",
                classification=obj.get("objectTypes", [""])[0] if obj.get("objectTypes") else None,
            )
        except Exception:
            return None

    def download_image(self, artwork: Artwork, output_dir: Path) -> Optional[Path]:
        """Download image from Rijksmuseum."""
        if not artwork.image_url:
            return None
        
        filename = self._safe_filename(f"rijks-{artwork.id}-{artwork.title}") + ".jpg"
        destination = output_dir / filename
        
        try:
            response = requests.get(artwork.image_url, timeout=60)
            response.raise_for_status()
            destination.write_bytes(response.content)
            
            # Save metadata
            json_file = output_dir / (self._safe_filename(f"rijks-{artwork.id}-{artwork.title}") + ".json")
            json_file.write_text(json.dumps(asdict(artwork), indent=2), encoding="utf-8")
            
            return destination
        except Exception:
            return None

    @staticmethod
    def _safe_filename(value: str) -> str:
        value = value.encode("ascii", "ignore").decode("ascii")
        value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-")
        return value.lower()[:100] or "artwork"
