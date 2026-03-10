"""
arcanum_theme.py — Drop-in theme system for Arcanum's NiceGUI frontend.

Usage:
    from arcanum_theme import Theme, inject_theme, sidebar_layout, divider, staggered_text

    # In your main page setup:
    inject_theme()

    # Wrap your entire UI in the sidebar layout:
    sidebar, content = sidebar_layout(theme="default")

    # Switch themes for dream sessions:
    sidebar, content = sidebar_layout(theme="cyberpunk")
"""

from nicegui import ui


# ============================================================================
# CHOICE CATEGORIZATION (shared utility)
# ============================================================================


def categorize_choices(choices: list) -> dict[str, list[tuple[int, dict]]]:
    """Sort a list of passage choices into buckets by their tags.

    Returns a dict with keys: 'client', 'special', 'meta', 'regular'.
    Each value is a list of (original_index, choice_dict) tuples.
    """
    buckets: dict[str, list[tuple[int, dict]]] = {
        "client": [],
        "special": [],
        "meta": [],
        "regular": [],
    }

    for i, choice in enumerate(choices):
        tags = choice.get("tags", [])
        has_client = any(tag.startswith("CLIENT") for tag in tags)
        is_special = any("SPECIAL" in tag for tag in tags)
        is_meta = any(tag.startswith("META") for tag in tags)

        if has_client and is_special:
            buckets["special"].append((i, choice))
        elif has_client:
            buckets["client"].append((i, choice))
        elif is_meta:
            buckets["meta"].append((i, choice))
        else:
            buckets["regular"].append((i, choice))

    return buckets


# ============================================================================
# COLOR PALETTES
# ============================================================================

THEMES = {
    "default": {
        "name": "Real World",
        # Backgrounds
        "sidebar_bg": "#1a0e2e",
        "sidebar_accent": "#2d1b4e",
        "reading_bg": "#0f0a18",
        "reading_panel": "#16102a",
        # Gold family
        "gold": "#c9a84c",
        "gold_light": "#e2c97e",
        "gold_dim": "#8a7235",
        # Accent (purple)
        "accent": "#6b3fa0",
        "accent_light": "#9b6fd0",
        # Text
        "text": "#d4cde0",
        "text_muted": "#8a7ea0",
        "text_bright": "#f0ecf5",
        # Fonts
        "heading_font": "'Cormorant Garamond', 'Garamond', serif",
        "body_font": "'EB Garamond', 'Georgia', serif",
        # UI labels
        "trust_labels": ["Wary", "Cautious", "Open", "Growing", "Deep"],
        "session_fmt": "Session {n} of {total}",
        "notes_label": "Notes",
        "save_label": "Save",
        "settings_label": "Settings",
    },
    "cyberpunk": {
        "name": "Dream — Nyx",
        "sidebar_bg": "#0a0a12",
        "sidebar_accent": "#0f1029",
        "reading_bg": "#06060e",
        "reading_panel": "#0c0c1a",
        "gold": "#00e5ff",
        "gold_light": "#80f0ff",
        "gold_dim": "#0088a0",
        "accent": "#ff2d78",
        "accent_light": "#ff6fa3",
        "text": "#b8c4d8",
        "text_muted": "#5a6a80",
        "text_bright": "#e8f0ff",
        "heading_font": "'Share Tech Mono', 'Courier New', monospace",
        "body_font": "'IBM Plex Sans', 'Helvetica Neue', sans-serif",
        "trust_labels": ["NULL", "PING", "SYNC", "BONDED", "LINKED"],
        "session_fmt": "SES.{n}/{total}",
        "notes_label": "// LOGS",
        "save_label": "SAVE",
        "settings_label": "SYS",
        "dream_badge": "◆ DREAM MODE",
        "choice_prefix": "",
    },
    "gothic": {
        "name": "Dream — The Manor House",
        "sidebar_bg": "#0e0c0f",
        "sidebar_accent": "#1a161e",
        "reading_bg": "#0a090c",
        "reading_panel": "#12101a",
        "gold": "#8a8495",
        "gold_light": "#b0a8be",
        "gold_dim": "#5a5464",
        "accent": "#7a2030",
        "accent_light": "#a83848",
        "text": "#c0bcc8",
        "text_muted": "#6a6474",
        "text_bright": "#e0dce8",
        "heading_font": "'Playfair Display', 'Georgia', serif",
        "body_font": "'Crimson Text', 'Georgia', serif",
        "trust_labels": ["Uneasy", "Wary", "Tolerant", "Confiding", "Entangled"],
        "session_fmt": "Session {n} of {total}",
        "notes_label": "Observations",
        "save_label": "Save",
        "settings_label": "Settings",
        "dream_badge": "◆ The Manor House",
        "choice_prefix": "✦",
    },
    "kind": {
        "name": "Dream — The Kind",
        "sidebar_bg": "#1a1612",
        "sidebar_accent": "#241e18",
        "reading_bg": "#12110e",
        "reading_panel": "#1a1814",
        "gold": "#b89a5a",
        "gold_light": "#d4c8a0",
        "gold_dim": "#7a6b4a",
        "accent": "#8b5e3c",
        "accent_light": "#c07858",
        "text": "#d4ccc0",
        "text_muted": "#8a8070",
        "text_bright": "#ece6da",
        "moss": "#5a7a56",
        "moss_light": "#7a9a74",
        "moss_dim": "#3a5238",
        "heading_font": "'Libre Baskerville', 'Georgia', serif",
        "body_font": "'Literata', 'Georgia', serif",
        "trust_labels": ["Browsing", "Lingering", "Settling In", "A Regular", "Family"],
        "session_fmt": "Session {n} of {total}",
        "notes_label": "Notes",
        "save_label": "Save",
        "settings_label": "Settings",
        "dream_badge": "◆ The Kind — Rewind, OR",
        "choice_prefix": "❧",
        "trust_label_name": "Rapport",
    },
    "weird_west": {
        "name": "Dream — The Ace of Spades",
        "sidebar_bg": "#1a1410",
        "sidebar_accent": "#241c14",
        "reading_bg": "#14110c",
        "reading_panel": "#1c1812",
        "gold": "#c8944a",
        "gold_light": "#ddb878",
        "gold_dim": "#8a6a3a",
        "accent": "#a03828",
        "accent_light": "#c85040",
        "text": "#d8ccb8",
        "text_muted": "#8a7e6e",
        "text_bright": "#ece0cc",
        "heading_font": "'Bitter', 'Georgia', serif",
        "body_font": "'Vollkorn', 'Georgia', serif",
        "trust_labels": [
            "Stranger",
            "Acquaintance",
            "Drinking Buddy",
            "Trusted",
            "Blood Oath",
        ],
        "session_fmt": "Hand {n} of {total}",
        "notes_label": "Ledger",
        "save_label": "Save",
        "settings_label": "Settings",
        "dream_badge": "◆ The Ace of Spades",
        "choice_prefix": "▸",
        "trust_label_name": "Standing",
    },
}


