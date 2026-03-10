import json
import sys
import uuid
from pathlib import Path

import markdown
from arcanum_theme import (
    # Choice categorization (shared utility)
    categorize_choices,
    choice_prompt,
    # Layout components
    divider,
    get_theme,
    heading,
    inject_stagger_script,
    # Setup
    inject_theme,
    # Motifs
    motif,
    section_label,
    # Reader's Desk
    show_readers_desk,
    stat_row,
)

# Import from installed bardic package
from bardic.runtime.engine import BardEngine
from nicegui import app, ui

# Import local save manager (from same directory)
sys.path.insert(0, str(Path(__file__).parent))
from save_manager import BrowserSaveManager

# Make sure to include game_logic directory
sys.path.insert(0, str(Path(__file__).parent.parent))

# ============================================================================
# MODULE-LEVEL SETUP (runs once at import, shared across all clients)
# ============================================================================

STORY_ID = "arcanum"
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Static files: accessible via URLs for all clients
app.add_static_files("/assets", str(PROJECT_ROOT / "assets"))

# Theme CSS and stagger JS: injected into <head> for all pages
inject_theme()
inject_stagger_script()


# ============================================================================
# PER-CLIENT GAME SESSION
# ============================================================================


class GameSession:
    """Holds all state for a single browser client's game session.

    Each client that connects gets their own GameSession instance,
    so multiple players can play simultaneously without interference.
    """

    def __init__(self):
        self.engine: BardEngine | None = None
        self.current_screen: str = "landing"
        self.active_theme: str = "default"  # sticky — persists until a tag overrides it
        self.main_container = None
        self.card_drawer = None
        self.card_drawer_content = None
        self.save_manager = BrowserSaveManager()

    # ================================================================
    # PAGE SETUP
    # ================================================================

    def build(self):
        """Create the root UI elements and render the initial screen."""
        self.card_drawer, self.card_drawer_content = self._create_card_drawer()
        self.main_container = ui.column().classes(
            "w-full min-h-screen m-0 p-0 items-stretch"
        )
        self.update_ui()

    def _create_card_drawer(self):
        """Create the card detail drawer (hidden by default)."""
        with (
            ui.right_drawer()
            .props("width=420 overlay elevated")
            .style(
                "background: var(--sidebar-bg) !important; "
                "border-left: 1px solid color-mix(in srgb, var(--gold-dim) 25%, transparent);"
            ) as drawer
        ):
            content = ui.column().classes("w-full h-full")

        drawer.hide()
        return drawer, content

    # ================================================================
    # STORY LOADING
    # ================================================================

    def load_story(self, story_path: str | Path | None = None):
        """Load a compiled story JSON and create BardEngine instance."""
        import types

        if story_path is None:
            story_path = PROJECT_ROOT / "compiled_stories" / f"{STORY_ID}.json"

        with open(story_path) as f:
            story_data = json.load(f)

        self.engine = BardEngine(story_data, context={})

        # The engine's _execute_imports puts everything into state, including
        # modules (e.g. `import random`) and functions (e.g. `get_artifact`).
        # These can't be deepcopied, which breaks engine.snapshot().
        # Move them to context (available in eval but not snapshotted).
        for key in list(self.engine.state):
            val = self.engine.state[key]
            if isinstance(val, (types.ModuleType, types.FunctionType)):
                self.engine.context[key] = self.engine.state.pop(key)

    # ================================================================
    # NAVIGATION
    # ================================================================

    def navigate_to(self, screen: str):
        """Switch to a different screen."""
        self.current_screen = screen
        self.update_ui()

    def update_ui(self):
        """Rebuild the UI based on current screen."""
        self.main_container.clear()

        with self.main_container:
            if self.current_screen == "landing":
                self.show_landing()
            elif self.current_screen == "player":
                self.show_player()

    # ================================================================
    # LANDING PAGE
    # ================================================================

    def show_landing(self):
        """Landing page — clean typography, begin/continue buttons."""
        with ui.element("div").classes("arc-landing"):
            divider(width="200px")

            ui.label("ARCANUM").classes("arc-landing-title")
            ui.label("A Digital Cartomancer's Tale").classes("arc-landing-subtitle")

            divider(width="200px")

            with ui.column().classes("gap-3 items-center").style("margin-top: 24px;"):
                with (
                    ui.element("button")
                    .classes("arc-btn-primary")
                    .on("click", lambda: self.start_new_game())
                ):
                    ui.label("Begin Reading")

                with (
                    ui.element("button")
                    .classes("arc-btn-secondary")
                    .on("click", lambda: self.show_load_dialog())
                ):
                    ui.label("Continue Journey")

    # ================================================================
    # SAVE / LOAD
    # ================================================================

    def show_save_dialog(self):
        """Save dialog with theme styling."""
        with (
            ui.dialog() as dialog,
            ui.card().style(
                "background: var(--sidebar-bg) !important; "
                "border: 1px solid color-mix(in srgb, var(--gold-dim) 25%, transparent); "
                "padding: 24px;"
            ),
        ):
            ui.label("Save Your Reading").classes("arc-subheading").style(
                "font-size: 24px; margin-bottom: 16px;"
            )

            save_name_input = (
                ui.input(
                    label="Save Name", placeholder="e.g., Before meeting the hermit"
                )
                .classes("w-full mb-4")
                .props("dark")
            )

            with ui.row().classes("gap-2 w-full justify-end"):
                with (
                    ui.element("button")
                    .classes("arc-btn-secondary")
                    .style("padding: 8px 20px;")
                    .on("click", dialog.close)
                ):
                    ui.label("Cancel")

                with (
                    ui.element("button")
                    .classes("arc-btn-primary")
                    .style("padding: 8px 20px;")
                    .on(
                        "click",
                        lambda: self._save_game_action(save_name_input.value, dialog),
                    )
                ):
                    ui.label("Save")

        dialog.open()

    async def _save_game_action(self, save_name: str, dialog):
        """Perform the save."""
        if not save_name:
            ui.notify("Please enter a save name", type="warning")
            return

        try:
            engine_state = self.engine.save_state()
            await self.save_manager.save_game(save_name, engine_state)
            ui.notify(f"Saved: {save_name}", type="positive")
            dialog.close()
        except Exception as e:
            ui.notify(f"Save failed: {e}", type="negative")

    async def show_load_dialog(self):
        """Show dialog to load a saved game."""
        saves = await self.save_manager.list_saves()

        with (
            ui.dialog() as dialog,
            ui.card().style(
                "background: var(--sidebar-bg) !important; "
                "border: 1px solid color-mix(in srgb, var(--gold-dim) 25%, transparent); "
                "padding: 24px; min-width: 400px;"
            ),
        ):
            ui.label("Load a Reading").classes("arc-subheading").style(
                "font-size: 24px; margin-bottom: 16px;"
            )

            if not saves:
                ui.label("No saved games found").classes("arc-muted").style(
                    "margin-bottom: 16px;"
                )
            else:
                with ui.column().style(
                    "gap: 8px; width: 100%; max-height: 384px; overflow-y: auto;"
                ):
                    for save in saves:
                        with (
                            ui.element("div")
                            .classes("arc-client-card")
                            .on(
                                "click",
                                lambda s=save: self._load_game_action(
                                    s["save_id"], dialog
                                ),
                            )
                        ):
                            ui.label(save["save_name"]).classes("arc-subheading").style(
                                "font-size: 18px;"
                            )
                            ui.label(f"Passage: {save['passage']}").classes(
                                "arc-body"
                            ).style("font-size: 14px;")
                            ui.label(save["date_display"]).classes("arc-muted").style(
                                "font-size: 12px;"
                            )

            with (
                ui.row().classes("gap-2 w-full justify-end").style("margin-top: 16px;")
            ):
                with (
                    ui.element("button")
                    .classes("arc-btn-secondary")
                    .style("padding: 8px 20px;")
                    .on("click", dialog.close)
                ):
                    ui.label("Cancel")

        dialog.open()

    async def _load_game_action(self, save_id: str, dialog):
        """Perform the load."""
        try:
            save_data = await self.save_manager.load_game(save_id)

            story_id = save_data.get("story_id", STORY_ID)
            story_path = PROJECT_ROOT / "compiled_stories" / f"{story_id}.json"

            if not story_path.exists():
                ui.notify(f"Story file not found: {story_id}", type="negative")
                return

            self.load_story(story_path)
            self.engine.load_state(save_data)

            ui.notify(f"Loaded: {save_data['save_name']}", type="positive")
            dialog.close()

            self.navigate_to("player")
        except Exception as e:
            ui.notify(f"Load failed: {e}", type="negative")

    # ================================================================
    # PLAYER MODE
    # ================================================================

    def start_new_game(self):
        """Start a new game — load story and navigate to player."""
        story_path = PROJECT_ROOT / "compiled_stories" / f"{STORY_ID}.json"
        self.load_story(story_path)
        self.navigate_to("player")

    def show_player(self):
        """Player screen with sidebar layout."""
        output = self.engine.current()

        passage = self.engine.passages.get(output.passage_id, {})
        passage_tags = passage.get("tags", [])

        # Update sticky theme from passage tags (only if a tag is present)
        if "DREAM:CYBERPUNK" in passage_tags or "DREAM:NYX" in passage_tags:
            self.active_theme = "cyberpunk"
        elif "DREAM:GOTHIC" in passage_tags or "DREAM:MANOR" in passage_tags:
            self.active_theme = "gothic"
        elif "DREAM:KIND" in passage_tags or "DREAM:BOOKSHOP" in passage_tags:
            self.active_theme = "kind"
        elif "DREAM:WEIRDWEST" in passage_tags:
            self.active_theme = "weird_west"
        elif "THEME:DEFAULT" in passage_tags or "UI:DASHBOARD" in passage_tags:
            self.active_theme = "default"
        # Otherwise: keep self.active_theme as-is (sticky)

        if "UI:DASHBOARD" in passage_tags:
            # Apply default theme for dashboard
            js = "document.documentElement.removeAttribute('data-theme');"
            ui.timer(0.01, lambda: ui.run_javascript(js), once=True)
            show_readers_desk(
                self.engine,
                output,
                self.get_reader_stats,
                self.make_choice,
                self.show_save_dialog,
                self.navigate_to,
            )
            return

        theme = self.active_theme
        t = get_theme(theme)
        is_dream = theme != "default"

        # Apply CSS theme to the DOM (switches CSS variables)
        if theme == "default":
            js = "document.documentElement.removeAttribute('data-theme');"
        else:
            js = f"document.documentElement.setAttribute('data-theme', '{theme}');"
        ui.timer(0.01, lambda: ui.run_javascript(js), once=True)

        # --- Sidebar + Content Layout ---
        with ui.element("div").style(
            "display: flex; width: 100%; min-height: 100vh; margin: 0; padding: 0;"
        ):
            # === SIDEBAR ===
            with ui.element("div").classes("arc-sidebar"):
                with ui.element("div").style("margin-bottom: 8px; opacity: 0.85;"):
                    motif(theme=theme, size=56)

                ui.label("ARCANUM").classes("arc-sidebar-title")

                dream_badge = t.get("dream_badge", "")
                if dream_badge:
                    ui.label(dream_badge).classes("arc-dream-badge")
                # ui.label("by katehlouie").classes("arc-sidebar-byline")

                divider(width="80%")

                # Navigation
                for item in [
                    {"label": "Story", "active": True},
                    {"label": "Reading", "active": False},
                ]:
                    cls = "arc-nav-btn active" if item["active"] else "arc-nav-btn"
                    with ui.element("button").classes(cls):
                        ui.label(item["label"])

                # # DEBUG: quick-nav links (remove before shipping)
                # divider(width="80%")
                # section_label("⚙ Debug Nav")
                # with ui.element("button").classes("arc-nav-btn").on(
                #     "click", lambda: self._debug_goto("ReaderTable")
                # ):
                #     ui.label("→ Reader's Table")
                # with ui.element("button").classes("arc-nav-btn").on(
                #     "click", lambda: self._debug_goto("Chen.Session1.LayoutCards")
                # ):
                #     ui.label("→ Card Reading")

                divider(width="80%")

                # Stats from engine
                stats = self.get_reader_stats()
                with ui.element("div").style("width: 100%; padding: 0 8px;"):
                    stat_row("Reputation", str(stats.get("reader_level", "Newcomer")))
                    stat_row("Clients", str(stats.get("sessions_completed", 0)))
                    stat_row("Savings", f"${stats.get('coins_earned', 0)}")

                divider(width="80%")

                # Bottom actions
                ui.element("div").style("flex: 1;")  # spacer

                with ui.row().classes("gap-4"):
                    ui.label("Save").classes("arc-sidebar-byline").style(
                        "cursor: pointer; font-style: normal; "
                        "text-transform: uppercase; letter-spacing: 2px;"
                    ).on("click", lambda: self.show_save_dialog())

                    ui.label("Menu").classes("arc-sidebar-byline").style(
                        "cursor: pointer; font-style: normal; "
                        "text-transform: uppercase; letter-spacing: 2px;"
                    ).on("click", lambda: self.navigate_to("landing"))

            # === CONTENT AREA ===
            with ui.element("div").classes("arc-content"):
                with ui.element("div").classes("arc-content-inner arc-fade-in"):
                    if is_dream:
                        section_label("◆ Dream Session", dream=True)
                    else:
                        section_label("Story")

                    passage_title = passage.get("title", "")
                    if passage_title:
                        heading(passage_title)

                    # Staggered paragraph reveal
                    container_id = f"passage-{uuid.uuid4().hex[:8]}"
                    paragraphs = [
                        p.strip() for p in output.content.split("\n\n") if p.strip()
                    ]

                    with ui.element("div").props(f'id="{container_id}"'):
                        for para in paragraphs:
                            para_html = markdown.markdown(para, extensions=["nl2br"])
                            ui.html(para_html, sanitize=False).classes(
                                "arc-body arc-stagger-p"
                            ).style("margin-bottom: 18px;")

                    # Render directives (card spreads, etc.)
                    if (
                        hasattr(output, "render_directives")
                        and output.render_directives
                    ):
                        with ui.column().classes("w-full my-8"):
                            for directive in output.render_directives:
                                self.render_directive(directive)

                    # Input directives
                    if hasattr(output, "input_directives") and output.input_directives:
                        self.render_input_form(output.input_directives)

                    # Choices
                    if output.choices:
                        divider()
                        self.render_choices(output.choices)
                    else:
                        ui.label("✧ THE END ✧").classes("arc-heading").style(
                            "font-size: 28px; margin-top: 32px; text-align: center;"
                        )

                    # Trigger staggered reveal after DOM renders
                    ui.timer(
                        0.05,
                        lambda cid=container_id: ui.run_javascript(
                            f"revealStaggered('{cid}', 180);"
                        ),
                        once=True,
                    )

    # ================================================================
    # DEBUG HELPERS (remove before shipping)
    # ================================================================

    def _debug_goto(self, passage_id: str):
        """Jump directly to a passage by ID. For debugging only."""
        if self.engine is None:
            self.load_story()
        self.engine.goto(passage_id)
        self.current_screen = "player"
        self.update_ui()

    # ================================================================
    # CHOICES
    # ================================================================

    def make_choice(self, choice_index: int):
        """Handle player choice and update the story."""
        self.engine.choose(choice_index)
        self.update_ui()

    def render_choices(self, choices: list):
        """Render all choices with theme styling, categorized by tags."""
        buckets = categorize_choices(choices)
        client_choices = buckets["client"]
        special_choices = buckets["special"]
        meta_choices = buckets["meta"]
        regular_choices = buckets["regular"]

        if regular_choices:
            choice_prompt("What do you do?")
            with ui.column().classes("gap-2 w-full"):
                for idx, choice in regular_choices:
                    with (
                        ui.element("button")
                        .classes("arc-choice")
                        .on("click", lambda i=idx: self.make_choice(i))
                    ):
                        ui.html(
                            f'<span class="arc-choice-prefix">›</span> {choice["text"]}'
                        )

        if client_choices:
            heading("Available Clients", size="22px")
            with ui.grid(columns=3).classes("gap-4 w-full mb-6"):
                for idx, choice in client_choices:
                    self.render_client_card(choice, idx, is_special=False)

        if special_choices:
            heading("Special Consultations", size="22px")
            with ui.grid(columns=3).classes("gap-4 w-full mb-6"):
                for idx, choice in special_choices:
                    self.render_client_card(choice, idx, is_special=True)

        if meta_choices:
            with ui.column().classes("gap-2 w-full mt-4"):
                for idx, choice in meta_choices:
                    with (
                        ui.element("button")
                        .classes("arc-meta-choice")
                        .on("click", lambda i=idx: self.make_choice(i))
                    ):
                        ui.label(choice["text"])

    def render_client_card(self, choice, choice_index, is_special=False):
        """Client card with theme styling."""
        client_name = choice["text"]

        flavor_text = ""
        tags = choice.get("tags", [])
        for tag in tags:
            if tag.startswith("var:"):
                var_name = tag.split(":", 1)[1]
                client_obj = self.engine.state.get(var_name)
                if client_obj and hasattr(client_obj, "flavor_text"):
                    flavor_text = client_obj.flavor_text
                break

        border_style = (
            f"border: 1px solid {'#0088a0' if is_special else '#8a7235'}40;"
            f"border-left: 3px solid {'#0088a0' if is_special else '#8a7235'}60;"
        )

        with (
            ui.element("div")
            .classes("arc-fade-in")
            .style(
                f"background: {'#6b3fa0' if not is_special else '#0088a0'}08; "
                f"{border_style} "
                "padding: 20px; cursor: pointer; transition: all 0.3s ease; "
                "min-width: 280px;"
            )
            .on("click", lambda: self.make_choice(choice_index))
        ):
            ui.label(client_name).classes("arc-subheading").style("font-size: 20px;")
            if flavor_text:
                ui.label(flavor_text).classes("arc-muted").style(
                    "font-size: 14px; margin-top: 4px;"
                )

    # ================================================================
    # INPUT FORMS
    # ================================================================

    def render_input_form(self, input_directives: list[dict]):
        """Render text input form from input directives."""
        input_widgets = {}

        with (
            ui.element("div")
            .classes("arc-card-detail")
            .style("width: 100%; margin: 24px 0; padding: 24px;")
        ):
            with ui.column().style("gap: 16px; width: 100%;"):
                for spec in input_directives:
                    name = spec.get("name", "")
                    label = spec.get("label", name.replace("_", " ").title())
                    placeholder = spec.get("placeholder", "")

                    input_widgets[name] = (
                        ui.input(label=label, placeholder=placeholder)
                        .classes("w-full")
                        .props("dark outlined")
                    )

                with (
                    ui.element("button")
                    .classes("arc-btn-primary")
                    .style("margin-top: 16px; padding: 10px 32px;")
                    .on("click", lambda: self._submit_inputs(input_widgets))
                ):
                    ui.label("Submit")

    def _submit_inputs(self, input_widgets: dict):
        """Collect input data and submit to engine."""
        input_data = {
            name: widget.value or "" for name, widget in input_widgets.items()
        }

        self.engine.submit_inputs(input_data)

        current_passage_id = self.engine.current_passage_id
        self.engine.goto(current_passage_id)
        self.update_ui()

    # ================================================================
    # RENDER DIRECTIVES (card spreads, readings)
    # ================================================================

    def render_directive(self, directive: dict):
        """Route a render directive to the appropriate rendering function."""
        directive_name = directive.get("name", "")
        directive_data = directive.get("data", {})

        if directive_name == "render_spread":
            self._render_card_spread(directive_data)
        elif directive_name == "render_reading":
            self._render_reading(directive_data)
        else:
            ui.label(f"Unknown directive: {directive_name}").style(
                "color: var(--accent); font-size: 14px;"
            )

    def _render_card_spread(self, args: dict):
        """Render a tarot card spread with actual card images."""
        cards = args.get("cards", [])
        spread_name = args.get("spread", "Card Spread")

        heading(spread_name.replace("-", " ").replace("_", " ").title(), size="24px")

        with ui.row().classes("gap-6 w-full justify-center"):
            for card in cards:
                abs_image_path = None
                if isinstance(card, dict):
                    card_name = card.get("name", "Unknown Card")
                    is_reversed = card.get("reversed", False)
                    image_path = None
                else:
                    card_name = getattr(card, "name", "Unknown Card")
                    is_reversed = getattr(card, "reversed", False)
                    try:
                        image_path = card.get_image_filename()
                        abs_image_path = PROJECT_ROOT / image_path
                        if not abs_image_path.exists():
                            image_path = None
                            abs_image_path = None
                    except AttributeError:
                        image_path = None

                with (
                    ui.element("div")
                    .classes("arc-card")
                    .style("width: 160px; padding: 8px;")
                ):
                    with ui.column().classes("items-center justify-center gap-2"):
                        if image_path and abs_image_path and abs_image_path.exists():
                            rotation_style = (
                                "transform: rotate(180deg);" if is_reversed else ""
                            )
                            ui.image(str(abs_image_path)).style(
                                f"width: 144px; height: auto; object-fit: contain; {rotation_style}"
                            )
                        else:
                            with ui.element("div").style(
                                "width: 100%; height: 128px; display: flex; "
                                "align-items: center; justify-content: center;"
                            ):
                                ui.html(
                                    '<span style="font-size: 3em; color: var(--gold-dim);">✧</span>'
                                )

                        display_name = f"↓ {card_name}" if is_reversed else card_name
                        ui.label(display_name).classes("arc-label").style(
                            "text-align: center; font-size: 11px;"
                        )

    def _render_reading(self, args: dict):
        """Render a full Reading object with spread layout."""
        reading = args.get("reading")
        if not reading:
            ui.label("Error: No reading provided").style(
                "color: var(--accent); font-size: 14px;"
            )
            return

        positioned_cards = reading.get_positioned_cards()
        spread = reading.spread

        heading(spread.name, size="24px")

        card_widths = {"large": 180, "medium": 140, "small": 100}
        card_width = card_widths.get(spread.card_size, 140)

        base_height = 850
        if spread.aspect_ratio:
            container_height = max(500, int(base_height / spread.aspect_ratio))
        else:
            container_height = base_height

        with (
            ui.element("div")
            .classes("relative w-full mx-auto")
            .style(f"height: {container_height}px; max-width: 900px; margin-top: 16px; overflow: hidden;")
        ):
            for card_data in positioned_cards:
                x = card_data["x"]
                y = card_data["y"]
                rotation = card_data.get("rotation", 0)
                z_index = card_data.get("zIndex", 1)

                transform = f"translate(-50%, -50%) rotate({rotation}deg)"

                with ui.element("div").style(
                    f"position: absolute; "
                    f"left: {x}%; "
                    f"top: {y}%; "
                    f"transform: {transform}; "
                    f"z-index: {z_index};"
                ):
                    self._render_single_card(card_data, card_width)

    def _render_single_card(self, card_data: dict, width: int):
        """Render a single card with image, position label, and click handler."""
        card = card_data["card"]
        position_name = card_data["name"]
        rotation = card_data.get("rotation", 0)

        abs_image_path = None
        try:
            image_path = card.get_image_filename()
            abs_image_path = PROJECT_ROOT / image_path
            has_image = abs_image_path.exists()
        except AttributeError:
            has_image = False

        with ui.column().classes("items-center").style(f"width: {width}px; gap: 8px;"):
            with (
                ui.element("div")
                .classes("arc-card")
                .style("padding: 8px; width: 100%;")
                .on("click", lambda cd=card_data: self._show_card_modal(cd))
            ):
                if has_image:
                    rotation_style = (
                        "transform: rotate(180deg);" if card.reversed else ""
                    )
                    ui.image(str(abs_image_path)).style(
                        f"width: 100%; height: auto; object-fit: contain; {rotation_style}"
                    )
                else:
                    with ui.element("div").style(
                        "width: 100%; height: 128px; display: flex; "
                        "align-items: center; justify-content: center;"
                    ):
                        ui.html(
                            '<span style="font-size: 3em; color: var(--gold-dim);">✧</span>'
                        )

            label_text = f"⟲ {position_name}" if rotation != 0 else position_name
            ui.label(label_text).classes("arc-card-label")

    def _show_card_modal(self, card_data: dict):
        """Update drawer content and show it with card details."""
        if self.card_drawer is None:
            return

        card = card_data["card"]
        position_name = card_data["name"]
        card_name = card.get_display_name()

        self.card_drawer_content.clear()

        with self.card_drawer_content:
            # Header
            with ui.row().style(
                "width: 100%; align-items: center; justify-content: space-between; "
                "padding: 16px; border-bottom: 1px solid "
                "color-mix(in srgb, var(--gold-dim) 25%, transparent);"
            ):
                ui.label(card_name).classes("arc-subheading").style("font-size: 22px;")
                ui.button(icon="close", on_click=self.card_drawer.hide).props(
                    "flat dense round"
                ).style("color: var(--gold);")

            # Content
            with ui.column().style("gap: 24px; width: 100%; padding: 24px;"):
                try:
                    image_path = card.get_image_filename()
                    abs_path = PROJECT_ROOT / image_path
                    if abs_path.exists():
                        with ui.row().style(
                            "width: 100%; justify-content: center; margin-bottom: 16px;"
                        ):
                            ui.image(str(abs_path)).style("width: 280px; height: auto;")
                except AttributeError:
                    pass

                ui.label(f"Position: {position_name}").classes("arc-label").style(
                    "font-size: 14px; letter-spacing: 1px;"
                )

                position_desc = card_data.get("short_description", "")
                if position_desc:
                    ui.label(position_desc).classes("arc-muted").style(
                        "font-size: 14px;"
                    )

                divider()

                position_meaning = card_data.get("position_meaning", "")
                if position_meaning:
                    ui.label("Position Interpretation").classes("arc-label")
                    ui.label(position_meaning).classes("arc-body").style(
                        "font-size: 15px;"
                    )
                    divider()

                core = card_data.get("core_meaning", {})
                if core:
                    ui.label("Core Card Meaning").classes("arc-label")

                    essence = core.get("essence", "")
                    if essence:
                        ui.label(essence).classes("arc-muted").style(
                            "font-size: 15px; margin-bottom: 12px;"
                        )

                    keywords = core.get("keywords", [])
                    if keywords:
                        ui.label(f"Keywords: {', '.join(keywords)}").classes(
                            "arc-body"
                        ).style("font-size: 13px; margin-bottom: 12px;")

                    practical = core.get("practical", "")
                    if practical:
                        ui.label("Practical Guidance").classes("arc-label")
                        ui.label(practical).classes("arc-body").style(
                            "font-size: 15px;"
                        )

            # Close button
            with ui.row().style(
                "width: 100%; justify-content: center; padding: 16px; "
                "border-top: 1px solid "
                "color-mix(in srgb, var(--gold-dim) 25%, transparent);"
            ):
                with (
                    ui.element("button")
                    .classes("arc-btn-secondary")
                    .style("padding: 8px 24px;")
                    .on("click", self.card_drawer.hide)
                ):
                    ui.label("Close")

        self.card_drawer.show()

    # ================================================================
    # READER STATS
    # ================================================================

    def get_reader_stats(self) -> dict:
        """Get reader stats from engine state, with defaults."""
        if self.engine is None:
            return {
                "sessions_completed": 0,
                "coins_earned": 0,
                "reader_level": 1,
                "experience": 0,
            }

        state = self.engine.state
        reader = state.get("reader")

        return {
            "sessions_completed": reader.sessions_completed if reader else 0,
            "coins_earned": reader.money if reader else 0,
            "reader_level": reader.get_level() if reader else "Novice",
            "experience": reader.experience if reader else 0,
        }


# ============================================================================
# PAGE ROUTE — each client gets their own GameSession
# ============================================================================


@ui.page("/")
def index():
    session = GameSession()
    session.build()


# Debug mode (only in development)
import os

if not os.environ.get("RAILWAY_ENVIRONMENT"):
    from debug_page import register_debug_routes

    register_debug_routes()


# ============================================================================
# SERVER ENTRY POINT
# ============================================================================

if __name__ in {"__main__", "__mp_main__"}:
    import os

    port = int(os.environ.get("PORT", 8080))
    is_production = os.environ.get("RAILWAY_ENVIRONMENT") is not None

    if is_production:
        ui.run(
            title="Arcanum",
            favicon="🔮",
            host="0.0.0.0",
            port=port,
            reload=False,
            show=False,
        )
    else:
        ui.run(title="Arcanum", favicon="🔮")
