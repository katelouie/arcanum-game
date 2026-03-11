"""Debug mode for Arcanum — preview spreads, themes, and jump to game states."""

import json
import sys
import types
from pathlib import Path

from nicegui import ui

# Ensure game_logic is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from arcanum_theme import divider, get_theme, heading, inject_stagger_script, inject_theme, motif
from card_renderer import render_svg_card_html, has_svg_card
from game_logic.tarot import Deck, Spread

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STORY_ID = "arcanum"

ALL_THEMES = ["default", "cyberpunk", "gothic", "kind", "weird_west"]

# Key passages to jump to, grouped by category
JUMP_TARGETS = {
    "Hub": [
        ("Reader's Table", "ReaderTable"),
    ],
    "Chen": [
        ("Session 1", "Chen.Session1.Start"),
        ("Session 2", "Chen.Session2.Start"),
    ],
    "Nyx": [
        ("Session 1", "Nyx.Session1.Start"),
        ("Session 2", "Nyx.Session2.Start"),
    ],
    "Blackthorn": [
        ("Session 1", "Blackthorn.Session1.Start"),
    ],
    "The Kind": [
        ("Session 1", "TheKind.Session1.Start"),
    ],
}


def _apply_theme(theme_name: str):
    """Apply a CSS theme via JS."""
    if theme_name == "default":
        js = "document.documentElement.removeAttribute('data-theme');"
    else:
        js = f"document.documentElement.setAttribute('data-theme', '{theme_name}');"
    ui.run_javascript(js)


def _load_all_spreads() -> list[dict]:
    """Load spread IDs and metadata from spreads-config.json."""
    with open(PROJECT_ROOT / "game_logic" / "spreads-config.json") as f:
        data = json.load(f)
    return data["spreads"]


def _render_spread_preview(spread_id: str, card_size_override: str | None = None):
    """Render a single spread with sample cards for preview."""
    try:
        spread = Spread(spread_id)
    except Exception as e:
        ui.label(f"Error loading {spread_id}: {e}").style("color: red;")
        return

    deck = Deck()
    cards = deck.draw_cards(len(spread.positions))
    # Reverse a couple for visual variety
    if len(cards) > 1:
        cards[1].set_reversed(True)
    if len(cards) > 3:
        cards[3].set_reversed(True)

    positioned = spread.get_positioned_cards(cards)

    card_widths = {"large": 160, "medium": 120, "small": 90}
    card_size = card_size_override or spread.card_size
    card_width = card_widths.get(card_size, 120)

    base_height = 850
    if spread.aspect_ratio:
        container_height = max(400, int(base_height / spread.aspect_ratio))
    else:
        container_height = base_height

    # Scale down for the gallery view
    container_height = min(container_height, 700)

    with ui.element("div").classes("relative w-full").style(
        f"height: {container_height}px; max-width: 750px; margin: 0 auto;"
    ):
        for card_data in positioned:
            x = card_data["x"]
            y = card_data["y"]
            rotation = card_data.get("rotation", 0)
            z_index = card_data.get("zIndex", 1)
            card = card_data["card"]
            position_name = card_data.get("name", "")

            transform = f"translate(-50%, -50%) rotate({rotation}deg)"

            with ui.element("div").style(
                f"position: absolute; left: {x}%; top: {y}%; "
                f"transform: {transform}; z-index: {z_index};"
            ):
                with ui.column().classes("items-center").style(
                    f"width: {card_width}px; gap: 4px;"
                ):
                    with ui.element("div").classes("arc-card").style(
                        "padding: 6px; width: 100%;"
                    ):
                        image_path = card.get_image_filename()
                        abs_path = PROJECT_ROOT / image_path
                        if abs_path.exists():
                            rot_style = (
                                "transform: rotate(180deg);" if card.reversed else ""
                            )
                            ui.image(str(abs_path)).style(
                                f"width: 100%; height: auto; object-fit: contain; {rot_style}"
                            )
                        else:
                            ui.html(
                                '<span style="font-size: 2em; color: var(--gold-dim);">&#10023;</span>'
                            ).style(
                                "width: 100%; height: 80px; display: flex; "
                                "align-items: center; justify-content: center;"
                            )

                    if position_name:
                        ui.label(position_name).style(
                            "font-family: var(--heading-font); font-size: 10px; "
                            "letter-spacing: 1.5px; color: var(--gold-dim); "
                            "text-transform: uppercase; text-align: center; "
                            "white-space: nowrap;"
                        )