def get_theme(name: str = "default") -> dict:
    """Get a theme palette by name."""
    return THEMES.get(name, THEMES["default"])


# ============================================================================
# CSS INJECTION — call once at startup
# ============================================================================


def inject_theme():
    """Inject fonts, CSS, and animations into the page head.
    Call this ONCE at the top of your NiceGUI app, before building any UI.

    Expects arcanum_styles.css to be served as a static file.
    Set up with:
        app.add_static_files("/theme", str(Path(__file__).parent))
    """
    from pathlib import Path

    # Serve this directory as static files (if not already done)
    try:
        from nicegui import app

        theme_dir = str(Path(__file__).parent)
        app.add_static_files("/theme", theme_dir)
    except Exception:
        pass  # May already be registered

    # Load the external stylesheet (shared=True so it works with @ui.page)
    ui.add_head_html(
        '<link rel="stylesheet" href="/theme/arcanum_styles.css">', shared=True
    )


# ============================================================================
# THEME SWITCHING (for dream sessions)
# ============================================================================


async def set_theme(theme_name: str):
    """Switch the active CSS theme. Call this when entering/leaving dream sessions.

    Args:
        theme_name: "default" or "cyberpunk" (or any key in THEMES)
    """
    if theme_name == "default":
        await ui.run_javascript(
            "document.documentElement.removeAttribute('data-theme');"
        )
    else:
        await ui.run_javascript(
            f"document.documentElement.setAttribute('data-theme', '{theme_name}');"
        )


# ============================================================================
# SVG MOTIFS — Sidebar brand marks for each theme
# ============================================================================


def motif(theme: str = "default", size: int = 56):
    """Render the appropriate SVG brand motif for the current theme.

    Args:
        theme: "default", "cyberpunk", "gothic", or "kind"
        size: Base size in pixels (height scales proportionally)
    """
    if theme == "cyberpunk":
        _motif_cyberpunk(size)
    elif theme == "gothic":
        _motif_gothic(size)
    elif theme == "kind":
        _motif_kind(size)
    elif theme == "weird_west":
        _motif_weird_west(size)
    else:
        _motif_default(size)


def _motif_default(size: int = 56):
    """Compass-rose tarot card back — default theme."""
    w = size
    h = int(size * 1.5)
    ui.html(
        f"""
    <svg width="{w}" height="{h}" viewBox="0 0 120 180" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="2" y="2" width="116" height="176" rx="8"
            stroke="var(--gold)" stroke-width="1.5" fill="var(--sidebar-bg)"/>
      <rect x="8" y="8" width="104" height="164" rx="5"
            stroke="var(--gold-dim)" stroke-width="0.5" fill="none"/>
      <!-- Circles -->
      <circle cx="60" cy="90" r="30" stroke="var(--gold)" stroke-width="0.75" fill="none"/>
      <circle cx="60" cy="90" r="20" stroke="var(--gold-dim)" stroke-width="0.5" fill="none"/>
      <circle cx="60" cy="90" r="3" fill="var(--gold)"/>
      <!-- Cardinal rays -->
      <line x1="60" y1="68" x2="60" y2="48" stroke="var(--gold)" stroke-width="1"/>
      <line x1="60" y1="112" x2="60" y2="132" stroke="var(--gold)" stroke-width="1"/>
      <line x1="38" y1="90" x2="18" y2="90" stroke="var(--gold)" stroke-width="1"/>
      <line x1="82" y1="90" x2="102" y2="90" stroke="var(--gold)" stroke-width="1"/>
      <!-- Diagonal rays -->
      <line x1="45.9" y1="75.9" x2="38.8" y2="68.8" stroke="var(--gold-dim)" stroke-width="0.5"/>
      <line x1="74.1" y1="75.9" x2="81.2" y2="68.8" stroke="var(--gold-dim)" stroke-width="0.5"/>
      <line x1="45.9" y1="104.1" x2="38.8" y2="111.2" stroke="var(--gold-dim)" stroke-width="0.5"/>
      <line x1="74.1" y1="104.1" x2="81.2" y2="111.2" stroke="var(--gold-dim)" stroke-width="0.5"/>
      <!-- Crescents -->
      <path d="M50 40 Q60 30 70 40" stroke="var(--gold-dim)" stroke-width="0.75" fill="none"/>
      <path d="M50 140 Q60 150 70 140" stroke="var(--gold-dim)" stroke-width="0.75" fill="none"/>
      <!-- Corner dots -->
      <circle cx="20" cy="24" r="4" stroke="var(--gold-dim)" stroke-width="0.5" fill="none"/>
      <circle cx="20" cy="24" r="1.5" fill="var(--gold-dim)"/>
      <circle cx="100" cy="24" r="4" stroke="var(--gold-dim)" stroke-width="0.5" fill="none"/>
      <circle cx="100" cy="24" r="1.5" fill="var(--gold-dim)"/>
      <circle cx="20" cy="156" r="4" stroke="var(--gold-dim)" stroke-width="0.5" fill="none"/>
      <circle cx="20" cy="156" r="1.5" fill="var(--gold-dim)"/>
      <circle cx="100" cy="156" r="4" stroke="var(--gold-dim)" stroke-width="0.5" fill="none"/>
      <circle cx="100" cy="156" r="1.5" fill="var(--gold-dim)"/>
    </svg>
    """,
        sanitize=False,
    )


