"""Comprehensive art knowledge database for intelligent querying."""

from typing import Dict, List, Optional, Tuple

# Artist lifespans and nationalities
ARTIST_DATABASE = {
    # Renaissance Masters
    "leonardo da vinci": {"years": (1452, 1519), "nationality": "italian", "movements": ["renaissance"]},
    "michelangelo": {"years": (1475, 1564), "nationality": "italian", "movements": ["renaissance"]},
    "raphael": {"years": (1483, 1520), "nationality": "italian", "movements": ["renaissance"]},
    "titian": {"years": (1488, 1576), "nationality": "italian", "movements": ["renaissance"]},
    "botticelli": {"years": (1445, 1510), "nationality": "italian", "movements": ["renaissance"]},
    
    # Northern Renaissance
    "albrecht dürer": {"years": (1471, 1528), "nationality": "german", "movements": ["renaissance"]},
    "hieronymus bosch": {"years": (1450, 1516), "nationality": "dutch", "movements": ["renaissance"]},
    "pieter bruegel": {"years": (1525, 1569), "nationality": "flemish", "movements": ["renaissance"]},
    "jan van eyck": {"years": (1390, 1441), "nationality": "flemish", "movements": ["renaissance"]},
    
    # Baroque
    "caravaggio": {"years": (1571, 1610), "nationality": "italian", "movements": ["baroque"]},
    "rembrandt": {"years": (1606, 1669), "nationality": "dutch", "movements": ["baroque"]},
    "johannes vermeer": {"years": (1632, 1675), "nationality": "dutch", "movements": ["baroque"]},
    "peter paul rubens": {"years": (1577, 1640), "nationality": "flemish", "movements": ["baroque"]},
    "diego velázquez": {"years": (1599, 1660), "nationality": "spanish", "movements": ["baroque"]},
    "nicolas poussin": {"years": (1594, 1665), "nationality": "french", "movements": ["baroque"]},
    "frans hals": {"years": (1582, 1666), "nationality": "dutch", "movements": ["baroque"]},
    
    # Rococo
    "jean-antoine watteau": {"years": (1684, 1721), "nationality": "french", "movements": ["rococo"]},
    "françois boucher": {"years": (1703, 1770), "nationality": "french", "movements": ["rococo"]},
    "jean-honoré fragonard": {"years": (1732, 1806), "nationality": "french", "movements": ["rococo"]},
    "giovanni battista tiepolo": {"years": (1696, 1770), "nationality": "italian", "movements": ["rococo"]},
    "canaletto": {"years": (1697, 1768), "nationality": "italian", "movements": ["rococo"]},
    
    # Neoclassicism
    "jacques-louis david": {"years": (1748, 1825), "nationality": "french", "movements": ["neoclassicism"]},
    "jean-auguste-dominique ingres": {"years": (1780, 1867), "nationality": "french", "movements": ["neoclassicism"]},
    
    # Romanticism
    "eugène delacroix": {"years": (1798, 1863), "nationality": "french", "movements": ["romanticism"]},
    "j.m.w. turner": {"years": (1775, 1851), "nationality": "british", "movements": ["romanticism"]},
    "caspar david friedrich": {"years": (1774, 1840), "nationality": "german", "movements": ["romanticism"]},
    "francisco goya": {"years": (1746, 1828), "nationality": "spanish", "movements": ["romanticism"]},
    "théodore géricault": {"years": (1791, 1824), "nationality": "french", "movements": ["romanticism"]},
    "john constable": {"years": (1776, 1837), "nationality": "british", "movements": ["romanticism"]},
    
    # Realism
    "gustave courbet": {"years": (1819, 1877), "nationality": "french", "movements": ["realism"]},
    "jean-françois millet": {"years": (1814, 1875), "nationality": "french", "movements": ["realism"]},
    "honoré daumier": {"years": (1808, 1879), "nationality": "french", "movements": ["realism"]},
    
    # Impressionism
    "claude monet": {"years": (1840, 1926), "nationality": "french", "movements": ["impressionism"]},
    "pierre-auguste renoir": {"years": (1841, 1919), "nationality": "french", "movements": ["impressionism"]},
    "edgar degas": {"years": (1834, 1917), "nationality": "french", "movements": ["impressionism"]},
    "camille pissarro": {"years": (1830, 1903), "nationality": "french", "movements": ["impressionism"]},
    "édouard manet": {"years": (1832, 1883), "nationality": "french", "movements": ["impressionism"]},
    "berthe morisot": {"years": (1841, 1895), "nationality": "french", "movements": ["impressionism"]},
    "mary cassatt": {"years": (1844, 1926), "nationality": "american", "movements": ["impressionism"]},
    "alfred sisley": {"years": (1839, 1899), "nationality": "french", "movements": ["impressionism"]},
    
    # Post-Impressionism
    "vincent van gogh": {"years": (1853, 1890), "nationality": "dutch", "movements": ["post-impressionism"]},
    "paul cézanne": {"years": (1839, 1906), "nationality": "french", "movements": ["post-impressionism"]},
    "paul gauguin": {"years": (1848, 1903), "nationality": "french", "movements": ["post-impressionism"]},
    "georges seurat": {"years": (1859, 1891), "nationality": "french", "movements": ["post-impressionism"]},
    "henri de toulouse-lautrec": {"years": (1864, 1901), "nationality": "french", "movements": ["post-impressionism"]},
    
    # Symbolism
    "gustav klimt": {"years": (1862, 1918), "nationality": "austrian", "movements": ["symbolism", "art nouveau"]},
    "edvard munch": {"years": (1863, 1944), "nationality": "norwegian", "movements": ["symbolism", "expressionism"]},
    
    # Fauvism
    "henri matisse": {"years": (1869, 1954), "nationality": "french", "movements": ["fauvism", "modernism"]},
    
    # Expressionism
    "wassily kandinsky": {"years": (1866, 1944), "nationality": "russian", "movements": ["expressionism", "abstract"]},
    "egon schiele": {"years": (1890, 1918), "nationality": "austrian", "movements": ["expressionism"]},
    
    # Cubism
    "pablo picasso": {"years": (1881, 1973), "nationality": "spanish", "movements": ["cubism", "modernism"]},
    "georges braque": {"years": (1882, 1963), "nationality": "french", "movements": ["cubism"]},
    
    # Surrealism
    "salvador dalí": {"years": (1904, 1989), "nationality": "spanish", "movements": ["surrealism"]},
    "rené magritte": {"years": (1898, 1967), "nationality": "belgian", "movements": ["surrealism"]},
    
    # American
    "winslow homer": {"years": (1836, 1910), "nationality": "american", "movements": ["realism"]},
    "john singer sargent": {"years": (1856, 1925), "nationality": "american", "movements": ["realism"]},
    "edward hopper": {"years": (1882, 1967), "nationality": "american", "movements": ["realism"]},
    "georgia o'keeffe": {"years": (1887, 1986), "nationality": "american", "movements": ["modernism"]},
    
    # British
    "thomas gainsborough": {"years": (1727, 1788), "nationality": "british", "movements": ["rococo"]},
    "joshua reynolds": {"years": (1723, 1792), "nationality": "british", "movements": ["rococo"]},
    "william hogarth": {"years": (1697, 1764), "nationality": "british", "movements": ["rococo"]},
}

