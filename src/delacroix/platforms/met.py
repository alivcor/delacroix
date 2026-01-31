from __future__ import annotations

import json
import re
from dataclasses import asdict
from pathlib import Path
from typing import Iterable, Optional

import requests
from PIL import Image

from .base import Artwork, BasePlatform
from ..types import get_type_keywords
from ..knowledge_base import build_smart_queries, get_met_department_for_query, is_artist_famous


class MetMuseumPlatform(BasePlatform):
    name = "met"
    base_url = "https://collectionapi.metmuseum.org/public/collection/v1"

    def list_artworks(self, tags: Optional[list[str]] = None, types: Optional[list[str]] = None) -> Iterable[Artwork]:
        # Build intelligent queries using art knowledge database
        queries = build_smart_queries(tags, types)
        department_id = get_met_department_for_query(types, tags)
        
        print(f"🎨 Searching for: {', '.join(queries[:5])}...")
        
        # Collect artworks from multiple targeted queries
        famous_artworks = []
        regular_artworks = []
        seen_ids = set()
        
        for query in queries:
            params = {
                "hasImages": "true",
                "isPublicDomain": "true",
                "q": query,
            }
            
            # Add department filter for faster results
            if department_id:
                params["departmentId"] = department_id
            
            try:
                response = requests.get(f"{self.base_url}/search", params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                object_ids = data.get("objectIDs") or []
                
                # Limit objects per query to avoid slowness
                for object_id in object_ids[:30]:
                    if object_id in seen_ids:
                        continue
                    seen_ids.add(object_id)
                    
                    art = self._fetch_object(object_id, tags, types)
                    if art:
                        if is_artist_famous(art.artist):
                            famous_artworks.append(art)
                            print(f"✓ Found: {art.title} by {art.artist}")
                        else:
                            regular_artworks.append(art)
                        
                        # Early exit if we have enough famous artworks
                        if len(famous_artworks) >= 30:
                            break
                
                if len(famous_artworks) >= 30:
                    break
                    
            except Exception as e:
                continue
        
        print(f"📊 Found {len(famous_artworks)} famous artworks, {len(regular_artworks)} others")
        
        # Yield famous artists first, then regular ones
        for art in famous_artworks:
            yield art
        for art in regular_artworks:
            yield art

    def _fetch_object(self, object_id: int, tags: Optional[list[str]] = None, types: Optional[list[str]] = None) -> Optional[Artwork]:
        try:
            response = requests.get(f"{self.base_url}/objects/{object_id}", timeout=30)
            response.raise_for_status()
            data = response.json()
        except Exception:
            return None
            
        if not data.get("isPublicDomain"):
            return None
        
        # Filter by tags if provided
        if tags and not self._matches_tags(data, tags):
            return None
        
        # Filter by types if provided
        if types and not self._matches_types(data, types):
            return None
            
        image_url = data.get("primaryImage") or data.get("primaryImageSmall")
        return Artwork(
            id=str(data.get("objectID")),
            title=data.get("title") or "Untitled",
            artist=data.get("artistDisplayName") or "Unknown",
            image_url=image_url,
            date=data.get("objectDate"),
            culture=data.get("culture"),
            classification=data.get("classification"),
        )

    def _matches_tags(self, data: dict, tags: list[str]) -> bool:
        """Check if artwork matches the provided tags."""
        searchable_text = " ".join([
            str(data.get("artistDisplayName", "")),
            str(data.get("culture", "")),
            str(data.get("objectDate", "")),
            str(data.get("classification", "")),
            str(data.get("medium", "")),
            str(data.get("artistNationality", "")),
            str(data.get("period", "")),
        ]).lower()
        
        # Check if any tag matches
        for tag in tags:
            tag_lower = tag.lower()
            
            # Handle century tags (e.g., "1800s", "19th century")
            if tag_lower.endswith("s") and tag_lower[:-1].isdigit():
                century = tag_lower[:-1]
                if century in searchable_text:
                    return True
            elif "century" in tag_lower:
                if tag_lower in searchable_text:
                    return True
            # Handle year ranges
            elif tag_lower.isdigit() and len(tag_lower) == 4:
                if tag_lower in searchable_text:
                    return True
            # Handle general tags (baroque, european, etc.)
            elif tag_lower in searchable_text:
                return True
        
        return False

    def _matches_types(self, data: dict, types: list[str]) -> bool:
        """Check if artwork matches the provided type filters (strict matching)."""
        classification = str(data.get("classification", "")).lower()
        object_name = str(data.get("objectName", "")).lower()
        
        # For strict type filtering, check classification field primarily
        for type_filter in types:
            keywords = get_type_keywords(type_filter)
            
            # Check if classification exactly matches the type
            for keyword in keywords:
                keyword_lower = keyword.lower()
                # Exact match in classification (most reliable)
                if keyword_lower in classification:
                    return True
                # For paintings, also check object name
                if type_filter.lower() == "painting" and "painting" in object_name:
                    return True
                # For photographs, be strict
                if type_filter.lower() == "photograph" and "photograph" in classification:
                    return True
                # For drawings, check both fields
                if type_filter.lower() == "drawing" and ("drawing" in classification or "drawing" in object_name):
                    return True
        
        return False

    def download_image(self, artwork: Artwork, output_dir: Path) -> Optional[Path]:
        if not artwork.image_url:
            return None
        filename = self._safe_filename(f"met-{artwork.id}-{artwork.title}") + ".jpg"
        destination = output_dir / filename
        response = requests.get(artwork.image_url, timeout=60)
        response.raise_for_status()
        destination.write_bytes(response.content)
        self._embed_metadata(destination, artwork.artist, artwork.title)
        (output_dir / f"{self._safe_filename(f'met-{artwork.id}-{artwork.title}')}.json").write_text(
            json.dumps(asdict(artwork), indent=2), encoding="utf-8"
        )
        return destination

    @staticmethod
    def _safe_filename(value: str) -> str:
        value = value.encode("ascii", "ignore").decode("ascii")
        value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-")
        return value.lower() or "artwork"

    @staticmethod
    def _embed_metadata(image_path: Path, artist: str, title: str) -> None:
        # Metadata is saved in accompanying JSON file
        # JPEG EXIF metadata can be unreliable across different viewers
        pass