def _motif_cyberpunk(size: int = 56):
    """Hexagonal eye with circuit traces — cyberpunk theme."""
    ui.html(
        f"""
    <svg width="{size}" height="{size}" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Hex frames -->
      <polygon points="40,4 72,22 72,58 40,76 8,58 8,22"
               stroke="var(--gold)" stroke-width="1" fill="none"/>
      <polygon points="40,12 64,26 64,54 40,68 16,54 16,26"
               stroke="var(--gold-dim)" stroke-width="0.5" fill="none"/>
      <!-- Eye -->
      <ellipse cx="40" cy="40" rx="16" ry="10"
               stroke="var(--gold)" stroke-width="0.75" fill="none"/>
      <circle cx="40" cy="40" r="4" fill="var(--accent)" opacity="0.8"/>
      <circle cx="40" cy="40" r="1.5" fill="var(--gold-light)"/>
      <!-- Circuit traces -->
      <line x1="8" y1="22" x2="0" y2="18" stroke="var(--gold-dim)" stroke-width="0.5"/>
      <line x1="72" y1="22" x2="80" y2="18" stroke="var(--gold-dim)" stroke-width="0.5"/>
      <line x1="8" y1="58" x2="0" y2="62" stroke="var(--gold-dim)" stroke-width="0.5"/>
      <line x1="72" y1="58" x2="80" y2="62" stroke="var(--gold-dim)" stroke-width="0.5"/>
      <!-- Scan brackets -->
      <line x1="24" y1="40" x2="20" y2="40" stroke="var(--accent)" stroke-width="0.5" opacity="0.6"/>
      <line x1="56" y1="40" x2="60" y2="40" stroke="var(--accent)" stroke-width="0.5" opacity="0.6"/>
    </svg>
    """,
        sanitize=False,
    )


def _motif_gothic(size: int = 56):
    """Cathedral arch with rose cross — gothic theme."""
    w = size
    h = int(size * 1.3)
    ui.html(
        f"""
    <svg width="{w}" height="{h}" viewBox="0 0 56 73" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Outer gothic arch -->
      <path d="M28 4 Q4 20 4 45 L4 69 L52 69 L52 45 Q52 20 28 4Z"
            stroke="var(--gold)" stroke-width="1" fill="none"/>
      <!-- Inner arch -->
      <path d="M28 10 Q10 24 10 44 L10 63 L46 63 L46 44 Q46 24 28 10Z"
            stroke="var(--gold-dim)" stroke-width="0.5" fill="none"/>
      <!-- Cross -->
      <line x1="28" y1="24" x2="28" y2="52" stroke="var(--gold)" stroke-width="0.75"/>
      <line x1="18" y1="36" x2="38" y2="36" stroke="var(--gold)" stroke-width="0.75"/>
      <!-- Rose at crossing -->
      <circle cx="28" cy="36" r="5" stroke="var(--accent)" stroke-width="0.75" fill="none"/>
      <circle cx="28" cy="36" r="2" fill="var(--accent)" opacity="0.6"/>
      <!-- Rose petals (subtle) -->
      <circle cx="28" cy="31" r="1" fill="var(--accent)" opacity="0.25"/>
      <circle cx="28" cy="41" r="1" fill="var(--accent)" opacity="0.25"/>
      <circle cx="23" cy="36" r="1" fill="var(--accent)" opacity="0.25"/>
      <circle cx="33" cy="36" r="1" fill="var(--accent)" opacity="0.25"/>
      <!-- Base ornaments -->
      <circle cx="14" cy="56" r="2.5" stroke="var(--gold-dim)" stroke-width="0.4" fill="none"/>
      <circle cx="14" cy="56" r="0.8" fill="var(--gold-dim)" opacity="0.5"/>
      <circle cx="42" cy="56" r="2.5" stroke="var(--gold-dim)" stroke-width="0.4" fill="none"/>
      <circle cx="42" cy="56" r="0.8" fill="var(--gold-dim)" opacity="0.5"/>
      <!-- Pointed finial at top -->
      <line x1="28" y1="4" x2="28" y2="0" stroke="var(--gold-dim)" stroke-width="0.5"/>
      <circle cx="28" cy="0" r="1" fill="var(--gold-dim)" opacity="0.4"/>
    </svg>
    """,
        sanitize=False,
    )


