"""Tarot game classes."""

import random
import json
from pathlib import Path
from typing import Optional

# Helper function to normalize suit names
def normalize_suit(suit: str) -> str:
    """Normalize suit names from tarot-images.json to internal format."""
    mapping = {
        "Majors": "major",
        "Cups": "cups",
        "Swords": "swords",
        "Wands": "wands",
        "Pentacles": "pentacles"
    }
    return mapping.get(suit, suit.lower())


def _load_all_cards() -> list["Card"]:
    """Load all 78 tarot cards from tarot-images.json."""
    # Get the path to tarot-images.json relative to this file
    assets_path = Path(__file__).parent.parent / "assets" / "images" / "tarot-images.json"

    with open(assets_path, 'r') as f:
        data = json.load(f)

    cards = []
    for card_data in data['cards']:
        # Parse number (it's a string in JSON)
        number = int(card_data['number'])

        # Normalize suit name
        suit = normalize_suit(card_data['suit'])

        # Create card
        card = Card(
            name=card_data['name'],
            suit=suit,
            number=number
        )
        cards.append(card)

    return cards


def _load_spreads_config() -> dict:
    """Load spreads-config.json at module init."""
    config_path = Path(__file__).parent / "spreads-config.json"
    with open(config_path, 'r') as f:
        return json.load(f)


def find_spread_by_id(spread_id: str) -> dict:
    """Find a spread in SPREADS_CONFIG by its ID.

    Args:
        spread_id: The ID of the spread (e.g., "past-present-future")

    Returns:
        The spread data dict from config

    Raises:
        ValueError: If spread_id not found
    """
    for spread in SPREADS_CONFIG['spreads']:
        if spread['id'] == spread_id:
            return spread
    raise ValueError(f"Spread '{spread_id}' not found in spreads-config.json")


class Card:
    def __init__(self, name, suit, number) -> None:
        self.name = name
        self.suit = suit
        self.number = number
        self.reversed = False
        self.position = None
        self._meaning_data = None  # Lazy load meaning JSON

    def __repr__(self) -> str:
        return f"Card({self.name}, {self.suit})"

    def set_reversed(self, is_reversed) -> None:
        self.reversed = is_reversed

    def in_position(self, position) -> "Card":
        self.position = position
        return self  # Allow chaining

    def get_display_name(self) -> str:
        prefix = "↓ " if self.reversed else ""
        return f"{prefix}{self.name}"

    def is_major(self) -> bool:
        return self.suit == "major"

    def is_minor(self) -> bool:
        return self.suit != "major" and self.number <= 10

    def is_court(self) -> bool:
        return self.suit != "major" and self.number > 10

    def get_position_meaning(self) -> str:
        meanings = {
            "past": "influences from your past",
            "present": "your current situation",
            "future": "potential outcomes",
        }
        return meanings.get(str(self.position), "unknown position")

    def _get_code(self) -> str:
        """Generate the filename code (e.g., 'm00', 'c05', 'w12')."""
        if self.suit == "major":
            return f"m{self.number:02d}"
        elif self.suit == "cups":
            return f"c{self.number:02d}"
        elif self.suit == "swords":
            return f"s{self.number:02d}"
        elif self.suit == "wands":
            return f"w{self.number:02d}"
        elif self.suit == "pentacles":
            return f"p{self.number:02d}"
        else:
            raise ValueError(f"Unknown suit: {self.suit}")

    def get_image_filename(self) -> str:
        """Return the full path to the card's image file."""
        code = self._get_code()
        # Return path relative to game root
        return f"assets/images/cards_wikipedia/{code}.jpg"

    def get_meaning_filename(self) -> str:
        """Return the full path to the card's meaning JSON file."""
        code = self._get_code()
        # Return path relative to game root
        return f"assets/text/card_meanings/{code}.json"

    def get_meaning_data(self) -> dict:
        """Load and cache card meaning JSON.

        Returns:
            Dict with core_meanings, position_interpretations, etc.
        """
        if self._meaning_data is None:
            meaning_file = self.get_meaning_filename()
            meaning_path = Path(__file__).parent.parent / meaning_file

            try:
                with open(meaning_path, 'r') as f:
                    self._meaning_data = json.load(f)
            except FileNotFoundError:
                print(f"Warning: Meaning file not found: {meaning_path}")
                self._meaning_data = {}
            except json.JSONDecodeError:
                print(f"Warning: Invalid JSON in meaning file: {meaning_path}")
                self._meaning_data = {}

        return self._meaning_data

    def get_core_meaning(self) -> dict:
        """Get core meaning based on reversed state.

        Returns:
            Dict with essence, keywords, psychological, spiritual, practical, shadow
        """
        data = self.get_meaning_data()
        if not data or 'core_meanings' not in data:
            return {}

        orientation = "reversed" if self.reversed else "upright"
        return data['core_meanings'].get(orientation, {})

    def get_position_meaning(self, rag_mapping: str) -> str:
        """Get position-specific meaning based on RAG mapping.

        Args:
            rag_mapping: Position mapping like "temporal_positions.past"

        Returns:
            Position-specific interpretation string (or empty if not found)
        """
        data = self.get_meaning_data()
        if not data or 'position_interpretations' not in data:
            return ""

        # Navigate nested dict: temporal_positions.past
        parts = rag_mapping.split('.')
        meaning = data['position_interpretations']

        for part in parts:
            if not isinstance(meaning, dict):
                return ""
            meaning = meaning.get(part, {})

        if not isinstance(meaning, dict):
            return ""

        orientation = "reversed" if self.reversed else "upright"
        return meaning.get(orientation, "")

    def to_save_dict(self) -> dict:
        """
        Serialize a card into a dictionary for saving.

        This method is called automatically by the engine when saving. You can
        customize what gets saved here.
        """
        return {
            "name": self.name,
            "number": self.number,
            "reversed": self.reversed,
            "suit": self.suit,
        }

    @classmethod
    def from_save_dict(cls, data: dict) -> "Card":
        """
        Restore a card from saved data.

        This method is called automatically by the engine when loading.
        It goes through __init__, so validation runs!
        """
        card = cls(
            name=data["name"],
            suit=data["suit"],
            number=data["number"],
        )
        card.set_reversed(data.get("reversed", False))

        return card


