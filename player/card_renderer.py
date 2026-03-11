"""SVG card loader and renderer for Arcanum's HTML/CSS tarot cards.

Loads card SVG illustrations from player/cards/svg/ and renders them
inline with theme-reactive CSS variables. Falls back to traditional
Rider-Waite images when an SVG card doesn't exist.
"""

import re
from pathlib import Path

CARDS_DIR = Path(__file__).parent / "cards" / "svg"

# Cache loaded SVG content to avoid re-reading files
_svg_cache: dict[str, str] = {}


def _load_card_svg(card_code: str) -> str | None:
    """Load and return the SVG illustration for a card, or None if not found.

    Args:
        card_code: The card filename code (e.g., 'm00', 'm17', 'c01')

    Returns:
        The inner SVG markup with prefixed gradient IDs, or None.
    """
    if card_code in _svg_cache:
        return _svg_cache[card_code]

    html_path = CARDS_DIR / f"{card_code}.html"
    if not html_path.exists():
        _svg_cache[card_code] = None
        return None

    raw = html_path.read_text()

    # Extract the SVG inside <div class="illustration">...</div>
    match = re.search(
        r'<div class="illustration">\s*(<svg.*?</svg>)\s*</div>',
        raw,
        re.DOTALL,
    )
    if not match:
        _svg_cache[card_code] = None
        return None

    svg = match.group(1)

    # Prefix gradient/filter IDs to avoid collisions when multiple cards
    # are on screen simultaneously. E.g., "sunglow" -> "m00-sunglow"
    # Find all id="..." declarations
    ids_found = re.findall(r'id="([^"]+)"', svg)
    for gid in ids_found:
        prefixed = f"{card_code}-{gid}"
        # Replace the id declaration
        svg = svg.replace(f'id="{gid}"', f'id="{prefixed}"')
        # Replace all url(#...) references
        svg = svg.replace(f"url(#{gid})", f"url(#{prefixed})")

    _svg_cache[card_code] = svg
    return svg


def has_svg_card(card_code: str) -> bool:
    """Check if an SVG card exists for the given code."""
    return (CARDS_DIR / f"{card_code}.html").exists()


def get_available_svg_cards() -> list[str]:
    """Return list of card codes that have SVG versions."""
    return [p.stem for p in CARDS_DIR.glob("*.html")]


# The shared card frame HTML — wraps any card's SVG illustration.
# Uses the same CSS classes as the standalone HTML files.
CARD_FRAME_TOP = """\
<div class="card-frame size-game" style="width:100%; height:100%;">
  <div class="border-outer"></div>
  <div class="border-inner"></div>
  <svg class="corner corner-tl" viewBox="0 0 40 40" fill="none">
    <path d="M0 40 L0 12 Q0 0 12 0 L40 0" stroke="var(--card-border)" stroke-width="1" fill="none" opacity="0.5"/>
    <circle cx="10" cy="10" r="2.5" stroke="var(--card-border)" stroke-width="0.5" fill="none" opacity="0.4"/>
    <circle cx="10" cy="10" r="1" fill="var(--card-border)" opacity="0.3"/>
  </svg>
  <svg class="corner corner-tr" viewBox="0 0 40 40" fill="none">
    <path d="M0 40 L0 12 Q0 0 12 0 L40 0" stroke="var(--card-border)" stroke-width="1" fill="none" opacity="0.5"/>
    <circle cx="10" cy="10" r="2.5" stroke="var(--card-border)" stroke-width="0.5" fill="none" opacity="0.4"/>
    <circle cx="10" cy="10" r="1" fill="var(--card-border)" opacity="0.3"/>
  </svg>
  <svg class="corner corner-bl" viewBox="0 0 40 40" fill="none">
    <path d="M0 40 L0 12 Q0 0 12 0 L40 0" stroke="var(--card-border)" stroke-width="1" fill="none" opacity="0.5"/>
    <circle cx="10" cy="10" r="2.5" stroke="var(--card-border)" stroke-width="0.5" fill="none" opacity="0.4"/>
    <circle cx="10" cy="10" r="1" fill="var(--card-border)" opacity="0.3"/>
  </svg>
  <svg class="corner corner-br" viewBox="0 0 40 40" fill="none">
    <path d="M0 40 L0 12 Q0 0 12 0 L40 0" stroke="var(--card-border)" stroke-width="1" fill="none" opacity="0.5"/>
    <circle cx="10" cy="10" r="2.5" stroke="var(--card-border)" stroke-width="0.5" fill="none" opacity="0.4"/>
    <circle cx="10" cy="10" r="1" fill="var(--card-border)" opacity="0.3"/>
  </svg>
  <div class="card-number">{number}</div>
  <div class="card-name">{name}</div>
  <div class="illustration">
"""

CARD_FRAME_BOTTOM = """\
  </div>
</div>
"""

# Roman numerals for Major Arcana
_ROMAN = [
    "0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI",
]


def render_svg_card_html(card, card_code: str) -> str | None:
    """Build the full card HTML (frame + illustration) for inline rendering.

    Args:
        card: A Card object with .name, .number, .suit, .reversed
        card_code: The card filename code (e.g., 'm00')

    Returns:
        Complete HTML string ready for ui.html(), or None if no SVG exists.
    """
    svg = _load_card_svg(card_code)
    if svg is None:
        return None

    # Card number display
    if card.suit == "major":
        number_display = _ROMAN[card.number] if card.number < len(_ROMAN) else str(card.number)
    else:
        number_display = str(card.number) if card.number <= 10 else ""

    frame_top = CARD_FRAME_TOP.format(number=number_display, name=card.name)

    return frame_top + svg + CARD_FRAME_BOTTOM