def _motif_kind(size: int = 56):
    """Douglas fir silhouette — The Kind theme.
    Inspired by the Cascadia Doug flag: a lone-standing fir,
    endurance and resilience, love of place.
    """
    w = size
    h = int(size * 1.4)
    ui.html(
        f"""
    <svg width="{w}" height="{h}" viewBox="0 0 56 78" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Trunk -->
      <rect x="25.5" y="58" width="5" height="14" rx="1"
            fill="var(--moss-dim, #3a5238)" opacity="0.7"/>
      <!-- Tree silhouette - layered Doug fir branches -->
      <polygon points="28,4 6,36 12,36 4,48 14,48 2,58 54,58 42,48 52,48 44,36 50,36"
               fill="var(--moss, #5a7a56)" opacity="0.85"/>
      <!-- Subtle inner trunk line -->
      <line x1="28" y1="10" x2="28" y2="58"
            stroke="var(--moss-dim, #3a5238)" stroke-width="0.5" opacity="0.3"/>
      <!-- Canopy highlight layers -->
      <polygon points="28,6 8,32 48,32"
               fill="var(--moss-dim, #3a5238)" opacity="0.5"/>
      <polygon points="28,2 12,26 44,26"
               fill="var(--moss, #5a7a56)" opacity="0.7"/>
      <!-- Ground line -->
      <line x1="16" y1="72" x2="40" y2="72"
            stroke="var(--gold-dim)" stroke-width="0.5" opacity="0.3"/>
      <!-- Roots reaching out -->
      <path d="M24 72 Q20 76 16 76"
            stroke="var(--gold-dim)" stroke-width="0.3" fill="none" opacity="0.25"/>
      <path d="M32 72 Q36 76 40 76"
            stroke="var(--gold-dim)" stroke-width="0.3" fill="none" opacity="0.25"/>
    </svg>
    """,
        sanitize=False,
    )


def _motif_weird_west(size: int = 56):
    """Sheriff's star badge — Weird West theme.
    Six-pointed star inside a circle: lawman's badge meets mystical hexagram.
    """
    w = size
    h = int(size * 1.15)
    # Compute six-pointed star path
    import math

    cx, cy = 28, 32
    outer_r, inner_r = 22, 10
    points = []
    for i in range(12):
        angle = (math.pi * i) / 6 - math.pi / 2
        r = outer_r if i % 2 == 0 else inner_r
        x = cx + math.cos(angle) * r
        y = cy + math.sin(angle) * r
        points.append(f"{x:.1f},{y:.1f}")
    star_path = "M" + "L".join(points) + "Z"
    # Tip dots
    tip_dots = ""
    for i in range(6):
        angle = (math.pi * 2 * i) / 6 - math.pi / 2
        x = cx + math.cos(angle) * (outer_r + 3)
        y = cy + math.sin(angle) * (outer_r + 3)
        tip_dots += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1" fill="var(--gold-dim)" opacity="0.4"/>'

    ui.html(
        f"""
    <svg width="{w}" height="{h}" viewBox="0 0 56 64" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Outer circle -->
      <circle cx="{cx}" cy="{cy}" r="26" stroke="var(--gold-dim)" stroke-width="1" fill="none" opacity="0.5"/>
      <circle cx="{cx}" cy="{cy}" r="24" stroke="var(--gold)" stroke-width="0.5" fill="none" opacity="0.3"/>
      <!-- Six-pointed star -->
      <path d="{star_path}" stroke="var(--gold)" stroke-width="1.2" fill="none"/>
      <!-- Inner circle -->
      <circle cx="{cx}" cy="{cy}" r="6" stroke="var(--gold-dim)" stroke-width="0.5" fill="none"/>
      <circle cx="{cx}" cy="{cy}" r="2.5" fill="var(--accent)" opacity="0.6"/>
      <!-- Tip dots -->
      {tip_dots}
      <!-- Badge plate -->
      <line x1="14" y1="58" x2="42" y2="58" stroke="var(--gold-dim)" stroke-width="0.5" opacity="0.3"/>
    </svg>
    """,
        sanitize=False,
    )


# ============================================================================
# HELPER COMPONENTS
# ============================================================================


def divider(width: str = "100%"):
    """Render a gold dot divider."""
    with ui.element("div").classes("arc-divider").style(f"width: {width}"):
        ui.element("div").classes("arc-divider-line left")
        ui.element("div").classes("arc-divider-dot")
        ui.element("div").classes("arc-divider-line right")


def section_label(text: str, dream: bool = False):
    """Render a small uppercase section label (e.g., 'Prologue', 'Session 1')."""
    cls = "arc-label"
    if dream:
        cls += " arc-accent-text"
    ui.label(text).classes(cls)


def heading(text: str, size: str = "28px"):
    """Render a passage heading."""
    ui.label(text).classes("arc-subheading").style(
        f"font-size: {size}; margin: 8px 0 24px 0;"
    )


def passage_text(content: str, bright: bool = False):
    """Render a paragraph of story text."""
    cls = "arc-body"
    if bright:
        cls += " arc-bright"
    ui.label(content).classes(cls).style("margin-bottom: 18px;")


def choice_prompt(text: str = "What do you do?"):
    """Render the choice prompt label."""
    ui.label(text).classes("arc-heading").style(
        "font-size: 18px; margin: 20px 0 16px 0; letter-spacing: 1px;"
    )


def choice_button(text: str, on_click, prefix: str = "›"):
    """Render a single story choice."""
    with ui.element("button").classes("arc-choice").on("click", on_click):
        ui.html(f'<span class="arc-choice-prefix">{prefix}</span> {text}')


def meta_choice_button(text: str, on_click):
    """Render a subtle meta choice (e.g., save, return to desk)."""
    with ui.element("button").classes("arc-meta-choice").on("click", on_click):
        ui.label(text)


def client_info_strip(
    client: str, session: int, total: int, trust: int, theme: str = "default"
):
    """Render the client info bar at the top of reading sessions."""
    t = get_theme(theme)
    is_cyber = theme == "cyberpunk"

    with ui.element("div").classes("arc-client-strip"):
        # Left: client name + session
        with ui.row().classes("items-center gap-4"):
            ui.label(client).classes("arc-heading").style(
                "font-size: 14px; letter-spacing: 2px;"
            )
            session_text = t["session_fmt"].format(n=session, total=total)
            ui.label(session_text).style(
                f"font-family: {t['heading_font']}; font-size: 12px; "
                f"color: {t['text_muted']}; letter-spacing: 1px;"
            )

        # Right: trust meter
        with ui.row().classes("items-center gap-2"):
            label = "LINK:" if is_cyber else "Trust:"
            ui.label(label).style(
                f"font-family: {t['heading_font']}; font-size: 11px; "
                f"color: {t['text_muted']}; letter-spacing: 1px; text-transform: uppercase;"
            )
            with ui.row().classes("gap-1"):
                for i in range(5):
                    dot_cls = (
                        "arc-trust-dot filled" if i < trust else "arc-trust-dot empty"
                    )
                    ui.element("div").classes(dot_cls)
            trust_label = (
                t["trust_labels"][min(trust, len(t["trust_labels"])) - 1]
                if trust > 0
                else ""
            )
            ui.label(trust_label).style(
                f"font-family: {t['heading_font']}; font-size: 11px; "
                f"color: {t['gold_dim']}; margin-left: 4px;"
            )