def _build_spread_gallery():
    """Render a gallery of all spreads."""
    spreads_meta = _load_all_spreads()

    # Deduplicate by layout (show one spread per unique layout)
    seen_layouts = set()
    unique_spreads = []
    for s in spreads_meta:
        if s["layout"] not in seen_layouts:
            seen_layouts.add(s["layout"])
            unique_spreads.append(s)

    for spread_data in unique_spreads:
        sid = spread_data["id"]
        name = spread_data["name"]
        layout = spread_data["layout"]
        n_positions = len(spread_data["positions"])
        card_size = spread_data["cardSize"]

        with ui.card().style(
            "background: var(--bg); border: 1px solid var(--gold-dim); "
            "padding: 24px; margin-bottom: 24px; width: 100%;"
        ):
            with ui.row().classes("items-center gap-4"):
                ui.label(name).style(
                    "font-family: var(--heading-font); font-size: 18px; "
                    "color: var(--gold); letter-spacing: 1px;"
                )
                ui.label(
                    f"layout: {layout} | {n_positions} cards | size: {card_size}"
                ).style("font-size: 12px; color: var(--gold-dim); opacity: 0.7;")

            _render_spread_preview(sid)


def _build_theme_gallery():
    """Show a sample card + text in each theme."""
    deck = Deck()

    for theme_name in ALL_THEMES:
        t = get_theme(theme_name)
        display_name = t.get("dream_badge", theme_name.replace("_", " ").title())

        with ui.card().style(
            "padding: 24px; margin-bottom: 16px; width: 100%; "
            "border: 1px solid var(--gold-dim);"
        ):
            with ui.row().classes("items-center gap-4"):
                ui.button(
                    f"Apply: {display_name or theme_name}",
                    on_click=lambda tn=theme_name: _apply_theme(tn),
                ).props("flat").style(
                    "color: var(--gold); font-family: var(--heading-font); "
                    "letter-spacing: 1px; text-transform: uppercase;"
                )

            ui.label(
                f"Fonts: {t.get('heading_font', '?')} / {t.get('body_font', '?')}"
            ).style("font-size: 12px; color: var(--gold-dim); opacity: 0.7;")

            # Sample text
            ui.html(
                f'<p style="font-family: var(--body-font); color: var(--fg); '
                f'line-height: 1.8; margin-top: 8px;">'
                f"The cards spread before you, each one a whispered secret. "
                f"<em>She watches you from behind the candle's glow.</em> "
                f'"Trust is not given," she says. "It is built, card by card."</p>'
            )


def _build_quick_jump():
    """Quick-jump buttons that open the game at specific passages."""
    ui.label(
        "Each button opens the game in a new tab, pre-loaded to that passage."
    ).style("font-size: 13px; color: var(--gold-dim); margin-bottom: 16px;")

    for category, targets in JUMP_TARGETS.items():
        ui.label(category).style(
            "font-family: var(--heading-font); font-size: 16px; "
            "color: var(--gold); letter-spacing: 1px; margin-top: 12px;"
        )
        with ui.row().classes("gap-2 flex-wrap"):
            for label, passage_id in targets:
                ui.button(
                    label,
                    on_click=lambda pid=passage_id: ui.navigate.to(
                        f"/debug/play?goto={pid}", new_tab=True
                    ),
                ).props("flat outline").style(
                    "color: var(--gold-dim); border-color: var(--gold-dim); "
                    "font-size: 12px; text-transform: none;"
                )


