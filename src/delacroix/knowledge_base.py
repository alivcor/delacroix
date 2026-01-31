"""Knowledge base loader and intelligent query builder."""

import json
from pathlib import Path
from typing import Dict, List, Optional, Set
from functools import lru_cache

# Cache the loaded databases
_ARTISTS_DB = None
_MOVEMENTS_DB = None
_PAINTINGS_DB = None


def _load_json(filename: str) -> dict:
    """Load a JSON database file."""
    data_dir = Path(__file__).parent / "data"
    file_path = data_dir / filename
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_artists_db() -> List[Dict]:
    """Get the artists database."""
    global _ARTISTS_DB
    if _ARTISTS_DB is None:
        _ARTISTS_DB = _load_json("artists.json")["artists"]
    return _ARTISTS_DB


def get_movements_db() -> List[Dict]:
    """Get the movements database."""
    global _MOVEMENTS_DB
    if _MOVEMENTS_DB is None:
        _MOVEMENTS_DB = _load_json("movements.json")["movements"]
    return _MOVEMENTS_DB


def get_paintings_db() -> List[Dict]:
    """Get the paintings database."""
    global _PAINTINGS_DB
    if _PAINTINGS_DB is None:
        _PAINTINGS_DB = _load_json("paintings.json")["paintings"]
    return _PAINTINGS_DB


@lru_cache(maxsize=128)
def find_artists_by_period(start_year: int, end_year: int, limit: int = 20) -> List[str]:
    """Find artists active during a specific period."""
    artists_db = get_artists_db()
    matching_artists = []
    
    for artist in artists_db:
        birth = artist["birth"]
        death = artist["death"]
        
        # Artist was active if their lifespan overlaps with the period
        if not (death < start_year or birth > end_year):
            matching_artists.append({
                "name": artist["name"],
                "priority": artist.get("priority", 50),
                "aliases": artist.get("aliases", [])
            })
    
    # Sort by priority (higher first)
    matching_artists.sort(key=lambda x: x["priority"], reverse=True)
    
    # Return artist names and aliases
    result = []
    for artist in matching_artists[:limit]:
        result.append(artist["name"])
        result.extend(artist["aliases"][:1])  # Add first alias
    
    return result


@lru_cache(maxsize=128)
def find_artists_by_nationality(nationality: str, limit: int = 15) -> List[str]:
    """Find artists by nationality."""
    artists_db = get_artists_db()
    nationality_lower = nationality.lower()
    matching_artists = []
    
    for artist in artists_db:
        if artist["nationality"].lower() == nationality_lower:
            matching_artists.append({
                "name": artist["name"],
                "priority": artist.get("priority", 50),
                "aliases": artist.get("aliases", [])
            })
    
    # Sort by priority
    matching_artists.sort(key=lambda x: x["priority"], reverse=True)
    
    result = []
    for artist in matching_artists[:limit]:
        result.append(artist["name"])
        if artist["aliases"]:
            result.append(artist["aliases"][0])
    
    return result


@lru_cache(maxsize=128)
def find_artists_by_movement(movement: str, limit: int = 15) -> List[str]:
    """Find artists by art movement."""
    artists_db = get_artists_db()
    movement_lower = movement.lower()
    matching_artists = []
    
    for artist in artists_db:
        movements = [m.lower() for m in artist.get("movements", [])]
        if movement_lower in movements or any(movement_lower in m for m in movements):
            matching_artists.append({
                "name": artist["name"],
                "priority": artist.get("priority", 50),
                "aliases": artist.get("aliases", [])
            })
    
    # Sort by priority
    matching_artists.sort(key=lambda x: x["priority"], reverse=True)
    
    result = []
    for artist in matching_artists[:limit]:
        result.append(artist["name"])
        if artist["aliases"]:
            result.append(artist["aliases"][0])
    
    return result


def extract_period_from_tags(tags: List[str]) -> Optional[tuple]:
    """Extract time period from tags (returns start_year, end_year)."""
    for tag in tags:
        tag_lower = tag.lower()
        
        # Check for century patterns
        for century in range(1400, 2000, 100):
            century_str = str(century)
            if century_str[:3] in tag_lower or f"{century_str}s" in tag_lower:
                return (century, century + 99)
        
        # Check for specific decades
        for decade in range(1400, 2000, 10):
            if f"{decade}s" in tag_lower:
                return (decade, decade + 9)
    
    return None


def extract_nationality_from_tags(tags: List[str]) -> Optional[str]:
    """Extract nationality from tags."""
    nationalities = {
        "french": "French",
        "italian": "Italian",
        "dutch": "Dutch",
        "spanish": "Spanish",
        "german": "German",
        "british": "British",
        "american": "American",
        "flemish": "Flemish",
        "austrian": "Austrian",
        "belgian": "Belgian",
        "russian": "Russian",
        "norwegian": "Norwegian",
    }
    
    for tag in tags:
        tag_lower = tag.lower()
        for key, value in nationalities.items():
            if key in tag_lower:
                return value
    
    # Check for "european" - return None to handle specially
    for tag in tags:
        if "european" in tag.lower() or "europe" in tag.lower():
            return "European"
    
    return None