class Spread:
    """A tarot spread loaded from spreads-config.json.

    Combines layout coordinates with position meanings to create
    a complete spread definition.
    """

    def __init__(self, spread_id: str):
        """Load a spread by its ID from spreads-config.json.

        Args:
            spread_id: The spread ID (e.g., "past-present-future")
        """
        # Load spread data
        spread_data = find_spread_by_id(spread_id)

        # Load referenced layout
        layout_name = spread_data['layout']
        if layout_name not in SPREADS_CONFIG['layouts']:
            raise ValueError(f"Layout '{layout_name}' not found in spreads-config.json")
        layout_data = SPREADS_CONFIG['layouts'][layout_name]

        # Store metadata
        self.id = spread_id
        self.name = spread_data['name']
        self.description = spread_data['description']
        self.layout_name = layout_name
        self.card_size = spread_data['cardSize']  # "large", "medium", "small"
        self.aspect_ratio = spread_data['aspectRatio']
        self.category = spread_data['category']
        self.difficulty = spread_data['difficulty']

        # Merge layout coordinates into position data
        self.positions = []
        for i, pos_data in enumerate(spread_data['positions']):
            layout_pos = layout_data['positions'][i]

            # Merge position meaning + layout coords
            merged = {
                **pos_data,  # name, descriptions, keywords, rag_mapping, etc.
                **layout_pos  # x, y, rotation (optional), zIndex (optional)
            }
            self.positions.append(merged)

    def get_positioned_cards(self, cards: list["Card"]) -> list[dict]:
        """Combine drawn cards with their position data.

        Args:
            cards: List of drawn Card objects

        Returns:
            List of dicts with 'card' plus all position data (x, y, name, etc.)
        """
        positioned = []
        for i, card in enumerate(cards):
            if i < len(self.positions):
                positioned.append({
                    'card': card,
                    **self.positions[i]  # x, y, name, descriptions, keywords, etc.
                })
        return positioned

    def __repr__(self) -> str:
        return f"Spread({self.id}, {len(self.positions)} positions)"