# Famous paintings with their artists
FAMOUS_PAINTINGS = {
    "mona lisa": "leonardo da vinci",
    "the last supper": "leonardo da vinci",
    "the creation of adam": "michelangelo",
    "the school of athens": "raphael",
    "the birth of venus": "botticelli",
    "primavera": "botticelli",
    "the night watch": "rembrandt",
    "girl with a pearl earring": "johannes vermeer",
    "the milkmaid": "johannes vermeer",
    "the garden of earthly delights": "hieronymus bosch",
    "the starry night": "vincent van gogh",
    "sunflowers": "vincent van gogh",
    "the potato eaters": "vincent van gogh",
    "water lilies": "claude monet",
    "impression sunrise": "claude monet",
    "the scream": "edvard munch",
    "the kiss": "gustav klimt",
    "guernica": "pablo picasso",
    "les demoiselles d'avignon": "pablo picasso",
    "the persistence of memory": "salvador dalí",
    "the son of man": "rené magritte",
    "the great wave": "hokusai",
    "liberty leading the people": "eugène delacroix",
    "the raft of the medusa": "théodore géricault",
    "the third of may 1808": "francisco goya",
    "saturn devouring his son": "francisco goya",
    "the fighting temeraire": "j.m.w. turner",
    "wanderer above the sea of fog": "caspar david friedrich",
    "the hay wain": "john constable",
    "olympia": "édouard manet",
    "luncheon on the grass": "édouard manet",
    "a bar at the folies-bergère": "édouard manet",
    "the dance class": "edgar degas",
    "bal du moulin de la galette": "pierre-auguste renoir",
    "luncheon of the boating party": "pierre-auguste renoir",
    "a sunday afternoon on the island of la grande jatte": "georges seurat",
    "the card players": "paul cézanne",
    "mont sainte-victoire": "paul cézanne",
    "where do we come from": "paul gauguin",
    "the yellow christ": "paul gauguin",
    "nighthawks": "edward hopper",
    "american gothic": "grant wood",
}