def stat_row(label: str, value: str):
    """Render a sidebar stat row (e.g., Reputation: Newcomer)."""
    with ui.element("div").classes("arc-stat-row"):
        ui.label(label).classes("arc-stat-label")
        ui.label(value).classes("arc-stat-value")


def card_detail_panel(
    title: str, position: str, interpretation: str, theme: str = "default"
):
    """Render an inline card interpretation panel (replaces drawer for readings)."""
    t = get_theme(theme)

    with ui.element("div").classes("arc-card-detail arc-fade-in"):
        ui.label(title).classes("arc-heading").style(
            "font-size: 20px; margin-bottom: 4px;"
        )
        ui.label(f"Position: {position}").classes("arc-label").style(
            "margin-bottom: 16px;"
        )
        divider()
        ui.label(interpretation).classes("arc-body").style("margin-top: 16px;")


# ============================================================================
# STAGGERED TEXT REVEAL (JavaScript-driven)
# ============================================================================


def inject_stagger_script():
    """Inject the JS that powers staggered paragraph reveals.
    Call once after inject_theme().
    """
    ui.add_head_html(
        """
    <script>
    function revealStaggered(containerId, delayMs) {
        const container = document.getElementById(containerId);
        if (!container) return;
        const paragraphs = container.querySelectorAll('.arc-stagger-p');
        paragraphs.forEach((p, i) => {
            setTimeout(() => {
                p.classList.add('visible');
            }, (i + 1) * (delayMs || 180));
        });
    }
    </script>
    """,
        shared=True,
    )


async def staggered_reveal(container_id: str, delay_ms: int = 180):
    """Trigger the staggered reveal animation for paragraphs in a container.
    Call this AFTER rendering all arc-stagger-p elements inside the container.
    """
    await ui.run_javascript(f"revealStaggered('{container_id}', {delay_ms});")


# ============================================================================
# LAYOUT BUILDERS
# ============================================================================


def landing_page(on_begin, on_continue):
    """Build the complete landing page."""
    with ui.element("div").classes("arc-landing"):
        # Card motif placeholder (SVG or image)
        divider(width="200px")

        ui.label("ARCANUM").classes("arc-landing-title")
        ui.label("A Digital Cartomancer's Tale").classes("arc-landing-subtitle")

        divider(width="200px")

        with ui.column().classes("gap-3 mt-4"):
            with ui.element("button").classes("arc-btn-primary").on("click", on_begin):
                ui.label("Begin Reading")
            with (
                ui.element("button")
                .classes("arc-btn-secondary")
                .on("click", on_continue)
            ):
                ui.label("Continue Journey")


def sidebar_layout(theme: str = "default"):
    """Create the two-panel sidebar + content layout.

    Returns:
        (sidebar_container, content_container) — use `with` on each to add children.

    Example:
        sidebar, content = sidebar_layout(theme="default")
        with sidebar:
            # sidebar nav, stats, notes
            ...
        with content:
            # story text, cards, choices
            ...
    """
    # Outer flex container
    outer = ui.row().classes("w-full min-h-screen m-0 p-0").style("gap: 0;")

    with outer:
        sidebar = ui.element("div").classes("arc-sidebar")
        content = ui.element("div").classes("arc-content")

    return sidebar, content


def build_sidebar(sidebar, stats: dict, nav_items: list = None, theme: str = "default"):
    """Populate a sidebar container with standard Arcanum chrome.

    Args:
        sidebar: The sidebar container from sidebar_layout()
        stats: Dict with keys like 'reputation', 'clients', 'savings'
        nav_items: List of {"label": "...", "on_click": fn, "active": bool}
        theme: Current theme name
    """
    t = get_theme(theme)

    with sidebar:
        # Brand motif
        with ui.element("div").style("margin-bottom: 8px; opacity: 0.85;"):
            motif(theme=theme, size=56)

        # Title
        ui.label("ARCANUM").classes("arc-sidebar-title")

        # Dream badge (if not default)
        dream_badge = t.get("dream_badge", "")
        if dream_badge:
            ui.label(dream_badge).classes("arc-dream-badge")

        # ui.label("by katehlouie").classes("arc-sidebar-byline")

        divider(width="80%")

        # Navigation
        if nav_items:
            for item in nav_items:
                cls = "arc-nav-btn"
                if item.get("active"):
                    cls += " active"
                with ui.element("button").classes(cls).on("click", item["on_click"]):
                    ui.label(item["label"])

        divider(width="80%")

        # Stats
        with ui.element("div").style("width: 100%; padding: 0 8px;"):
            for key, val in stats.items():
                stat_row(key, str(val))

        divider(width="80%")

        # Bottom buttons (pushed to bottom with spacer)
        ui.element("div").style("flex: 1;")  # spacer
        with ui.row().classes("gap-4"):
            ui.label(t["save_label"]).style(
                f"font-family: {t['heading_font']}; font-size: 11px; "
                f"color: {t['text_muted']}; letter-spacing: 1px; "
                "text-transform: uppercase; cursor: pointer;"
            )
            ui.label(t["settings_label"]).style(
                f"font-family: {t['heading_font']}; font-size: 11px; "
                f"color: {t['text_muted']}; letter-spacing: 1px; "
                "text-transform: uppercase; cursor: pointer;"
            )