class Deck:
    """Construct a Deck of Cards, either full or partial."""

    def __init__(self, cards: Optional[list[str]] = None) -> None:
        self.cards_raw = cards
        self.cards = []

        self._construct_deck()

    def _construct_deck(self):
        if self.cards_raw:
            for card_name in self.cards_raw:
                matching_cards = [c for c in ALL_CARDS if c.name == card_name]
                if not matching_cards:
                    print(f"Warning: Card '{card_name}' not found in ALL_CARDS")
                self.cards.extend(matching_cards)
        else:
            # Make a copy of ALL_CARDS to avoid modifying the original
            self.cards = ALL_CARDS.copy()

    def draw_card(self) -> Card:
        """Draw a card from the deck"""
        if not self.cards:
            raise ValueError("Cannot draw from an empty deck")
        return random.sample(self.cards, 1)[0]

    def draw_cards(self, count=1) -> list[Card]:
        """Draw multiple cards from the deck."""
        if count > len(self.cards):
            raise ValueError(f"Cannot draw {count} cards from deck with only {len(self.cards)} cards")
        return random.sample(self.cards, count)

    @classmethod
    def from_names(cls, card_names: list[str]) -> "Deck":
        """Create a deck from a list of card names."""
        return cls(cards=card_names)

    @classmethod
    def major_only(cls) -> "Deck":
        """Create a deck containing only major arcana cards."""
        deck = cls()
        deck.cards = [c for c in ALL_CARDS if c.is_major()]
        return deck

    @classmethod
    def suit(cls, suit_name: str) -> "Deck":
        """Create a deck containing only cards from a specific suit."""
        deck = cls()
        normalized_suit = normalize_suit(suit_name)
        deck.cards = [c for c in ALL_CARDS if c.suit == normalized_suit]
        return deck

    @classmethod
    def numbers(cls, min_num: int, max_num: int, suit_filter: Optional[str] = None) -> "Deck":
        """Create a deck containing only cards with numbers in the given range.

        Args:
            min_num: Minimum card number (inclusive)
            max_num: Maximum card number (inclusive)
            suit_filter: Optional suit to filter by (e.g., 'cups', 'major')
        """
        deck = cls()
        filtered = [c for c in ALL_CARDS if min_num <= c.number <= max_num]

        if suit_filter:
            normalized_suit = normalize_suit(suit_filter)
            filtered = [c for c in filtered if c.suit == normalized_suit]

        deck.cards = filtered
        return deck


class Reading:
    """A full tarot reading with spread layout and position meanings."""

    def __init__(
        self,
        spread_id: str,
        decks: Optional[list[Deck]] = None,
        allow_repeats: bool = False,
    ) -> None:
        """Create a reading with a specific spread.

        Args:
            spread_id: ID of spread from spreads-config.json (e.g., "past-present-future")
            decks: Optional list of Deck objects for each position (for curated draws)
            allow_repeats: Whether same card can appear in multiple positions
        """
        self.spread = Spread(spread_id)
        self.drawn_cards = []
        self.allow_repeats = allow_repeats

        # Create decks for each position
        if decks is None:
            self.decks = [Deck() for _ in range(len(self.spread.positions))]
        else:
            self.decks = decks

    def draw_cards(self) -> list["Card"]:
        """Draw cards for each position in the spread.

        Returns:
            The list of drawn cards
        """
        for p in range(len(self.spread.positions)):
            if not self.allow_repeats:
                position_pool = [
                    c for c in self.decks[p].cards if c not in self.drawn_cards
                ]

                if not position_pool:
                    raise Exception(f"No cards available for position {p}")
            else:  # Repeats allowed
                position_pool = self.decks[p].cards

            self.drawn_cards.extend(random.sample(position_pool, 1))

        return self.drawn_cards

    def get_positioned_cards(self) -> list[dict]:
        """Get drawn cards merged with their position data AND meanings.

        Returns:
            List of dicts with 'card', position data (x, y, name, descriptions),
            and meaning data (core_meaning, position_meaning)
        """
        positioned = self.spread.get_positioned_cards(self.drawn_cards)

        # Enhance with meaning data
        for card_data in positioned:
            card = card_data['card']

            # Get core meaning (upright/reversed)
            card_data['core_meaning'] = card.get_core_meaning()

            # Get position-specific meaning using RAG mapping
            rag_mapping = card_data.get('rag_mapping', '')
            if rag_mapping:
                card_data['position_meaning'] = card.get_position_meaning(rag_mapping)
            else:
                card_data['position_meaning'] = ""

        return positioned

    def __repr__(self) -> str:
        return f"Reading({self.spread.id}, {len(self.drawn_cards)} cards drawn)"


# Service function for drawing cards
def draw_cards(count=3):
    """Draw random cards from the full deck.

    This is a convenience function that creates a full deck and draws from it.
    For more control, create a Deck object directly.

    Args:
        count: Number of cards to draw (default 3)

    Returns:
        List of drawn Card objects, with random reversals applied
    """
    deck = Deck()  # Full 78-card deck
    drawn = deck.draw_cards(count)

    # Random reversals (30% chance per card)
    for card in drawn:
        if random.random() < 0.3:
            card.set_reversed(True)

    return drawn


# Initialize ALL_CARDS by loading from tarot-images.json
ALL_CARDS = _load_all_cards()

# Initialize SPREADS_CONFIG by loading from spreads-config.json
SPREADS_CONFIG = _load_spreads_config()
