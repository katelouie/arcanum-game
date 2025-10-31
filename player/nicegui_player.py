from nicegui import ui, app
import json
from pathlib import Path
import sys
import markdown

# Import from installed bardic package
from bardic.runtime.engine import BardEngine

# Import local save manager (from same directory)
sys.path.insert(0, str(Path(__file__).parent))
from save_manager import SaveManager

# Make sure to include game_logic directory
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set the story ID
STORY_ID = "arcanum"

# Add assets as static files so they're accessible via URLs (for favicon, images, etc.)
app.add_static_files("/assets", str(Path(__file__).parent.parent / "assets"))

# CSS Reset + Body Styling (fix white border)
ui.add_head_html("""
<style>
    /* Only reset body/html, not everything */
    html, body {
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        background-color: #000000;
        overflow-x: hidden;
        box-sizing: border-box;
    }
</style>
""")

# Google Fonts
ui.add_head_html("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300&family=Lora:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
<style>
    .font-serif { font-family: 'Cinzel', serif; }
    .font-light { font-family: 'Cormorant Garamond', serif; }
    .font-semibold { font-family: 'Cinzel', serif; }
    .font-body { font-family: 'Lora', serif; }
</style>
""")

ui.add_head_html("""
<style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeIn 1s ease-out;
    }