def _build_deck_gallery():
    """Render the full 78-card deck with a toggle between Arcanum SVG and Classic."""
    deck = Deck()

    # Group by suit
    groups = [
        ("Major Arcana", [c for c in deck.cards if c.suit == "major"]),
        ("Cups", [c for c in deck.cards if c.suit == "cups"]),
        ("Swords", [c for c in deck.cards if c.suit == "swords"]),
        ("Wands", [c for c in deck.cards if c.suit == "wands"]),
        ("Pentacles", [c for c in deck.cards if c.suit == "pentacles"]),
    ]

    # Style toggle — reactive
    style_state = {"current": "arcanum"}
    grid_container = None

    def render_grid():
        """Render the card grid based on current style."""
        grid_container.clear()
        with grid_container:
            for group_name, cards in groups:
                ui.label(group_name).style(
                    "font-family: var(--heading-font); font-size: 18px; "
                    "color: var(--gold); letter-spacing: 1px; margin-top: 16px; "
                    "margin-bottom: 8px; width: 100%;"
                )
                with ui.element("div").style(
                    "display: flex; flex-wrap: wrap; gap: 12px; width: 100%; "
                    "margin-bottom: 24px;"
                ):
                    for card in cards:
                        card_code = card._get_code()
                        has_svg = has_svg_card(card_code)
                        use_svg = style_state["current"] == "arcanum" and has_svg

                        with ui.element("div").style("width: 120px;"):
                            with ui.element("div").style(
                                "width: 120px; height: 207px; "
                                "border: 1px solid var(--gold-dim); border-radius: 4px; "
                                "overflow: hidden; position: relative;"
                            ):
                                if use_svg:
                                    svg_html = render_svg_card_html(card, card_code)
                                    if svg_html:
                                        ui.html(svg_html).style(
                                            "width: 100%; height: 100%;"
                                        )
                                    else:
                                        _render_fallback_image(card)
                                else:
                                    _render_fallback_image(card)

                                # SVG badge
                                if has_svg:
                                    ui.element("div").style(
                                        "position: absolute; top: 4px; right: 4px; "
                                        "width: 8px; height: 8px; border-radius: 50%; "
                                        "background: var(--gold); opacity: 0.7;"
                                    )

                            # Card name
                            ui.label(card.name).style(
                                "font-size: 9px; color: var(--gold-dim); "
                                "text-align: center; margin-top: 4px; width: 100%; "
                                "white-space: nowrap; overflow: hidden; text-overflow: ellipsis;"
                            )

    def _render_fallback_image(card):
        """Render the Rider-Waite image for a card."""
        image_path = card.get_image_filename()
        abs_path = PROJECT_ROOT / image_path
        if abs_path.exists():
            ui.image(str(abs_path)).style(
                "width: 100%; height: 100%; object-fit: cover;"
            )
        else:
            ui.html(
                '<span style="font-size: 2em; color: var(--gold-dim); '
                'display: flex; align-items: center; justify-content: center; '
                'width: 100%; height: 100%;">&#10023;</span>'
            )

    def switch_style(style):
        style_state["current"] = style
        render_grid()

    # Toggle buttons
    with ui.row().classes("items-center gap-4 mb-4"):
        ui.button(
            "Arcanum",
            on_click=lambda: switch_style("arcanum"),
        ).props("flat").style(
            "color: var(--gold); font-family: var(--heading-font); "
            "letter-spacing: 1px; text-transform: uppercase; font-size: 12px;"
        )
        ui.button(
            "Classic (Rider-Waite)",
            on_click=lambda: switch_style("classic"),
        ).props("flat").style(
            "color: var(--gold-dim); font-family: var(--heading-font); "
            "letter-spacing: 1px; text-transform: uppercase; font-size: 12px;"
        )
        ui.label(
            "Gold dot = SVG available"
        ).style("font-size: 11px; color: var(--gold-dim); opacity: 0.5;")

    # Card grid container (cleared and rebuilt on toggle)
    grid_container = ui.column().classes("w-full")
    render_grid()


def register_debug_routes():
    """Register the /debug page and /debug/play route. Call from main module."""
    from bardic.runtime.engine import BardEngine

    @ui.page("/debug")
    def debug_page():
        # Apply default theme
        _apply_theme("default")

        with ui.element("div").style(
            "max-width: 1000px; margin: 0 auto; padding: 32px;"
        ):
            # Header
            ui.label("ARCANUM DEBUG MODE").style(
                "font-family: var(--heading-font); font-size: 28px; "
                "color: var(--gold); letter-spacing: 3px; margin-bottom: 4px;"
            )
            ui.label("Preview spreads, themes, and jump to game states.").style(
                "font-size: 13px; color: var(--gold-dim); margin-bottom: 24px;"
            )

            # Theme selector in header
            with ui.row().classes("items-center gap-2 mb-4"):
                ui.label("Theme:").style(
                    "font-size: 12px; color: var(--gold-dim); text-transform: uppercase; "
                    "letter-spacing: 1px;"
                )
                for tn in ALL_THEMES:
                    ui.button(
                        tn.replace("_", " "),
                        on_click=lambda t=tn: _apply_theme(t),
                    ).props("flat dense").style(
                        "color: var(--gold-dim); font-size: 11px; text-transform: uppercase; "
                        "letter-spacing: 1px; min-height: 28px; padding: 2px 10px;"
                    )

            divider()

            # Tabs
            with ui.tabs().style(
                "color: var(--gold-dim);"
            ).classes("w-full") as tabs:
                spreads_tab = ui.tab("Spreads")
                deck_tab = ui.tab("Deck")
                themes_tab = ui.tab("Themes")
                jump_tab = ui.tab("Quick Play")

            with ui.tab_panels(tabs, value=spreads_tab).classes("w-full").style(
                "background: transparent;"
            ):
                with ui.tab_panel(spreads_tab):
                    _build_spread_gallery()

                with ui.tab_panel(deck_tab):
                    _build_deck_gallery()

                with ui.tab_panel(themes_tab):
                    _build_theme_gallery()

                with ui.tab_panel(jump_tab):
                    _build_quick_jump()

    @ui.page("/debug/play")
    def debug_play(goto: str = "ReaderTable"):
        """Start a game session pre-jumped to a specific passage."""
        # Reuse GameSession but jump to the target passage after init
        from nicegui_player import GameSession

        session = GameSession()
        session.build()

        # Load story and run init
        session.load_story()

        # Run until InitVars completes (it jumps to Start)
        # Then goto the requested passage
        try:
            session.engine.goto(goto)
        except Exception as e:
            ui.notify(f"Failed to jump to '{goto}': {e}", type="negative")
            return

        session.current_screen = "player"
        session.update_ui()
