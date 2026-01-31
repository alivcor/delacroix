from __future__ import annotations

import argparse
from pathlib import Path

from .core import Harvester
from .platforms.registry import PLATFORM_REGISTRY, get_platform
from .types import list_available_types


def _list_platforms() -> None:
    for name in sorted(PLATFORM_REGISTRY):
        print(name)


def _list_types(args: argparse.Namespace) -> None:
    platform = args.platform if args.platform else None
    types = list_available_types(platform)
    
    if platform:
        print(f"Available types for {platform}:")
    else:
        print("Available artwork types:")
    
    for t in sorted(types):
        print(f"  - {t}")


def _harvest(args: argparse.Namespace) -> None:
    platform = get_platform(args.platform)
    harvester = Harvester(platform, aspect_ratio=args.aspect_ratio)
    tags = args.tags.split(",") if args.tags else None
    types = args.types.split(",") if args.types else None
    result = harvester.harvest(Path(args.out), max_items=args.max, tags=tags, types=types)
    print(
        f"Platform={result.platform} downloaded={result.downloaded} "
        f"skipped_vertical={result.skipped_vertical} "
        f"skipped_missing_image={result.skipped_missing_image} failed={result.failed}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(prog="delacroix")
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list", help="List available platforms")
    list_parser.set_defaults(func=lambda _: _list_platforms())

    types_parser = sub.add_parser("types", help="List available artwork types")
    types_parser.add_argument("--platform", help="Show types for specific platform")
    types_parser.set_defaults(func=_list_types)

    harvest_parser = sub.add_parser("harvest", help="Harvest images from a platform")
    harvest_parser.add_argument("--platform", required=True, help="Platform name (chicago, nga, louvre, met, rijksmuseum)")
    harvest_parser.add_argument("--out", required=True, help="Output directory")
    harvest_parser.add_argument("--max", type=int, default=5, help="Max items (default: 5)")
    harvest_parser.add_argument(
        "--aspect-ratio",
        type=float,
        default=16 / 9,
        help="Target aspect ratio, e.g. 1.777 for 16:9",
    )
    harvest_parser.add_argument(
        "--tags",
        type=str,
        default="european,1800s",
        help="Comma-separated tags to filter (default: 'european,1800s')",
    )
    harvest_parser.add_argument(
        "--types",
        type=str,
        default="painting",
        help="Comma-separated artwork types (default: 'painting')",
    )
    harvest_parser.set_defaults(func=_harvest)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
