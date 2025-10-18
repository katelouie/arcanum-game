# Arcanum: A Digital Cartomancer's Tale

An interactive fiction game about becoming a tarot reader, built with [Bardic](https://github.com/katelouie/bardic).

## About

Arcanum is a narrative game where you play as an aspiring tarot reader building your practice. Meet clients, perform readings, manage your schedule, and grow your skills.

This game demonstrates what you can build with the Bardic interactive fiction engine:
- Custom Python classes (Card, Client objects)
- Dynamic UI with passage-level tags
- Save/load functionality
- Dashboard systems
- Object-oriented game state

## Features

- 📖 **Branching narrative** - Your choices shape your journey
- 🃏 **Tarot reading system** - Work with actual tarot card objects
- 👥 **Client management** - Build relationships with different clients
- 📊 **Progress tracking** - Level up and earn money
- 💾 **Save/load** - Save your progress at any time
- 🎨 **Beautiful UI** - Mystical purple/gold aesthetic

## Quick Start

### Prerequisites

- Python 3.12+
- pyenv (recommended)

### Installation

```bash
# Create and activate virtual environment
pyenv virtualenv 3.12 arcanum
pyenv activate arcanum

# Install dependencies
pip install -r requirements.txt
```

### Running the Game

```bash
# Compile the story (first time or after changes)
bardic compile stories/reader_journey.bard -o compiled_stories/reader_journey.json

# Run the player
python player/nicegui_test_player.py
```

Open your browser to `http://localhost:8080` and start playing!

## Project Structure

```
arcanum-game/
├── player/
│   ├── nicegui_test_player.py  # Main NiceGUI player application
│   └── save_manager.py         # Save/load system
├── game_logic/
│   └── test_tarot_objects.py   # Card and Client classes
├── stories/
│   └── reader_journey.bard     # Main story file
├── compiled_stories/           # Compiled JSON stories
├── assets/                     # Images, card meanings, etc.
├── saves/                      # Save game files
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Built With Bardic

This game is built with [Bardic](https://github.com/katelouie/bardic), a Python-first interactive fiction engine.

Want to create your own IF game? Check out Bardic:

```bash
pip install bardic
bardic init my-game
```

## Game Development

### Adding New Content

Edit `stories/reader_journey.bard` and recompile:

```bash
bardic compile stories/reader_journey.bard -o compiled_stories/reader_journey.json
```

### Custom Classes

The game uses custom Python classes defined in `game_logic/test_tarot_objects.py`:
- `Card` - Tarot card objects with serialization
- `Client` - Client profiles with flavor text

These objects are imported in the story and persist through saves.

### UI Customization

The player UI in `player/nicegui_test_player.py` includes:
- Landing page with gradient background
- Story player with centered layout
- Client cards with business card styling
- Dashboard for client management
- Save/load dialogs

All styling uses Tailwind CSS classes and can be customized.

## Story Features

Arcanum demonstrates advanced Bardic features:

- **@metadata** - Story metadata for save/load
- **Python blocks** - Dynamic variable calculations
- **Conditionals** - Branching based on state
- **Loops** - Iterating over collections
- **Tags** - Passage-level UI routing (`^UI:DASHBOARD`)
- **Custom objects** - Full Python class integration

## License

This game is an example project demonstrating the Bardic engine.

## Credits

Built with:
- [Bardic](https://github.com/katelouie/bardic) - Interactive fiction engine
- [NiceGUI](https://nicegui.io/) - Python UI framework
- [Tailwind CSS](https://tailwindcss.com/) - Styling

Tarot card images and meanings sourced from public domain resources.