def extract_movement_from_tags(tags: List[str]) -> Optional[str]:
    """Extract art movement from tags."""
    movements_db = get_movements_db()
    
    for tag in tags:
        tag_lower = tag.lower()
        for movement in movements_db:
            movement_name = movement["name"].lower()
            if movement_name in tag_lower or any(kw in tag_lower for kw in movement.get("keywords", [])):
                return movement["name"]
    
    return None


def build_smart_queries(tags: Optional[List[str]] = None, types: Optional[List[str]] = None) -> List[str]:
    """Build intelligent queries based on art knowledge database."""
    import random
    
    if not tags:
        # Default: mix of famous artists from different movements - randomized
        default_artists = ["Rembrandt", "Monet", "Van Gogh", "Picasso", "Renoir", "Degas", 
                          "Cézanne", "Gauguin", "Turner", "Delacroix", "Manet", "Pissarro",
                          "Velázquez", "Caravaggio", "Rubens", "Raphael", "Titian"]
        random.shuffle(default_artists)
        return default_artists[:10]
    
    queries = []
    seen = set()
    
    # Extract information from tags
    period = extract_period_from_tags(tags)
    nationality = extract_nationality_from_tags(tags)
    movement = extract_movement_from_tags(tags)
    
    # Build queries based on extracted information
    if period:
        artists = find_artists_by_period(period[0], period[1], limit=20)
        random.shuffle(artists)
        for artist in artists[:15]:
            if artist not in seen:
                queries.append(artist)
                seen.add(artist)
    
    if movement:
        artists = find_artists_by_movement(movement, limit=20)
        random.shuffle(artists)
        for artist in artists[:15]:
            if artist not in seen:
                queries.append(artist)
                seen.add(artist)
    
    if nationality:
        if nationality == "European":
            # Get mix from major European countries
            nationalities = ["French", "Italian", "Dutch", "Spanish", "German", "Flemish"]
            random.shuffle(nationalities)
            for nat in nationalities:
                artists = find_artists_by_nationality(nat, limit=3)
                random.shuffle(artists)
                for artist in artists:
                    if artist not in seen:
                        queries.append(artist)
                        seen.add(artist)
        else:
            artists = find_artists_by_nationality(nationality, limit=20)
            random.shuffle(artists)
            for artist in artists[:15]:
                if artist not in seen:
                    queries.append(artist)
                    seen.add(artist)
    
    # If no specific criteria found, use high-priority artists
    if not queries:
        artists_db = get_artists_db()
        high_priority = [a for a in artists_db if a.get("priority", 0) >= 90]
        random.shuffle(high_priority)
        for artist in high_priority[:15]:
            queries.append(artist["name"])
    
    # Shuffle final queries for variety
    random.shuffle(queries)
    return queries[:15]  # Limit to 15 queries


def get_met_department_for_query(types: Optional[List[str]] = None, tags: Optional[List[str]] = None) -> Optional[int]:
    """Get the best Met Museum department ID for the query."""
    departments = {
        "european_paintings": 11,
        "american_paintings": 21,
        "drawings_prints": 5,
        "photographs": 19,
        "asian_art": 6,
    }
    
    # Check type first
    if types:
        type_lower = types[0].lower()
        if "painting" in type_lower:
            # Check if American
            if tags and any("american" in t.lower() for t in tags):
                return departments["american_paintings"]
            return departments["european_paintings"]
        elif "photograph" in type_lower:
            return departments["photographs"]
        elif "drawing" in type_lower or "print" in type_lower:
            return departments["drawings_prints"]
    
    # Check tags for region
    if tags:
        for tag in tags:
            tag_lower = tag.lower()
            if "american" in tag_lower:
                return departments["american_paintings"]
            elif "asian" in tag_lower or "chinese" in tag_lower or "japanese" in tag_lower:
                return departments["asian_art"]
    
    # Default to European paintings
    return departments["european_paintings"]


def is_artist_famous(artist_name: str) -> bool:
    """Check if an artist is in our famous artists database."""
    if not artist_name:
        return False
    
    artists_db = get_artists_db()
    artist_lower = artist_name.lower()
    
    for artist in artists_db:
        # Check name
        if artist["name"].lower() == artist_lower:
            return True
        # Check aliases
        for alias in artist.get("aliases", []):
            if alias.lower() == artist_lower or alias.lower() in artist_lower or artist_lower in alias.lower():
                return True
        # Check if artist name contains any part of famous artist
        if artist["name"].lower() in artist_lower:
            return True
    
    return False
