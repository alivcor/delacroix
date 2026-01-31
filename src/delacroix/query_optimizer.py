"""Smart query optimization for faster artwork discovery."""

from typing import List, Optional

# Famous artists by time period for targeted queries
ARTISTS_BY_PERIOD = {
    "1400s": ["van eyck", "fra angelico", "masaccio"],
    "1500s": ["leonardo", "michelangelo", "raphael", "titian", "dürer", "holbein"],
    "1600s": ["caravaggio", "rembrandt", "vermeer", "rubens", "velázquez", "poussin"],
    "1700s": ["watteau", "canaletto", "tiepolo", "gainsborough", "reynolds", "goya", "david"],
    "1800s": ["turner", "delacroix", "courbet", "monet", "renoir", "degas", "van gogh", "cézanne"],
    "1900s": ["picasso", "matisse", "kandinsky", "klimt", "munch", "hopper"],
}

# European regions and their famous artists
ARTISTS_BY_REGION = {
    "french": ["monet", "renoir", "degas", "cézanne", "gauguin", "delacroix", "poussin", "watteau", "ingres", "david"],
    "italian": ["leonardo", "michelangelo", "raphael", "titian", "caravaggio", "botticelli"],
    "dutch": ["rembrandt", "vermeer", "van gogh", "mondrian", "bosch"],
    "spanish": ["velázquez", "goya", "picasso", "dalí", "el greco", "murillo"],
    "german": ["dürer", "friedrich", "holbein", "kandinsky", "klee"],
    "flemish": ["rubens", "van eyck", "bruegel", "van der weyden"],
    "british": ["turner", "constable", "gainsborough", "reynolds"],
    "european": ["monet", "rembrandt", "van gogh", "picasso", "leonardo", "michelangelo"],
}

# Met Museum department IDs for faster filtering
MET_DEPARTMENTS = {
    "european_paintings": 11,
    "drawings_prints": 5,
    "photographs": 19,
    "american_paintings": 21,
    "asian_art": 6,
    "greek_roman": 13,
}


def build_optimized_queries(
    tags: Optional[List[str]] = None,
    types: Optional[List[str]] = None
) -> List[str]:
    """Build multiple targeted queries instead of one generic query."""
    queries = []
    
    # Extract time period from tags
    time_period = None
    region = None
    
    if tags:
        for tag in tags:
            tag_lower = tag.lower()
            # Check for time periods
            if any(period in tag_lower for period in ["1400", "1500", "1600", "1700", "1800", "1900"]):
                # Extract century
                for century in ["1400s", "1500s", "1600s", "1700s", "1800s", "1900s"]:
                    if century[:3] in tag_lower:
                        time_period = century
                        break
            # Check for regions
            for region_key in ARTISTS_BY_REGION:
                if region_key in tag_lower:
                    region = region_key
                    break
    
    # Build queries targeting famous artists
    target_artists = set()
    
    if time_period and time_period in ARTISTS_BY_PERIOD:
        target_artists.update(ARTISTS_BY_PERIOD[time_period])
    
    if region and region in ARTISTS_BY_REGION:
        target_artists.update(ARTISTS_BY_REGION[region])
    
    # If we have specific artists, query for them
    if target_artists:
        # Create queries for top artists (limit to avoid too many queries)
        for artist in list(target_artists)[:10]:
            queries.append(artist)
    else:
        # Fallback to generic query
        query_parts = []
        if types:
            query_parts.extend(types)
        if tags:
            query_parts.extend(tags)
        queries.append(" ".join(query_parts) if query_parts else "painting")
    
    return queries


def get_met_department_id(types: Optional[List[str]] = None, tags: Optional[List[str]] = None) -> Optional[int]:
    """Get the most relevant Met department ID for filtering."""
    if not types and not tags:
        return MET_DEPARTMENTS["european_paintings"]
    
    if types:
        type_lower = types[0].lower()
        if "painting" in type_lower:
            # Check if European or American
            if tags and any("american" in t.lower() for t in tags):
                return MET_DEPARTMENTS["american_paintings"]
            return MET_DEPARTMENTS["european_paintings"]
        elif "photograph" in type_lower:
            return MET_DEPARTMENTS["photographs"]
        elif "drawing" in type_lower or "print" in type_lower:
            return MET_DEPARTMENTS["drawings_prints"]
    
    return MET_DEPARTMENTS["european_paintings"]


def should_prioritize_artist(artist_name: str, tags: Optional[List[str]] = None) -> bool:
    """Check if artist matches the search criteria for prioritization."""
    if not artist_name or not tags:
        return False
    
    artist_lower = artist_name.lower()
    
    # Check if artist matches time period
    for tag in tags:
        tag_lower = tag.lower()
        for century, artists in ARTISTS_BY_PERIOD.items():
            if century[:3] in tag_lower:
                if any(artist in artist_lower for artist in artists):
                    return True
        
        # Check if artist matches region
        for region, artists in ARTISTS_BY_REGION.items():
            if region in tag_lower:
                if any(artist in artist_lower for artist in artists):
                    return True
    
    return False