# ============================================================================
# READER'S DESK COMPONENTS
# ============================================================================


def desk_stat_card(label: str, value: str, sub: str = ""):
    """Render a compact stat card for the desk header row."""
    with ui.element("div").classes("arc-desk-stat"):
        ui.label(label).classes("arc-desk-stat-label")
        ui.label(value).classes("arc-desk-stat-value")
        if sub:
            ui.label(sub).classes("arc-desk-stat-sub")


def xp_bar(current: int, max_xp: int):
    """Render an XP progress bar."""
    pct = min((current / max_xp * 100), 100) if max_xp > 0 else 0
    with ui.row().classes("items-center gap-3 w-full"):
        with ui.element("div").classes("arc-xp-track"):
            ui.element("div").classes("arc-xp-fill").style(f"width: {pct}%;")
        ui.label(f"{current}/{max_xp} XP").classes("arc-xp-label")


def desk_tab(label: str, active: bool, on_click, count: int = 0, icon: str = ""):
    """Render a tab button for the desk tab bar."""
    cls = "arc-tab active" if active else "arc-tab"
    with ui.element("button").classes(cls).on("click", on_click):
        if icon:
            ui.html(f'<span style="font-size:14px">{icon}</span>')
        ui.html(label)
        if count > 0:
            ui.html(f'<span class="arc-tab-badge">{count}</span>')


def desk_client_card(
    name: str,
    flavor: str,
    session_text: str,
    trust: int,
    on_click,
    is_special: bool = False,
    available: bool = True,
    dream_tag: str = "",
):
    """Render a client card on the Reader's Desk.

    Args:
        name: Client name
        flavor: Short description / flavor text
        session_text: e.g., "Session 2 of 3"
        trust: Trust level 0-5
        on_click: Callback when clicked (only fires if available)
        is_special: True for dream clients
        available: False to dim the card
        dream_tag: Label like "◆ Dream Client" for special clients
    """
    cls = "arc-client-card"
    if is_special:
        cls += " special"
    if not available:
        cls += " dimmed"

    card = ui.element("div").classes(cls)
    if available:
        card.on("click", on_click)

    with card:
        # Top row: name + trust
        with ui.row().classes("w-full justify-between items-start"):
            with ui.column().style("gap: 2px;"):
                if dream_tag:
                    ui.label(dream_tag).classes("arc-dream-tag")
                ui.label(name).classes("arc-client-name")
            with ui.column().classes("items-end").style("gap: 4px;"):
                # Trust dots
                with ui.row().style("gap: 3px;"):
                    for i in range(5):
                        dot_cls = (
                            "arc-trust-dot filled"
                            if i < trust
                            else "arc-trust-dot empty"
                        )
                        ui.element("div").classes(dot_cls)
                ui.label(session_text).classes("arc-client-meta")

        # Flavor text
        if flavor:
            ui.label(flavor).classes("arc-client-flavor")


def desk_note_card(text: str, source: str, category: str = "observation"):
    """Render a note card with category indicator.

    Args:
        text: The note text
        source: Where the note came from (e.g., "Session 1 — Mrs. Chen")
        category: "observation", "insight", or "anomaly"
    """
    cat_colors = {
        "observation": "var(--gold-dim)",
        "insight": "var(--gold)",
        "anomaly": "var(--accent-light)",
    }
    dot_color = cat_colors.get(category, "var(--gold-dim)")

    cls = f"arc-desk-note {category}"
    with ui.element("div").classes(cls):
        with ui.row().classes("items-center gap-2").style("margin-bottom: 4px;"):
            ui.element("div").classes("arc-note-category-dot").style(
                f"background: {dot_color};"
            )
            ui.label(category).classes("arc-note-category-label")
        ui.label(text).classes("arc-body").style("font-size: 14px; margin-bottom: 4px;")
        ui.label(source).classes("arc-note-source")


def desk_filter_chip(label: str, active: bool, on_click):
    """Render a filter chip for the notes tab."""
    cls = "arc-filter-chip active" if active else "arc-filter-chip"
    with ui.element("button").classes(cls).on("click", on_click):
        ui.label(label)


def desk_artifact_card(name: str, description: str, origin: str, on_click):
    """Render an artifact card in the list view."""
    with ui.element("div").classes("arc-artifact-card").on("click", on_click):
        ui.label(name).classes("arc-artifact-name")
        ui.label(description).classes("arc-client-flavor")  # reuse italic muted style
        ui.label(origin).classes("arc-artifact-origin")


def desk_artifact_detail(artifact_data: dict, on_back):
    """Render the full artifact detail view.

    Args:
        artifact_data: Dict with name, description, lore, origin_character, origin_session
        on_back: Callback for the back button
    """
    with ui.element("div").classes("arc-fade-in"):
        with ui.element("button").classes("arc-back-link").on("click", on_back):
            ui.label("← Back to collection")

        ui.label(artifact_data.get("name", "")).classes("arc-subheading").style(
            "font-size: 28px; margin-bottom: 8px; letter-spacing: 1px;"
        )
        ui.label(artifact_data.get("description", "")).classes("arc-body").style(
            "margin-bottom: 24px;"
        )

        divider()

        lore = artifact_data.get("lore", "")
        if lore:
            ui.label(lore).classes("arc-artifact-lore").style("margin: 16px 0 24px;")

        origin_char = artifact_data.get("origin_character", "")
        origin_session = artifact_data.get("origin_session", "")
        if origin_char or origin_session:
            ui.label(f"Acquired from {origin_char} during {origin_session}").classes(
                "arc-artifact-provenance"
            )


# ============================================================================
# READER'S DESK: FULL SCREEN BUILDER
# ============================================================================


