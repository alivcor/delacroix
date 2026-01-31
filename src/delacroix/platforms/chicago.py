from __future__ import annotations

import json
import re
from dataclasses import asdict
from pathlib import Path
from typing import Iterable, Optional

import requests
from PIL import Image

from .base import Artwork, BasePlatform
from ..knowledge_base import is_artist_famous, build_smart_queries


class ChicagoPlatform(BasePlatform):
    name = "chicago"
    base_url = "https://api.artic.edu/api/v1"

    def list_artworks(self, tags: Optional[list[str]] = None, types: Optional[list[str]] = None) -> Iterable[Artwork]:
        """List artworks from Art Institute of Chicago."""
        
        print(f"🏛️ Searching Art Institute of Chicago...")
        
        famous_artworks = []
        regular_artworks = []
        
        # Use smart queries from knowledge base
        artist_queries = build_smart_queries(tags, types)
        
        for query in artist_queries[:5]:  # Try top 5 artists
            # Add painting filter to query if type is painting
            search_query = query
            if types and "painting" in types[0].lower():
                search_query = f"{query} painting"
            
            params = {
                "q": search_query,
                "fields": "id,title,artist_display,date_display,image_id,artwork_type_title,classification_title,medium_display",
                "limit": 30,
            }
            
            try:
                response = requests.get(f"{self.base_url}/artworks/search", params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                for item in data.get("data", []):
                    artwork_id = item.get("id")
                    if not artwork_id:
                        continue
                    
                    artwork = self._fetch_artwork(artwork_id, tags, types)
                    if artwork and artwork.image_url:
                        if is_artist_famous(artwork.artist):
                            famous_artworks.append(artwork)
                            print(f"✓ Found: {artwork.title} by {artwork.artist}")
                        else:
                            regular_artworks.append(artwork)
                        
                        if len(famous_artworks) >= 20:
                            break
                
                if len(famous_artworks) >= 20:
                    break
                    
            except Exception as e:
                continue
        
        print(f"📊 Chicago: {len(famous_artworks)} famous, {len(regular_artworks)} others")
        
        # Yield famous first
        for art in famous_artworks:
            yield art
        for art in regular_artworks:
            yield art

    def _fetch_artwork(self, artwork_id: int, tags: Optional[list[str]], types: Optional[list[str]]) -> Optional[Artwork]:
        """Fetch detailed artwork information."""
        try:
            response = requests.get(f"{self.base_url}/artworks/{artwork_id}", timeout=30)
            response.raise_for_status()
            data = response.json().get("data", {})
            
            # Check if has image
            image_id = data.get("image_id")
            if not image_id:
                return None
            
            # Filter by type if specified
            artwork_type = data.get("artwork_type_title", "").lower()
            classification = data.get("classification_title", "").lower()
            medium = data.get("medium_display", "").lower()
            
            if types:
                type_filter = types[0].lower()
                
                # For paintings, be strict - exclude drawings, prints, sketches
                if "painting" in type_filter:
                    # Must be a painting
                    if "painting" not in artwork_type and "painting" not in classification:
                        return None
                    # Exclude drawings, prints, sketches, watercolors
                    exclude_terms = ["drawing", "print", "sketch", "watercolor", "etching", "lithograph", "engraving"]
                    if any(term in artwork_type or term in classification or term in medium for term in exclude_terms):
                        return None
                    # Prefer oil paintings
                    if "oil" not in medium and "canvas" not in medium:
                        # Allow but deprioritize
                        pass
                
                elif "photograph" in type_filter:
                    if "photograph" not in artwork_type and "photograph" not in classification:
                        return None
                
                elif "drawing" in type_filter:
                    if "drawing" not in artwork_type and "drawing" not in classification:
                        return None
            
            # Build IIIF image URL
            iiif_url = data.get("config", {}).get("iiif_url")
            if not iiif_url:
                iiif_url = "https://www.artic.edu/iiif/2"
            
            image_url = f"{iiif_url}/{image_id}/full/843,/0/default.jpg"
            
            return Artwork(
                id=str(artwork_id),
                title=data.get("title", "Untitled"),
                artist=data.get("artist_display", "Unknown").split("\n")[0],  # First line is artist name
                image_url=image_url,
                date=data.get("date_display"),
                culture=data.get("place_of_origin"),
                classification=data.get("artwork_type_title"),
            )
        except Exception:
            return None

    def download_image(self, artwork: Artwork, output_dir: Path) -> Optional[Path]:
        """Download image from Chicago."""
        if not artwork.image_url:
            return None
        
        filename = self._safe_filename(f"chicago-{artwork.id}-{artwork.title}") + ".jpg"
        destination = output_dir / filename
        
        try:
            response = requests.get(artwork.image_url, timeout=60)
            response.raise_for_status()
            destination.write_bytes(response.content)
            
            # Save metadata
            json_file = output_dir / (self._safe_filename(f"chicago-{artwork.id}-{artwork.title}") + ".json")
            json_file.write_text(json.dumps(asdict(artwork), indent=2), encoding="utf-8")
            
            return destination
        except Exception:
            return None

    @staticmethod
    def _safe_filename(value: str) -> str:
        value = value.encode("ascii", "ignore").decode("ascii")
        value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-")
        return value.lower()[:100] or "artwork"
