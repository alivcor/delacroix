#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import requests
from PIL import Image

ASPECT_RATIO = 16 / 9
OUTPUT_ROOT = Path("output")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download and crop museum art.")
    parser.add_argument("platform", choices=["louvre", "nga"], help="Source platform")
    parser.add_argument("--max", type=int, default=20, help="Number of images to download")
    args = parser.parse_args()

    if args.max <= 0:
        raise SystemExit("--max must be > 0")

    out_dir = OUTPUT_ROOT / args.platform
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.platform == "nga":
        harvest_nga(out_dir, args.max)
    else:
        harvest_louvre(out_dir, args.max)


def harvest_nga(out_dir: Path, max_items: int) -> None:
    print("Fetching NGA open data...", flush=True)
    candidates = list(_nga_candidates(max_items * 3))
    if not candidates:
        print("No NGA candidates found.")
        return

    object_meta = _nga_object_metadata({c["object_id"] for c in candidates})

    downloaded = 0
    for candidate in candidates:
        if downloaded >= max_items:
            break
        meta = object_meta.get(candidate["object_id"], {})
        title = meta.get("title") or "Untitled"
        artist = meta.get("artist") or "Unknown"
        filename = _safe_filename(f"nga-{candidate['object_id']}-{title}") + ".jpg"
        dest = out_dir / filename
        try:
            image_url = _nga_iiif_image_url(candidate["iiif_url"], candidate.get("maxpixels"))
            _download_image(image_url, dest)
            if not _is_landscape(dest):
                dest.unlink(missing_ok=True)
                continue
            _crop_to_aspect(dest, ASPECT_RATIO)
            _embed_metadata(dest, artist=artist, title=title)
            downloaded += 1
            print(f"Downloaded {downloaded}/{max_items}: {dest.name}")
        except Exception as exc:
            dest.unlink(missing_ok=True)
            print(f"Failed NGA object {candidate['object_id']}: {exc}")

    print(f"Done. Saved {downloaded} image(s) to {out_dir}")
    print("Note: NGA data does not expose a clear open-access flag for images; verify usage terms.")


def _nga_candidates(limit: int) -> Iterable[Dict[str, str]]:
    url = "https://raw.githubusercontent.com/NationalGalleryOfArt/opendata/main/data/published_images.csv"
    reader = _stream_csv(url)
    count = 0
    for row in reader:
        if row.get("viewtype") != "primary":
            continue
        if not row.get("iiifurl"):
            continue
        width = _to_int(row.get("width"))
        height = _to_int(row.get("height"))
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


def _nga_object_metadata(object_ids: set[str]) -> Dict[str, Dict[str, str]]:
    url = "https://raw.githubusercontent.com/NationalGalleryOfArt/opendata/main/data/objects.csv"
    reader = _stream_csv(url)
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


def _nga_iiif_image_url(base_url: str, maxpixels: Optional[str]) -> str:
    size = "max"
    if maxpixels and maxpixels.isdigit():
        size = f"!{maxpixels},{maxpixels}"
    return f"{base_url}/full/{size}/0/default.jpg"


def harvest_louvre(out_dir: Path, max_items: int) -> None:
    print("Fetching Louvre sitemap...", flush=True)
    candidates = list(_louvre_candidates(max_items * 3))
    if not candidates:
        print("No Louvre candidates found.")
        return

    downloaded = 0
    for candidate in candidates:
        if downloaded >= max_items:
            break
        title = candidate.get("title") or "Untitled"
        artist = candidate.get("artist") or "Unknown"
        ark_id = candidate.get("ark") or "item"
        filename = _safe_filename(f"louvre-{ark_id}-{title}") + ".jpg"
        dest = out_dir / filename
        try:
            _download_image(candidate["image_url"], dest)
            if not _is_landscape(dest):
                dest.unlink(missing_ok=True)
                continue
            _crop_to_aspect(dest, ASPECT_RATIO)
            _embed_metadata(dest, artist=artist, title=title)
            downloaded += 1
            print(f"Downloaded {downloaded}/{max_items}: {dest.name}")
        except Exception as exc:
            dest.unlink(missing_ok=True)
            print(f"Failed Louvre item {ark_id}: {exc}")

    print(f"Done. Saved {downloaded} image(s) to {out_dir}")
    print("Note: Louvre image rights vary; this script filters to likely public-domain items.")


def _louvre_candidates(limit: int) -> Iterable[Dict[str, str]]:
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    index_url = "https://collections.louvre.fr/sitemap.xml"
    index_xml = requests.get(index_url, timeout=30).text
    index_root = ET.fromstring(index_xml)
    sitemap_urls = [loc.text for loc in index_root.findall("s:sitemap/s:loc", ns)]

    count = 0
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
            candidate = _louvre_candidate_from_json(data)
            if not candidate:
                continue
            yield candidate
            count += 1
            if count >= limit:
                return
            time.sleep(0.1)


def _louvre_candidate_from_json(data: Dict) -> Optional[Dict[str, str]]:
    images = data.get("image") or []
    if not isinstance(images, list) or not images:
        return None

    image_url = None
    for img in images:
        if not isinstance(img, dict):
            continue
        copyright_text = (img.get("copyright") or "").lower()
        if copyright_text and not _looks_public_domain(copyright_text):
            continue
        image_url = img.get("urlImage")
        if image_url:
            break

    if not image_url:
        return None

    creator = data.get("creator") or []
    artist = _louvre_artist(creator)

    return {
        "ark": (data.get("arkId") or "").replace("ark:/", "ark-"),
        "title": (data.get("title") or "").strip(),
        "artist": artist,
        "image_url": image_url,
    }


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


def _looks_public_domain(text: str) -> bool:
    text = text.lower()
    return "domaine public" in text or "public domain" in text


def _stream_csv(url: str) -> Iterable[Dict[str, str]]:
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()
    text_stream = io.TextIOWrapper(response.raw, encoding="utf-8")
    return csv.DictReader(text_stream)


def _download_image(url: str, destination: Path) -> None:
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()
    with destination.open("wb") as handle:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                handle.write(chunk)


def _is_landscape(image_path: Path) -> bool:
    with Image.open(image_path) as img:
        width, height = img.size
    return width >= height


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


def _embed_metadata(image_path: Path, *, artist: str, title: str) -> None:
    with Image.open(image_path) as img:
        exif = img.getexif()
        exif[270] = title  # ImageDescription
        exif[315] = artist  # Artist
        img.save(image_path, exif=exif, quality=95)


def _safe_filename(value: str) -> str:
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-")
    return value.lower() or "artwork"


def _to_int(value: Optional[str]) -> int:
    if not value:
        return 0
    try:
        return int(float(value))
    except ValueError:
        return 0


if __name__ == "__main__":
    main()
