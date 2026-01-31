"""Famous artists for prioritization."""

# List of well-known artists to prioritize in results
FAMOUS_ARTISTS = {
    # Renaissance (Italian)
    "leonardo da vinci", "leonardo", "michelangelo", "michelangelo buonarroti",
    "raphael", "raffaello sanzio", "titian", "tiziano vecellio", "botticelli",
    "sandro botticelli", "caravaggio", "michelangelo merisi da caravaggio",
    "donatello", "giotto", "giotto di bondone", "masaccio", "piero della francesca",
    "mantegna", "andrea mantegna", "bellini", "giovanni bellini", "tintoretto",
    "veronese", "paolo veronese", "correggio", "antonio da correggio",
    
    # Northern Renaissance
    "dürer", "albrecht dürer", "holbein", "hans holbein", "cranach", "lucas cranach",
    
    # Baroque
    "rembrandt", "rembrandt van rijn", "vermeer", "johannes vermeer", "rubens",
    "peter paul rubens", "velázquez", "diego velázquez", "el greco", "domenikos theotokopoulos",
    "poussin", "nicolas poussin", "bernini", "gian lorenzo bernini", "lorrain",
    "claude lorrain", "hals", "frans hals", "reni", "guido reni", "carracci",
    "annibale carracci", "artemisia gentileschi", "gentileschi",
    
    # Rococo
    "watteau", "jean-antoine watteau", "fragonard", "jean-honoré fragonard",
    "boucher", "françois boucher", "tiepolo", "giovanni battista tiepolo",
    "chardin", "jean-baptiste-siméon chardin", "canaletto", "giovanni antonio canal",
    
    # Neoclassicism
    "david", "jacques-louis david", "ingres", "jean-auguste-dominique ingres",
    "canova", "antonio canova", "vigée le brun", "élisabeth vigée le brun",
    
    # Romanticism
    "delacroix", "eugène delacroix", "géricault", "théodore géricault",
    "turner", "j.m.w. turner", "joseph mallord william turner",
    "friedrich", "caspar david friedrich", "goya", "francisco goya",
    "francisco de goya", "constable", "john constable", "blake", "william blake",
    "fuseli", "henry fuseli",
    
    # Realism
    "courbet", "gustave courbet", "millet", "jean-françois millet",
    "daumier", "honoré daumier", "corot", "jean-baptiste-camille corot",
    
    # Pre-Raphaelite
    "rossetti", "dante gabriel rossetti", "millais", "john everett millais",
    "hunt", "william holman hunt", "burne-jones", "edward burne-jones",
    
    # Impressionism
    "monet", "claude monet", "renoir", "pierre-auguste renoir",
    "degas", "edgar degas", "pissarro", "camille pissarro",
    "sisley", "alfred sisley", "manet", "édouard manet",
    "morisot", "berthe morisot", "cassatt", "mary cassatt",
    "caillebotte", "gustave caillebotte", "bazille", "frédéric bazille",
    
    # Post-Impressionism
    "van gogh", "vincent van gogh", "cézanne", "paul cézanne",
    "gauguin", "paul gauguin", "seurat", "georges seurat",
    "toulouse-lautrec", "henri de toulouse-lautrec", "signac", "paul signac",
    
    # Symbolism
    "moreau", "gustave moreau", "redon", "odilon redon",
    "klimt", "gustav klimt", "munch", "edvard munch",
    "böcklin", "arnold böcklin", "puvis de chavannes", "pierre puvis de chavannes",
    
    # Art Nouveau
    "mucha", "alphonse mucha", "beardsley", "aubrey beardsley",
    
    # Fauvism
    "matisse", "henri matisse", "derain", "andré derain",
    "vlaminck", "maurice de vlaminck", "dufy", "raoul dufy",
    
    # Expressionism
    "kirchner", "ernst ludwig kirchner", "nolde", "emil nolde",
    "kandinsky", "wassily kandinsky", "marc", "franz marc",
    "macke", "august macke", "heckel", "erich heckel",
    "schiele", "egon schiele", "kokoschka", "oskar kokoschka",
    
    # Cubism
    "picasso", "pablo picasso", "braque", "georges braque",
    "léger", "fernand léger", "gris", "juan gris",
    "delaunay", "robert delaunay", "sonia delaunay",
    
    # Futurism
    "boccioni", "umberto boccioni", "balla", "giacomo balla",
    "severini", "gino severini",
    
    # Dada & Surrealism
    "dalí", "salvador dalí", "magritte", "rené magritte",
    "miró", "joan miró", "ernst", "max ernst",
    "tanguy", "yves tanguy", "duchamp", "marcel duchamp",
    "man ray", "arp", "jean arp", "hans arp",
    
    # Abstract & Modernism
    "mondrian", "piet mondrian", "malevich", "kazimir malevich",
    "rothko", "mark rothko", "pollock", "jackson pollock",
    "de kooning", "willem de kooning", "klee", "paul klee",
    "albers", "josef albers", "newman", "barnett newman",
    "still", "clyfford still", "motherwell", "robert motherwell",
    
    # Dutch Golden Age
    "steen", "jan steen", "hobbema", "meindert hobbema",
    "ruisdael", "jacob van ruisdael", "ter borch", "gerard ter borch",
    "metsu", "gabriel metsu", "de hooch", "pieter de hooch",
    
    # Flemish
    "van eyck", "jan van eyck", "bruegel", "pieter bruegel",
    "pieter bruegel the elder", "memling", "hans memling",
    "van der weyden", "rogier van der weyden", "bosch", "hieronymus bosch",
    
    # Spanish
    "murillo", "bartolomé esteban murillo", "zurbarán", "francisco de zurbarán",
    "ribera", "jusepe de ribera", "sorolla", "joaquín sorolla",
    
    # British
    "gainsborough", "thomas gainsborough", "reynolds", "joshua reynolds",
    "hogarth", "william hogarth", "stubbs", "george stubbs",
    "lawrence", "thomas lawrence", "raeburn", "henry raeburn",
    
    # American
    "homer", "winslow homer", "sargent", "john singer sargent",
    "whistler", "james mcneill whistler", "eakins", "thomas eakins",
    "hopper", "edward hopper", "o'keeffe", "georgia o'keeffe",
    "wood", "grant wood", "benton", "thomas hart benton",
    "bellows", "george bellows", "sloan", "john sloan",
    
    # Russian
    "repin", "ilya repin", "levitan", "isaac levitan",
    "shishkin", "ivan shishkin", "aivazovsky", "ivan aivazovsky",
    
    # Scandinavian
    "zorn", "anders zorn", "krøyer", "peder severin krøyer",
    "hammershøi", "vilhelm hammershøi",
    
    # German
    "friedrich", "caspar david friedrich", "menzel", "adolph menzel",
    "liebermann", "max liebermann", "corinth", "lovis corinth",
    
    # Austrian
    "klimt", "gustav klimt", "schiele", "egon schiele",
    
    # Swiss
    "hodler", "ferdinand hodler", "böcklin", "arnold böcklin",
    
    # Mexican
    "rivera", "diego rivera", "kahlo", "frida kahlo",
    "orozco", "josé clemente orozco", "siqueiros", "david alfaro siqueiros",
    
    # Japanese (Western-style)
    "hokusai", "katsushika hokusai", "hiroshige", "utagawa hiroshige",
    "utamaro", "kitagawa utamaro",
    
    # Other Notable
    "sargent", "john singer sargent", "alma-tadema", "lawrence alma-tadema",
    "leighton", "frederic leighton", "waterhouse", "john william waterhouse",
    "bouguereau", "william-adolphe bouguereau", "gérôme", "jean-léon gérôme",
    "meissonier", "jean-louis-ernest meissonier", "cabanel", "alexandre cabanel",
}


def is_famous_artist(artist_name: str) -> bool:
    """Check if an artist is in the famous artists list."""
    if not artist_name:
        return False
    artist_lower = artist_name.lower().strip()
    
    # Check exact match
    if artist_lower in FAMOUS_ARTISTS:
        return True
    
    # Check if any famous artist name is contained in the artist name
    for famous in FAMOUS_ARTISTS:
        if famous in artist_lower or artist_lower in famous:
            return True
    
    return False


def get_artist_priority(artist_name: str) -> int:
    """Get priority score for an artist (higher = more famous)."""
    if is_famous_artist(artist_name):
        return 100
    return 0
