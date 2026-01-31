from __future__ import annotations

import csv
import io
import re
from pathlib import Path
from typing import Dict, Iterable, Optional

import requests
from PIL import Image

from .base import Artwork, BasePlatform


class NGAPlatform(BasePlatform):
    name = "nga"

    def list_artworks(self, tags: Optional[list[str]] = None, types: Optional[list[str]] = None) -> Iterable[Artwork]:
        candidates = list(self._nga_candidates(500))
        if not candidates:
            return
        
        object_meta = self._nga_object_metadata({c["object_id"] for c in candidates})
        
        for candidate in candidates:
            meta = object_meta.get(candidate["object_id"], {})
            title = meta.get("title") or "Untitled"
            artist = meta.get("artist") or "Unknown"
            image_url = self._nga_iiif_image_url(candidate["iiif_url"], candidate.get("maxpixels"))
            
            artwork = Artwork(
                id=candidate["object_id"],
                title=title,
                artist=artist,
                image_url=image_url,
            )
            
            # Filter by tags if provided
            if tags and not self._matches_tags(artwork, tags):
                continue
            
            # Filter by types if provided (NGA has limited type info)
            if types and not self._matches_types(artwork, types):
                continue
                
            yield artwork

    def download_image(self, artwork: Artwork, output_dir: Path) -> Optional[Path]:
        if not artwork.image_url:
            return None
        
        filename = self._safe_filename(f"nga-{artwork.id}-{artwork.title}") + ".jpg"
        destination = output_dir / filename
        
        response = requests.get(artwork.image_url, timeout=60)
        response.raise_for_status()
        destination.write_bytes(response.content)
        self._embed_metadata(destination, artwork.artist, artwork.title)
        
        # Save metadata to JSON
        import json
        from dataclasses import asdict
        json_file = output_dir / (self._safe_filename(f"nga-{artwork.id}-{artwork.title}") + ".json")
        json_file.write_text(json.dumps(asdict(artwork), indent=2), encoding="utf-8")
        
        return destination

    def _nga_candidates(self, limit: int) -> Iterable[Dict[str, str]]:
        url = "https://raw.githubusercontent.com/NationalGalleryOfArt/opendata/main/data/published_images.csv"
        reader = self._stream_csv(url)
        count = 0
        for row in reader:
            if row.get("viewtype") != "primary":
                continue
            if not row.get("iiifurl"):
                continue
            width = self._to_int(row.get("width"))
            height = self._to_int(row.get("height"))
            if width and height and width < height:
                continue
            count += 1
            yield {
                "object_id": row.get("depictstmsobjectid", "").strip(),
                "iiif_url": row.get("iiifurl", "").strip(),
                "maxpixels": row.get("maxpixels", "").strip(),
            }
            if count >= limit:
                break

    def _nga_object_metadata(self, object_ids: set[str]) -> Dict[str, Dict[str, str]]:
        url = "https://raw.githubusercontent.com/NationalGalleryOfArt/opendata/main/data/objects.csv"
        reader = self._stream_csv(url)
        metadata: Dict[str, Dict[str, str]] = {}
        remaining = set(object_ids)
        for row in reader:
            object_id = row.get("objectid", "").strip()
            if object_id in remaining:
                metadata[object_id] = {
                    "title": row.get("title", "").strip(),
                    "artist": row.get("attribution", "").strip(),
                }
                remaining.remove(object_id)
                if not remaining:
                    break
        return metadata

    @staticmethod
    def _nga_iiif_image_url(base_url: str, maxpixels: Optional[str]) -> str:
        size = "max"
        if maxpixels and maxpixels.isdigit():
            size = f"!{maxpixels},{maxpixels}"
        return f"{base_url}/full/{size}/0/default.jpg"

    @staticmethod
    def _stream_csv(url: str) -> Iterable[Dict[str, str]]:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        # Handle gzip compression
        import gzip
        if response.headers.get('Content-Encoding') == 'gzip':
            text_stream = io.TextIOWrapper(gzip.GzipFile(fileobj=response.raw), encoding="utf-8")
        else:
            text_stream = io.TextIOWrapper(response.raw, encoding="utf-8")
        return csv.DictReader(text_stream)

    @staticmethod
    def _safe_filename(value: str) -> str:
        value = value.encode("ascii", "ignore").decode("ascii")
        value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-")
        return value.lower() or "artwork"

    @staticmethod
    def _embed_metadata(image_path: Path, artist: str, title: str) -> None:
        # Metadata is saved in accompanying JSON file
        pass

    @staticmethod
    def _to_int(value: Optional[str]) -> int:
        if not value:
            return 0
        try:
            return int(float(value))
        except ValueError:
            return 0

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