</style>
""")

# Set your color theme
ui.colors(
    primary="#6B46C1",  # Deep purple
    secondary="#D4AF37",  # Gold
    accent="#4A5568",  # Slate gray
    dark="#1A202C",  # Almost black
    positive="#9F7AEA",  # Light purple
)

# ============================================================================
# GLOBAL STATE
# ============================================================================

# Current screen: "landing", "player", "dashboard"
current_screen = "landing"

# Story engine (loaded when player starts)
engine = None

# Main container that will hold all screens
main_container = None

# Card detail drawer (created at page level)
card_drawer = None
card_drawer_content = None

# SaveManager instance
project_root = Path(__file__).resolve().parent.parent
save_manager = SaveManager(project_root / "saves")

# ============================================================================
# STORY LOADING
# ============================================================================


def load_story(story_path: str):
    """Load a compiled story JSON and create BardEngine instance."""
    global engine

    with open(story_path) as f:
        story_data = json.load(f)

    # Create engine with empty context for now
    engine = BardEngine(story_data, context={})


# ============================================================================
# NAVIGATION
# ============================================================================


def navigate_to(screen: str):
    """Switch to a different screen."""
    global current_screen
    current_screen = screen
    update_ui()


def update_ui():
    """Rebuild the UI based on current screen."""
    main_container.clear()

    with main_container:
        if current_screen == "landing":
            show_landing()
        elif current_screen == "player":
            show_player()
        elif current_screen == "dashboard":
            show_dashboard()


# ============================================================================
# LANDING PAGE
# ============================================================================


def show_landing():
    """Display the landing page."""
    with ui.column().classes(
        "min-h-screen w-screen bg-gradient-to-b from-purple via-purple-950 to-black flex items-center justify-center m-0 p-8"
    ):
        # Main title
        ui.label("ARCANUM").classes(
            "text-7xl font-serif text-amber-400 border-b-4 border-amber-600/50 pb-4 fade-in"
        )

        # Subtitle
        ui.label("A Digital Cartomancer's Tale").classes(
            "text-2xl font-light text-purple-200 italic mb-16 tracking-wide"
        )

        # Central card image or mystical symbol
        with ui.card().classes(
            "bg-white/10 backdrop-blur-sm border border-purple-400/30 shadow-2xl p-8 mb-12"
        ):
            ui.html("🔮", sanitize=False).classes("text-9xl animate-pulse")

        # Action buttons
        with ui.column().classes("gap-4 w-80"):
            ui.button("Begin Reading", on_click=lambda: start_new_game()).classes(
                "w-full py-4 text-xl bg-purple-600 "
                "text-white font-semibold rounded-full shadow-lg "
                "hover:bg-purple-700 hover:scale-105 "
                "transition-all duration-300 tracking-wide"
            )

            ui.button("Continue Journey", on_click=lambda: show_load_dialog()).classes(
                "w-full py-4 text-xl bg-purple-900/50 backdrop-blur-sm "
                "text-purple-200 font-semibold rounded-full shadow-lg border border-purple-400/30 "
                "hover:bg-purple-800/50 hover:scale-105 "
                "transition-all duration-300 tracking-wide"
            )

            ui.button(
                "View Reading Table", on_click=lambda: navigate_to("dashboard")
            ).classes(
                "w-full py-4 text-xl bg-purple-900/50 backdrop-blur-sm "
                "text-purple-200 font-semibold rounded-full shadow-lg border border-purple-400/30 "
                "hover:bg-purple-800/50 hover:scale-105 "
                "transition-all duration-300 tracking-wide"
            )


# ============================================================================
# SAVE/LOAD FUNCTIONALITY
# ============================================================================


def show_save_dialog():
    """Show dialog to save the current game."""
    with (
        ui.dialog() as dialog,
        ui.card().classes("bg-purple-950 border border-purple-400/30 p-6"),
    ):
        ui.label("Save Your Reading").classes("text-2xl font-serif text-amber-400 mb-4")

        save_name_input = (
            ui.input(label="Save Name", placeholder="e.g., Before meeting the hermit")
            .classes("w-full mb-4")
            .props("dark")
        )

        with ui.row().classes("gap-2 w-full justify-end"):
            ui.button("Cancel", on_click=dialog.close).classes(
                "px-4 py-2 bg-purple-900/50 text-purple-200 rounded-lg"
            )

            ui.button(
                "Save", on_click=lambda: save_game_action(save_name_input.value, dialog)
            ).classes("px-4 py-2 bg-purple-600 text-white rounded-lg")

    dialog.open()


def save_game_action(save_name: str, dialog):
    """Actually perform the save."""
    if not save_name:
        ui.notify("Please enter a save name", type="warning")
        return

    try:
        # Get engine state
        engine_state = engine.save_state()

        # Save using SaveManager
        result = save_manager.save_game(save_name, engine_state)

        ui.notify(f"Saved: {save_name}", type="positive")
        dialog.close()

    except Exception as e:
        ui.notify(f"Save failed: {str(e)}", type="negative")


def show_load_dialog():
    """Show dialog to load a saved game."""
    saves = save_manager.list_saves()

    with (
        ui.dialog() as dialog,
        ui.card().classes("bg-purple-950 border border-purple-400/30 p-6 min-w-96"),
    ):
        ui.label("Load a Reading").classes("text-2xl font-serif text-amber-400 mb-4")

        if not saves:
            ui.label("No saved games found").classes("text-purple-200 italic mb-4")
        else:
            with ui.column().classes("gap-2 w-full max-h-96 overflow-y-auto"):
                for save in saves:
                    with (
                        ui.card()
                        .classes(
                            "bg-purple-900/30 border border-purple-400/20 p-4 cursor-pointer "
                            "hover:bg-purple-800/30 transition-all"
                        )
                        .on(
                            "click",
                            lambda s=save: load_game_action(s["save_id"], dialog),
                        )
                    ):
                        ui.label(save["save_name"]).classes(
                            "text-lg font-serif text-amber-300"
                        )
                        ui.label(f"Passage: {save['passage']}").classes(
                            "text-sm text-purple-200"
                        )
                        ui.label(save["date_display"]).classes(
                            "text-xs text-purple-300 italic"
                        )

        with ui.row().classes("gap-2 w-full justify-end mt-4"):
            ui.button("Cancel", on_click=dialog.close).classes(
                "px-4 py-2 bg-purple-900/50 text-purple-200 rounded-lg"
            )

    dialog.open()


def load_game_action(save_id: str, dialog):
    """Actually perform the load."""
    try:
        # Load save data
        save_data = save_manager.load_game(save_id)

        # Load the story first (in case we're not already in a game)
        story_id = save_data.get("story_id", STORY_ID)
        story_path = project_root / "compiled_stories" / f"{story_id}.json"

        if not story_path.exists():
            ui.notify(f"Story file not found: {story_id}", type="negative")
            return

        load_story(str(story_path))

        # Restore engine state
        engine.load_state(save_data)

        ui.notify(f"Loaded: {save_data['save_name']}", type="positive")
        dialog.close()

        # Navigate to player screen
        navigate_to("player")

    except Exception as e:
        ui.notify(f"Load failed: {str(e)}", type="negative")


# ============================================================================
# PLAYER MODE
# ============================================================================


def start_new_game():
    """Start a new game - load story and navigate to player."""
    # Load the test story
    # __file__ is nicegui-player/nicegui_test_player.py
    # We need to go up to bardic/, then into compiled_stories/
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent  # nicegui-player -> bardic
    story_path = project_root / "compiled_stories" / f"{STORY_ID}.json"

    print(f"Loading story from: {story_path}")  # Debug
    load_story(str(story_path))

    # Navigate to player screen
    navigate_to("player")


def show_player():
    """Display the player mode."""
    # Get current passage from engine
    output = engine.current()

    # Check for UI layout tags on the passage
    passage = engine.passages.get(output.passage_id, {})
    passage_tags = passage.get("tags", [])

    # If passage has UI:DASHBOARD tag, show dashboard instead
    if "UI:DASHBOARD" in passage_tags:
        show_dashboard(output)
        return

    # Otherwise, show normal player UI
    with ui.column().classes(
        "min-h-screen w-screen bg-gradient-to-b from-purple via-purple-950 to-black flex items-center justify-start m-0 p-8"
    ):
        # Header bar
        with ui.row().classes("w-full max-w-4xl justify-between items-center mb-8"):
            ui.label("ARCANUM").classes("text-4xl font-serif text-amber-400")

            with ui.row().classes("gap-2"):
                ui.button("Save", on_click=lambda: show_save_dialog()).classes(
                    "px-8 py-2 bg-purple-700/50 text-purple-200 rounded-lg "
                    "hover:bg-purple-600/50 transition-all"
                )

                ui.button(
                    "Return to Table", on_click=lambda: navigate_to("dashboard")
                ).classes(
                    "px-8 py-2 bg-purple-900/50 text-purple-200 rounded-lg "
                    "border border-purple-400/30 hover:bg-purple-800/50 transition-all"
                )

        # Story card (centered, max-width)
        with ui.card().classes(
            "w-full max-w-4xl bg-white/10 backdrop-blur-sm border border-purple-400/30 "
            "shadow-2xl fade-in"
        ):
            # Wrap everything in a padded column to ensure spacing
            with ui.column().classes("p-12 w-full"):
                # Passage text - convert markdown to HTML with newline preservation
                html_content = markdown.markdown(
                    output.content,
                    extensions=["nl2br"],  # Converts \n to <br>
                )
                ui.html(html_content, sanitize=False).classes(
                    "text-xl font-body text-purple-100 mb-8 leading-relaxed [&_p]:mb-6"
                )

                # Render directives (between text and choices)
                if hasattr(output, "render_directives") and output.render_directives:
                    with ui.column().classes("w-full my-8"):
                        for directive in output.render_directives:
                            render_directive(directive)

                # Input directives (text input forms)
                if hasattr(output, "input_directives") and output.input_directives:
                    render_input_form(output.input_directives)

                # Choices - categorize by tags
                if output.choices:
                    # Separate choices by type
                    client_choices = []
                    special_choices = []
                    meta_choices = []
                    regular_choices = []

                    for i, choice in enumerate(output.choices):
                        tags = choice.get("tags", [])
                        has_client_tag = any(tag.startswith("CLIENT") for tag in tags)
                        is_special = any("SPECIAL" in tag for tag in tags)
                        is_meta = any(tag.startswith("META") for tag in tags)

                        if has_client_tag and is_special:
                            special_choices.append((i, choice))
                        elif has_client_tag:
                            client_choices.append((i, choice))
                        elif is_meta:
                            meta_choices.append((i, choice))
                        else:
                            regular_choices.append((i, choice))

                    # Render normal client cards (purple) - GRID LAYOUT
                    if client_choices:
                        ui.label("Available Clients").classes(
                            "text-2xl font-serif font-bold text-amber-300 mb-4"
                        )
                        with ui.grid(columns=3).classes("gap-4 w-full mb-6"):
                            for idx, choice in client_choices:
                                render_client_card(choice, idx, is_special=False)

                    # Render special consultation cards (blue) - GRID LAYOUT
                    if special_choices:
                        ui.label("Special Consultations").classes(
                            "text-2xl font-serif font-bold text-blue-300 mb-4"
                        )
                        with ui.grid(columns=3).classes("gap-4 w-full mb-6"):
                            for idx, choice in special_choices:
                                render_client_card(choice, idx, is_special=True)

                    # Render regular choices (button style)
                    if regular_choices:
                        ui.label("What do you do?").classes(
                            "text-2xl font-serif font-bold text-amber-300 mb-4"
                        )
                        with ui.column().classes("gap-3 w-full mb-6"):
                            for idx, choice in regular_choices:
                                ui.button(
                                    choice["text"],
                                    on_click=lambda i=idx: make_choice(i),
                                ).classes(
                                    "w-full py-3 px-6 text-lg bg-purple-600 "
                                    "text-white font-light rounded-lg shadow-lg "
                                    "hover:bg-purple-700 hover:scale-105 "
                                    "transition-all duration-200 text-left"
                                )

                    # Render meta options (subtle buttons at bottom)
                    if meta_choices:
                        with ui.column().classes("gap-2 w-full mt-4"):
                            for idx, choice in meta_choices:
                                ui.button(
                                    choice["text"],
                                    on_click=lambda i=idx: make_choice(i),
                                ).classes(
                                    "w-full py-2 px-4 text-sm bg-purple-900/30 "
                                    "text-purple-300 font-light rounded-lg "
                                    "border border-purple-400/20 "
                                    "hover:bg-purple-800/30 transition-all text-center"
                                )
                else:
                    # No choices = THE END
                    ui.label("✧ THE END ✧").classes(
                        "text-3xl font-serif text-amber-300 italic mt-8 text-center"
                    )


def render_input_form(input_directives: list[dict]):
    """Render text input form from input directives.

    Args:
        input_directives: List of input directive dicts with name, label, placeholder
    """
    # Store input widgets for later access
    input_widgets = {}

    with ui.column().classes(
        "w-full gap-4 my-6 p-6 bg-purple-900/20 border border-purple-400/30 rounded-lg"
    ):
        # Render each input field
        for spec in input_directives:
            name = spec.get("name", "")
            label = spec.get("label", name.replace("_", " ").title())
            placeholder = spec.get("placeholder", "")

            # Create input widget with purple/amber styling
            input_widgets[name] = (
                ui.input(label=label, placeholder=placeholder)
                .classes("w-full text-purple-100")
                .props("dark outlined")
            )

        # Submit button
        ui.button(
            "Submit", on_click=lambda: submit_inputs_action(input_widgets)
        ).classes(
            "mt-4 px-8 py-3 bg-purple-600 text-white font-semibold rounded-lg "
            "hover:bg-purple-700 hover:scale-105 transition-all shadow-lg"
        )


def submit_inputs_action(input_widgets: dict):
    """Collect input data and submit to engine.

    Args:
        input_widgets: Dict mapping input names to NiceGUI input widgets
    """
    # Collect values from input widgets
    input_data = {
        name: widget.value or ""  # Use empty string if None
        for name, widget in input_widgets.items()
    }

    # Submit to engine
    engine.submit_inputs(input_data)

    # Re-navigate to current passage to re-render with new state
    # (engine.current() returns cached output, we need fresh render)
    current_passage_id = engine.current_passage_id
    engine.goto(current_passage_id)

    # Re-render UI to show submitted state
    update_ui()


def render_directive(directive: dict):
    """Route a render directive to the appropriate rendering function.

    Args:
        directive: Directive dict with 'name', 'data', 'mode', etc.
    """
    directive_name = directive.get("name", "")
    directive_data = directive.get("data", {})  # Changed from 'args' to 'data'

    if directive_name == "render_spread":
        # Legacy: simple card list with spread name
        render_card_spread(directive_data)
    elif directive_name == "render_reading":
        # New: full Reading object with spread layout
        render_reading(directive_data)
    else:
        # Unknown directive - show debug info
        ui.label(f"Unknown directive: {directive_name}").classes("text-red-400 text-sm")


def render_card_spread(args: dict):
    """Render a tarot card spread with actual card images.

    Args:
        args: Dict with 'cards' (list) and 'spread' (str) keys
    """
    cards = args.get("cards", [])
    spread_name = args.get("spread", "Card Spread")

    # Spread title
    ui.label(spread_name.replace("-", " ").replace("_", " ").title()).classes(
        "text-2xl font-serif font-bold text-amber-300 mb-4"
    )

    # Card boxes in a horizontal row
    with ui.row().classes("gap-6 w-full justify-center"):
        for card in cards:
            # Get card attributes - handle both dict and object
            if isinstance(card, dict):
                card_name = card.get("name", "Unknown Card")
                is_reversed = card.get("reversed", False)
                # For dict, we can't get image path directly - use placeholder
                image_path = None
            else:
                card_name = getattr(card, "name", "Unknown Card")
                is_reversed = getattr(card, "reversed", False)
                # Get actual image path from card object
                try:
                    image_path = card.get_image_filename()
                    # Convert to absolute path for NiceGUI
                    from pathlib import Path

                    abs_image_path = Path(__file__).parent.parent / image_path
                    if not abs_image_path.exists():
                        print(f"Warning: Card image not found: {abs_image_path}")
                        image_path = None
                except AttributeError:
                    image_path = None

            # Card box with image
            with ui.card().classes(
                "w-40 h-auto flex items-center justify-center "
                "bg-purple-900/30 border-2 border-amber-400/50 "
                "hover:border-amber-300 transition-all cursor-pointer p-2"
            ):
                with ui.column().classes("items-center justify-center gap-2"):
                    # Card image or placeholder
                    if image_path and abs_image_path.exists():
                        # Show actual card image
                        rotation_class = "rotate-180" if is_reversed else ""
                        ui.image(str(abs_image_path)).classes(
                            f"w-36 h-auto object-contain {rotation_class}"
                        )
                    else:
                        # Fallback placeholder
                        reversed_icon = "↓ " if is_reversed else ""
                        ui.icon("style", size="3em").classes("text-amber-300/50")

                    # Card name below image
                    display_name = f"↓ {card_name}" if is_reversed else card_name
                    ui.label(display_name).classes(
                        "text-center text-sm font-light text-purple-100 mt-2"
                    )


def render_reading(args: dict):
    """Render a full Reading object with spread layout.

    Args:
        args: Dict with 'reading' key containing Reading object
    """
    from pathlib import Path

    reading = args.get("reading")
    if not reading:
        ui.label("Error: No reading provided").classes("text-red-400")
        return

    # Get positioned cards (cards merged with position data)
    positioned_cards = reading.get_positioned_cards()
    spread = reading.spread

    # Spread title
    ui.label(spread.name).classes("text-2xl font-serif font-bold text-amber-300 mb-6")

    # Map card sizes to pixel widths
    card_widths = {
        "large": 180,  # 3-card spreads
        "medium": 140,  # 5-7 card spreads
        "small": 100,  # Celtic Cross, Year Ahead
    }
    card_width = card_widths.get(spread.card_size, 140)

    # Container with aspect ratio
    # Higher aspect ratio = shorter container (horizontal spreads)
    # Lower aspect ratio = taller container (vertical spreads like Celtic Cross)
    base_height = 600
    if spread.aspect_ratio:
        container_height = max(500, int(base_height / spread.aspect_ratio))
    else:
        container_height = base_height

    # Relative positioning container
    with (
        ui.element("div")
        .classes("relative w-full mx-auto")
        .style(f"height: {container_height}px; max-width: 800px;")
    ):
        for card_data in positioned_cards:
            card = card_data["card"]
            x = card_data["x"]  # Percentage (0-100)
            y = card_data["y"]  # Percentage (0-100)
            position_name = card_data["name"]
            rotation = card_data.get("rotation", 0)
            z_index = card_data.get("zIndex", 1)

            # Position card absolutely
            transform = f"translate(-50%, -50%) rotate({rotation}deg)"

            with ui.element("div").style(
                f"position: absolute; "
                f"left: {x}%; "
                f"top: {y}%; "
                f"transform: {transform}; "
                f"z-index: {z_index};"
            ):
                render_single_card(card_data, card_width)


def render_single_card(card_data: dict, width: int):
    """Render a single card with image, position label, and click handler.

    Args:
        card_data: Full positioned card dict with card, position, meanings, etc.
        width: Card width in pixels
    """
    from pathlib import Path

    card = card_data["card"]
    position_name = card_data["name"]
    rotation = card_data.get("rotation", 0)

    # Get image path
    try:
        image_path = card.get_image_filename()
        abs_image_path = Path(__file__).parent.parent / image_path
        has_image = abs_image_path.exists()
    except AttributeError:
        has_image = False

    # Card container
    with ui.column().classes("items-center gap-2").style(f"width: {width}px"):
        # Card image with click handler and hover effect
        with (
            ui.card()
            .classes(
                "p-2 bg-purple-900/30 border-2 border-amber-400/50 "
                "hover:border-amber-300 hover:scale-105 "  # Added hover scale
                "transition-all duration-200 cursor-pointer w-full"
            )
            .on("click", lambda cd=card_data: show_card_modal(cd))
        ):
            if has_image:
                # Actual card image
                card_rotation = "rotate-180" if card.reversed else ""
                ui.image(str(abs_image_path)).classes(
                    f"w-full h-auto object-contain {card_rotation}"
                )
            else:
                # Fallback placeholder
                with ui.column().classes("items-center justify-center h-32"):
                    ui.icon("style", size="3em").classes("text-amber-300/50")

        # Position label only (card name is visible in the image itself)
        label_class = (
            "text-center text-xs font-semibold text-amber-200 uppercase tracking-wide"
        )

        if rotation != 0:
            # Rotated card - label with rotation indicator
            ui.label(f"⟲ {position_name}").classes(f"{label_class} mt-1")
        else:
            # Normal card - label below
            ui.label(position_name).classes(f"{label_class} mt-1")


def show_card_modal(card_data: dict):
    """Update drawer content and show it with card details.

    Args:
        card_data: Dict from get_positioned_cards() with card, position, meanings
    """
    global card_drawer, card_drawer_content

    if card_drawer is None:
        return  # Drawer not initialized yet

    from pathlib import Path

    card = card_data["card"]
    position_name = card_data["name"]
    card_name = card.get_display_name()

    # Clear and rebuild drawer content
    card_drawer_content.clear()

    with card_drawer_content:
        # Header with close button
        with ui.row().classes(
            "w-full items-center justify-between p-4 border-b border-amber-400/30"
        ):
            ui.label(card_name).classes("text-2xl font-serif text-amber-300 font-bold")
            ui.button(icon="close", on_click=card_drawer.hide).props(
                "flat dense round"
            ).classes("text-amber-300")

        # Content (drawer handles scrolling natively)
        with ui.column().classes("gap-6 w-full p-6"):
            # Card image (centered, nice size)
            image_path = card.get_image_filename()
            abs_path = Path(__file__).parent.parent / image_path
            if abs_path.exists():
                with ui.row().classes("w-full justify-center mb-4"):
                    ui.image(str(abs_path)).classes("rounded-lg shadow-2xl").style(
                        "width: 280px; height: auto;"
                    )

            # Position section
            ui.label(f"Position: {position_name}").classes(
                "text-lg font-serif text-amber-200 font-semibold"
            )

            position_desc = card_data.get("short_description", "")
            if position_desc:
                ui.label(position_desc).classes("text-sm text-purple-200 italic")

            # Divider
            ui.separator().classes("bg-amber-400/20 my-2")

            # Position meaning
            position_meaning = card_data.get("position_meaning", "")
            if position_meaning:
                ui.label("Position Interpretation").classes(
                    "text-sm font-serif text-amber-300 font-semibold uppercase tracking-wide"
                )
                ui.label(position_meaning).classes(
                    "text-sm text-purple-100 leading-relaxed"
                )

                # Divider
                ui.separator().classes("bg-amber-400/20 my-4")

            # Core meaning
            core = card_data.get("core_meaning", {})
            if core:
                ui.label("Core Card Meaning").classes(
                    "text-sm font-serif text-amber-300 font-semibold uppercase tracking-wide"
                )

                essence = core.get("essence", "")
                if essence:
                    ui.label(essence).classes(
                        "text-sm text-purple-100 italic leading-relaxed mb-3"
                    )

                keywords = core.get("keywords", [])
                if keywords:
                    ui.label(f"Keywords: {', '.join(keywords)}").classes(
                        "text-xs text-purple-200 mb-3"
                    )

                practical = core.get("practical", "")
                if practical:
                    ui.label("Practical Guidance:").classes(
                        "text-xs font-serif text-amber-300 font-semibold uppercase tracking-wide mt-2"
                    )
                    ui.label(practical).classes(
                        "text-sm text-purple-100 leading-relaxed"
                    )

        # Close button at bottom
        with ui.row().classes("w-full justify-center p-4 border-t border-amber-400/30"):
            ui.button("Close", on_click=card_drawer.hide).classes(
                "px-6 py-2 bg-amber-600/20 text-amber-300 rounded-lg "
                "hover:bg-amber-600/30 transition-all"
            )

    # Show the drawer
    card_drawer.show()


def render_client_card(choice: dict, choice_index: int, is_special: bool = False):
    """Render a clickable client card as horizontal business card style.

    Args:
        choice: The choice dict with text, tags, etc.
        choice_index: Index for make_choice()
        is_special: True for special clients (blue), False for normal (purple)
    """
    client_name = choice["text"]  # e.g., "Elena Hart"

    # Extract flavor text from engine state using ^var: tag
    flavor_text = ""
    tags = choice.get("tags", [])
    for tag in tags:
        if tag.startswith("var:"):
            var_name = tag.split(":", 1)[1]  # "var:elena" → "elena"
            client_obj = engine.state.get(var_name)
            if client_obj and hasattr(client_obj, "flavor_text"):
                flavor_text = client_obj.flavor_text
            break

    # Determine colors based on type
    if is_special:
        bg_color = "bg-blue-900/20"
        border_color = "border-blue-400/30"
        hover_classes = "hover:bg-blue-800/30 hover:shadow-2xl hover:-translate-y-1"
        title_color = "text-blue-200"
        desc_color = "text-blue-300/80"
    else:
        bg_color = "bg-purple-900/20"
        border_color = "border-purple-400/30"
        hover_classes = "hover:bg-purple-800/30 hover:shadow-2xl hover:-translate-y-1"
        title_color = "text-purple-200"
        desc_color = "text-purple-300/80"

    # Business card: horizontal layout, fixed width
    with (
        ui.card()
        .classes(
            f"{bg_color} {border_color} border-2 p-6 cursor-pointer "
            f"{hover_classes} transition-all duration-300 shadow-xl rounded-xl "
            "min-w-80 max-w-md"
        )
        .on("click", lambda: make_choice(choice_index))
    ):
        with ui.column().classes("gap-2 w-full"):
            # Client name (large, Cinzel)
            ui.label(client_name).classes(
                f"text-2xl font-serif {title_color} tracking-wide"
            )

            # Flavor text (smaller, Lora, italic)
            if flavor_text:
                ui.label(flavor_text).classes(
                    f"text-sm font-body {desc_color} italic leading-relaxed"
                )


def make_choice(choice_index: int):
    """Handle player choice and update the story."""
    # Make the choice in the engine
    engine.choose(choice_index)

    # Rebuild the UI to show new passage
    update_ui()


# ============================================================================
# DASHBOARD / READER'S TABLE
# ============================================================================


def get_reader_stats():
    """Get reader stats from engine state, with defaults."""
    if engine is None:
        return {
            "sessions_completed": 0,
            "coins_earned": 0,
            "reader_level": 1,
            "experience": 0,
        }

    state = engine.state

    # Get reader object if it exists (it's a Reader instance from the story)
    reader = state.get("reader")

    return {
        "sessions_completed": state.get(
            "completed_sessions", 0
        ),  # Match story variable
        "coins_earned": state.get("total_earnings", 0),  # Match story variable
        "reader_level": reader.get_level()
        if reader
        else "Novice",  # Descriptive level (string)
        "experience": reader.experience if reader else 0,  # Numeric XP
    }


def calculate_level_progress(experience: int, level: int) -> tuple[int, int]:
    """Calculate progress to next level. Returns (current_xp, xp_needed)."""
    # Simple progression: level * 100 XP needed for next level
    xp_for_next_level = level * 100
    return (experience % xp_for_next_level, xp_for_next_level)


def show_dashboard(output=None):
    """Display the reading table / dashboard.

    Args:
        output: Optional PassageOutput from ReaderDesk passage. If provided,
                renders dynamically from passage content/choices.
    """
    with ui.column().classes(
        "min-h-screen w-screen bg-gradient-to-b from-purple via-purple-950 to-black flex items-center justify-start m-0 p-8"
    ):
        # Header
        with ui.row().classes("w-full max-w-6xl justify-between items-center mb-8"):
            with ui.column().classes("gap-1"):
                ui.label("ARCANUM").classes("text-5xl font-serif text-amber-400")
                ui.label("The Reading Table").classes(
                    "text-xl font-light text-purple-200 italic"
                )

            with ui.row().classes("gap-2"):
                # Save button
                ui.button("Save", on_click=lambda: show_save_dialog()).classes(
                    "px-8 py-2 bg-purple-700/50 text-purple-200 rounded-lg "
                    "hover:bg-purple-600/50 transition-all"
                )

                # Return to landing button
                ui.button(
                    "Return to Landing", on_click=lambda: navigate_to("landing")
                ).classes(
                    "px-8 py-2 bg-purple-900/50 text-purple-200 rounded-lg "
                    "border border-purple-400/30 hover:bg-purple-800/50 transition-all"
                )

        # Stats Section
        stats = get_reader_stats()

        with ui.row().classes("w-full max-w-6xl gap-4 mb-8"):
            # Sessions Completed Card
            with ui.card().classes(
                "bg-white/10 backdrop-blur-sm border border-purple-400/30 shadow-lg flex-1"
            ):
                with ui.column().classes("p-6 items-center gap-2"):
                    ui.label("Sessions Completed").classes(
                        "text-base font-serif font-bold text-purple-200 uppercase tracking-wide"
                    )
                    ui.label(str(stats["sessions_completed"])).classes(
                        "text-5xl font-serif text-amber-400"
                    )

            # Coins Earned Card
            with ui.card().classes(
                "bg-white/10 backdrop-blur-sm border border-purple-400/30 shadow-lg flex-1"
            ):
                with ui.column().classes("p-6 items-center gap-2"):
                    ui.label("Money Earned").classes(
                        "text-base font-serif font-bold text-purple-200 uppercase tracking-wide"
                    )
                    ui.label(f"{stats['coins_earned']} 🪙").classes(
                        "text-5xl font-serif text-amber-400"
                    )

            # Reader Level Card
            with ui.card().classes(
                "bg-white/10 backdrop-blur-sm border border-purple-400/30 shadow-lg flex-1"
            ):
                with ui.column().classes("p-6 items-center gap-2"):
                    ui.label("Reader Level").classes(
                        "text-base font-serif font-bold text-purple-200 uppercase tracking-wide"
                    )
                    ui.label(str(stats["reader_level"])).classes(
                        "text-5xl font-serif text-amber-400"
                    )

        # Experience Progress Bar
        # Calculate numeric level from experience (every 100 XP = 1 level)
        experience = stats["experience"]
        numeric_level = (
            experience // 100
        ) + 1  # Level 1 at 0-99 XP, Level 2 at 100-199, etc.

        current_xp, xp_needed = calculate_level_progress(experience, numeric_level)
        progress_percent = (current_xp / xp_needed * 100) if xp_needed > 0 else 0

        with ui.card().classes(
            "w-full max-w-6xl bg-white/10 backdrop-blur-sm border border-purple-400/30 shadow-lg mb-12"
        ):
            with ui.column().classes("p-6 gap-3"):
                ui.label("Experience").classes(
                    "text-base font-serif font-bold text-purple-200 uppercase tracking-wide"
                )
                with ui.row().classes("w-full items-center gap-3"):
                    # Progress bar background
                    with ui.element("div").classes(
                        "flex-1 h-4 bg-purple-900/50 rounded-full overflow-hidden"
                    ):
                        # Progress bar fill
                        ui.element("div").classes(
                            f"h-full bg-gradient-to-r from-purple-500 to-amber-400 transition-all"
                        ).style(f"width: {progress_percent}%")

                    ui.label(f"{current_xp}/{xp_needed} XP").classes(
                        "text-sm font-light text-purple-200 min-w-24 text-right"
                    )

        # Passage Content (if provided from ReaderDesk)
        if output and output.content:
            with ui.card().classes(
                "w-full max-w-6xl bg-white/10 backdrop-blur-sm border border-purple-400/30 shadow-lg mb-8"
            ):
                with ui.column().classes("p-8 w-full"):
                    # Render passage text with markdown
                    html_content = markdown.markdown(
                        output.content,
                        extensions=["nl2br"],
                    )
                    ui.html(html_content, sanitize=False).classes(
                        "text-lg font-body text-purple-100 leading-relaxed [&_p]:mb-6"
                    )

        # Client Selection Section (from passage choices if provided)
        if output and output.choices:
            with ui.card().classes(
                "w-full max-w-6xl bg-white/10 backdrop-blur-sm border border-purple-400/30 shadow-2xl fade-in"
            ):
                with ui.column().classes("p-12 w-full"):
                    # Categorize choices by tags
                    client_choices = []
                    special_choices = []
                    meta_choices = []
                    regular_choices = []

                    for i, choice in enumerate(output.choices):
                        tags = choice.get("tags", [])
                        has_client_tag = any(tag.startswith("CLIENT") for tag in tags)
                        is_special = any("SPECIAL" in tag for tag in tags)
                        is_meta = any(tag.startswith("META") for tag in tags)

                        if has_client_tag and is_special:
                            special_choices.append((i, choice))
                        elif has_client_tag:
                            client_choices.append((i, choice))
                        elif is_meta:
                            meta_choices.append((i, choice))
                        else:
                            regular_choices.append((i, choice))

                    # Render normal client cards (purple) - GRID LAYOUT
                    if client_choices:
                        ui.label("Available Clients").classes(
                            "text-2xl font-serif font-bold text-amber-300 mb-4"
                        )
                        with ui.grid(columns=3).classes("gap-4 w-full mb-6"):
                            for idx, choice in client_choices:
                                render_client_card(choice, idx, is_special=False)

                    # Render special consultation cards (blue) - GRID LAYOUT
                    if special_choices:
                        ui.label("Special Consultations").classes(
                            "text-2xl font-serif font-bold text-blue-300 mb-4 mt-6"
                        )
                        with ui.grid(columns=3).classes("gap-4 w-full mb-6"):
                            for idx, choice in special_choices:
                                render_client_card(choice, idx, is_special=True)

                    # Render regular choices (button style)
                    if regular_choices:
                        ui.label("What do you do?").classes(
                            "text-2xl font-serif font-bold text-amber-300 mb-4 mt-6"
                        )
                        with ui.column().classes("gap-3 w-full mb-6"):
                            for idx, choice in regular_choices:
                                ui.button(
                                    choice["text"],
                                    on_click=lambda i=idx: make_choice(i),
                                ).classes(
                                    "w-full py-3 px-6 text-lg bg-purple-600 "
                                    "text-white font-light rounded-lg shadow-lg "
                                    "hover:bg-purple-700 hover:scale-105 "
                                    "transition-all duration-200 text-left"
                                )

                    # Render meta options (subtle buttons at bottom)
                    if meta_choices:
                        with ui.column().classes("gap-2 w-full mt-4"):
                            for idx, choice in meta_choices:
                                ui.button(
                                    choice["text"],
                                    on_click=lambda i=idx: make_choice(i),
                                ).classes(
                                    "w-full py-2 px-4 text-sm bg-purple-900/30 "
                                    "text-purple-300 font-light rounded-lg "
                                    "border border-purple-400/20 "
                                    "hover:bg-purple-800/30 transition-all text-center"
                                )


# ============================================================================
# MAIN APP
# ============================================================================

# Create the main container
main_container = ui.column().classes("w-full h-full m-0 p-0")

# Create the card detail drawer (at page level, outside main container)
with (
    ui.right_drawer()
    .props("width=450 overlay elevated")
    .classes("bg-purple-950/90 border-l-4 border-amber-500/50") as card_drawer
):
    card_drawer_content = ui.column().classes("w-full h-full")

# Explicitly hide drawer on startup
card_drawer.hide()

# Initial render
update_ui()

ui.run(title="Arcanum", favicon="🔮")