# Art movements by time period
ART_MOVEMENTS_BY_PERIOD = {
    "1400s": ["early renaissance"],
    "1500s": ["high renaissance", "mannerism"],
    "1600s": ["baroque"],
    "1700s": ["rococo", "neoclassicism"],
    "1800s": ["romanticism", "realism", "impressionism", "post-impressionism", "symbolism"],
    "1900s": ["fauvism", "expressionism", "cubism", "surrealism", "abstract", "modernism"],
}


def get_artists_by_century(century: str) -> List[str]:
    """Get artists who were active in a given century."""
    if not century or len(century) < 4:
        return []
    
    # Extract century number (e.g., "1700s" -> 1700)
    try:
        century_start = int(century[:4])
    except ValueError:
        return []
    
    century_end = century_start + 99
    
    artists = []
    for artist, info in ARTIST_DATABASE.items():
        birth, death = info["years"]
        # Artist was active if their lifespan overlaps with the century
        if not (death < century_start or birth > century_end):
            artists.append(artist)
    
    return artists


def get_artists_by_nationality(nationality: str) -> List[str]:
    """Get artists by nationality."""
    nationality_lower = nationality.lower()
    artists = []
    
    for artist, info in ARTIST_DATABASE.items():
        if info["nationality"] == nationality_lower:
            artists.append(artist)
    
    return artists


def get_artists_by_movement(movement: str) -> List[str]:
    """Get artists by art movement."""
    movement_lower = movement.lower()
    artists = []
    
    for artist, info in ARTIST_DATABASE.items():
        if movement_lower in info["movements"]:
            artists.append(artist)
    
    return artists


def get_artist_search_terms(tags: Optional[List[str]] = None) -> List[str]:
    """Get smart artist search terms based on tags."""
    if not tags:
        # Default to famous impressionists and post-impressionists
        return ["monet", "renoir", "van gogh", "cézanne", "degas"]
    
    search_terms = []
    
    for tag in tags:
        tag_lower = tag.lower()
        
        # Check for century
        for century in ["1400s", "1500s", "1600s", "1700s", "1800s", "1900s"]:
            if century[:3] in tag_lower or century in tag_lower:
                artists = get_artists_by_century(century)
                search_terms.extend(artists[:10])  # Top 10 from that century
                break
        
        # Check for nationality
        for nationality in ["french", "italian", "dutch", "spanish", "german", "british", "american", "flemish"]:
            if nationality in tag_lower:
                artists = get_artists_by_nationality(nationality)
                search_terms.extend(artists[:10])
                break
        
        # Check for movement
        for movement in ["renaissance", "baroque", "rococo", "romanticism", "impressionism", "realism"]:
            if movement in tag_lower:
                artists = get_artists_by_movement(movement)
                search_terms.extend(artists[:10])
                break
        
        # Check for "european" - get mix of major European artists
        if "european" in tag_lower or "europe" in tag_lower:
            european_nationalities = ["french", "italian", "dutch", "spanish", "german", "flemish"]
            for nat in european_nationalities:
                artists = get_artists_by_nationality(nat)
                search_terms.extend(artists[:3])  # Top 3 from each
    
    # Remove duplicates while preserving order
    seen = set()
    unique_terms = []
    for term in search_terms:
        if term not in seen:
            seen.add(term)
            unique_terms.append(term)
    
    return unique_terms[:15]  # Limit to 15 artists


def get_painting_keywords() -> List[str]:
    """Get keywords for famous paintings."""
    return list(FAMOUS_PAINTINGS.keys())


def suggest_query_improvements(query: str) -> List[str]:
    """Suggest improved queries based on art knowledge."""
    query_lower = query.lower()
    suggestions = []
    
    # Check if query mentions a famous painting
    for painting, artist in FAMOUS_PAINTINGS.items():
        if painting in query_lower:
            suggestions.append(artist)
    
    # Check if query mentions an art movement
    for movement in ["impressionism", "baroque", "renaissance", "romanticism"]:
        if movement in query_lower:
            artists = get_artists_by_movement(movement)
            suggestions.extend(artists[:5])
    
    return suggestions