def show_readers_desk(
    engine,
    output,
    get_stats_fn,
    make_choice_fn,
    show_save_fn,
    navigate_fn,
):
    """Build the complete Reader's Desk hub screen.

    This renders the tabbed workspace where the player manages their practice
    between sessions. It reads choices from the engine output to populate
    the client list, and reads engine state for notes and artifacts.

    Args:
        engine: The BardEngine instance
        output: The current PassageOutput (from a UI:DASHBOARD passage)
        get_stats_fn: Callable that returns stats dict
        make_choice_fn: Callable(int) to make a choice
        show_save_fn: Callable to show save dialog
        navigate_fn: Callable(str) to navigate to a screen
    """
    # ---- State: track active tab and selected artifact ----
    # Using a mutable dict so closures can update it
    desk_state = {"tab": "clients", "note_filter": "all", "artifact_idx": None}

    def switch_tab(tab):
        desk_state["tab"] = tab
        desk_state["artifact_idx"] = None
        rebuild_desk()

    def set_note_filter(f):
        desk_state["note_filter"] = f
        rebuild_desk()

    def select_artifact(idx):
        desk_state["artifact_idx"] = idx
        rebuild_desk()

    # ---- Extract data from engine ----
    stats = get_stats_fn()
    state = engine.state if engine else {}

    # Reader object
    reader = state.get("reader")

    # Notes — pull from engine state if available
    notes = []
    raw_notes = state.get("reader_notes", [])
    if hasattr(reader, "notes") and not raw_notes:
        raw_notes = getattr(reader, "notes", [])
    for n in raw_notes:
        if isinstance(n, dict):
            notes.append(n)
        elif isinstance(n, str):
            notes.append({"text": n, "source": "", "category": "observation"})

    # Artifacts — from reader.artifacts
    artifacts = []
    if reader and hasattr(reader, "artifacts"):
        try:
            # Import the game's artifact lookup
            from game_logic.artifacts import get_artifact

            for aid in reader.artifacts:
                art = get_artifact(aid)
                if art:
                    artifacts.append(
                        {
                            "name": getattr(art, "name", str(aid)),
                            "description": getattr(art, "description", ""),
                            "lore": getattr(art, "lore", ""),
                            "origin_character": getattr(art, "origin_character", ""),
                            "origin_session": getattr(art, "origin_session", ""),
                        }
                    )
        except (ImportError, Exception):
            pass

    # Categorize choices, then enrich client entries with flavor/trust data
    buckets = categorize_choices(output.choices if output else [])

    def _enrich(idx, choice):
        """Extract client metadata from engine state via var: tags."""
        tags = choice.get("tags", [])
        flavor, trust, session_text = "", 0, ""
        for tag in tags:
            if tag.startswith("var:"):
                var_name = tag.split(":", 1)[1]
                client_obj = state.get(var_name)
                if client_obj:
                    flavor = getattr(client_obj, "flavor_text", "")
                    trust = getattr(client_obj, "trust", 0)
                    completed = getattr(client_obj, "sessions_completed", 0)
                    total = getattr(client_obj, "total_sessions", 3)
                    session_text = f"Session {completed + 1} of {total}"
                break
        return {
            "index": idx,
            "name": choice["text"],
            "flavor": flavor,
            "trust": trust,
            "session_text": session_text,
        }

    client_choices = [_enrich(i, c) for i, c in buckets["client"]]
    special_choices = [_enrich(i, c) for i, c in buckets["special"]]
    regular_choices = [{"index": i, "name": c["text"]} for i, c in buckets["regular"]]

    # ---- Main container that gets rebuilt on tab switch ----
    desk_container = ui.column().classes("w-full min-h-screen m-0 p-0")

    def rebuild_desk():
        desk_container.clear()
        with desk_container:
            _build_desk_content()

    def _build_desk_content():
        tab = desk_state["tab"]

        with ui.element("div").style(
            "display: flex; width: 100%; min-height: 100vh; margin: 0; padding: 0;"
        ):
            # ===== SIDEBAR =====
            with ui.element("div").classes("arc-sidebar"):
                # Brand motif
                with ui.element("div").style("margin-bottom: 8px; opacity: 0.85;"):
                    motif(theme="default", size=56)

                ui.label("ARCANUM").classes("arc-sidebar-title")
                # ui.label("by katehlouie").classes("arc-sidebar-byline")

                divider(width="80%")

                # Sidebar nav mirrors tabs
                for item in [
                    {"label": "Clients", "tab": "clients"},
                    {"label": "Notes", "tab": "notes"},
                    {"label": "Artifacts", "tab": "artifacts"},
                ]:
                    cls = "arc-nav-btn active" if tab == item["tab"] else "arc-nav-btn"
                    with (
                        ui.element("button")
                        .classes(cls)
                        .on("click", lambda t=item["tab"]: switch_tab(t))
                    ):
                        ui.label(item["label"])

                divider(width="80%")

                # Stats
                with ui.element("div").style("width: 100%; padding: 0 8px;"):
                    stat_row("Level", str(stats.get("reader_level", "Novice")))
                    stat_row("Sessions", str(stats.get("sessions_completed", 0)))
                    stat_row("Savings", f"${stats.get('coins_earned', 0)}")

                # XP bar
                experience = stats.get("experience", 0)
                level_num = (experience // 100) + 1
                xp_needed = level_num * 100
                with ui.element("div").style("width: 100%; padding: 8px 8px 0;"):
                    xp_bar(experience % xp_needed, xp_needed)

                divider(width="80%")

                # Bottom actions
                ui.element("div").style("flex: 1;")
                with ui.row().classes("gap-4"):
                    ui.label("Save").style(
                        f"font-family: var(--heading-font); font-size: 11px; "
                        f"color: var(--text-muted); letter-spacing: 1px; "
                        "text-transform: uppercase; cursor: pointer;"
                    ).on("click", show_save_fn)
                    ui.label("Menu").style(
                        f"font-family: var(--heading-font); font-size: 11px; "
                        f"color: var(--text-muted); letter-spacing: 1px; "
                        "text-transform: uppercase; cursor: pointer;"
                    ).on("click", lambda: navigate_fn("landing"))

            # ===== CONTENT =====
            with ui.element("div").classes("arc-content"):
                with ui.element("div").classes("arc-content-inner"):
                    # Header
                    section_label("The Reading Table")
                    heading("Your Desk")

                    # Flavor text from passage
                    if output and output.content:
                        ui.label(output.content.strip().replace("*", "")).classes(
                            "arc-muted"
                        ).style("margin-bottom: 24px; font-size: 16px;")

                    # Stats row
                    with ui.row().style(
                        "gap: 1px; width: 100%; margin-bottom: 32px; align-items: stretch;"
                    ):
                        desk_stat_card(
                            "Sessions", str(stats.get("sessions_completed", 0))
                        )
                        desk_stat_card("Earnings", f"${stats.get('coins_earned', 0)}")
                        desk_stat_card(
                            "Level",
                            str(stats.get("reader_level", "Novice")),
                            sub=f"{experience % xp_needed}/{xp_needed} XP",
                        )

                    # Tab bar
                    with ui.element("div").classes("arc-tab-bar"):
                        avail_count = len(client_choices) + len(special_choices)
                        desk_tab(
                            "Clients",
                            tab == "clients",
                            lambda: switch_tab("clients"),
                            count=avail_count,
                        )
                        desk_tab(
                            "Notes",
                            tab == "notes",
                            lambda: switch_tab("notes"),
                            count=len(notes),
                        )
                        desk_tab(
                            "Artifacts",
                            tab == "artifacts",
                            lambda: switch_tab("artifacts"),
                            icon="✧",
                            count=len(artifacts),
                        )

                    # Tab content
                    with ui.element("div").classes("arc-fade-in"):
                        # ---- CLIENTS TAB ----
                        if tab == "clients":
                            # Available clients
                            if special_choices or client_choices:
                                ui.label("Available Appointments").classes(
                                    "arc-label"
                                ).style("margin-bottom: 8px;")

                            with ui.column().style(
                                "gap: 8px; width: 100%; align-items: stretch;"
                            ):
                                # Special (dream) clients first
                                for c in special_choices:
                                    desk_client_card(
                                        name=c["name"],
                                        flavor=c["flavor"],
                                        session_text=c["session_text"],
                                        trust=c["trust"],
                                        on_click=lambda idx=c["index"]: make_choice_fn(
                                            idx
                                        ),
                                        is_special=True,
                                        dream_tag="◆ Dream Client",
                                    )
                                # Regular clients
                                for c in client_choices:
                                    desk_client_card(
                                        name=c["name"],
                                        flavor=c["flavor"],
                                        session_text=c["session_text"],
                                        trust=c["trust"],
                                        on_click=lambda idx=c["index"]: make_choice_fn(
                                            idx
                                        ),
                                    )

                            # Non-client choices (e.g., "Wander over to your shelf")
                            if regular_choices:
                                divider()
                                with ui.column().style("gap: 6px; width: 100%;"):
                                    for c in regular_choices:
                                        with (
                                            ui.element("button")
                                            .classes("arc-choice")
                                            .on(
                                                "click",
                                                lambda idx=c["index"]: make_choice_fn(
                                                    idx
                                                ),
                                            )
                                        ):
                                            ui.html(
                                                f'<span class="arc-choice-prefix">›</span> {c["name"]}'
                                            )

                        # ---- NOTES TAB ----
                        elif tab == "notes":
                            nf = desk_state["note_filter"]

                            # Filter chips
                            with ui.row().style("gap: 8px; margin-bottom: 16px;"):
                                for cat in ["all", "observation", "insight", "anomaly"]:
                                    desk_filter_chip(
                                        cat, nf == cat, lambda c=cat: set_note_filter(c)
                                    )

                            # Note cards
                            filtered = [
                                n
                                for n in notes
                                if nf == "all" or n.get("category") == nf
                            ]
                            if filtered:
                                with ui.column().style("width: 100%;"):
                                    for n in filtered:
                                        desk_note_card(
                                            text=n.get("text", ""),
                                            source=n.get("source", ""),
                                            category=n.get("category", "observation"),
                                        )
                            else:
                                ui.label(
                                    "No notes yet. They'll appear as you conduct readings."
                                ).classes("arc-muted").style("font-size: 15px;")

                        # ---- ARTIFACTS TAB ----
                        elif tab == "artifacts":
                            artifact_idx = desk_state["artifact_idx"]

                            if artifact_idx is not None and artifact_idx < len(
                                artifacts
                            ):
                                # Detail view
                                desk_artifact_detail(
                                    artifacts[artifact_idx],
                                    on_back=lambda: select_artifact(None),
                                )
                            else:
                                # List view
                                if artifacts:
                                    ui.label(
                                        "Your collection gleams in the low light."
                                    ).classes("arc-muted").style(
                                        "font-size: 16px; margin-bottom: 16px;"
                                    )
                                    with ui.column().style("gap: 8px; width: 100%;"):
                                        for idx, art in enumerate(artifacts):
                                            desk_artifact_card(
                                                name=art["name"],
                                                description=art["description"],
                                                origin=f"From {art.get('origin_character', '?')} — {art.get('origin_session', '?')}",
                                                on_click=lambda i=idx: select_artifact(
                                                    i
                                                ),
                                            )
                                else:
                                    ui.label(
                                        "The shelf is empty. No artifacts yet."
                                    ).classes("arc-muted").style("font-size: 16px;")

    # Initial build
    rebuild_desk()
    return desk_container
