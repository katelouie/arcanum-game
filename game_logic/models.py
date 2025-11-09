from dataclasses import dataclass, field
from random import randint
from typing import List, Optional

from game_logic.characters import Client, Nyx


@dataclass
class Session:
    """
    State for a single reading session.

    Resets between clients and tracks the quality, atmosphere, and focus
    of the current reading.
    """

    # === SESSION METADATA ===
    current_client: Optional[str] = None

    # === QUALITY METRICS ===
    _atmosphere: int = 0  # -3 to +5: Hostile to magical
    _quality: int = 0  # 0 to 5: How well session went
    _pacing: int = 0  # -2 to +2: Rushed vs thoughtful

    # === INTERPRETIVE FOCUS (unbounded, accumulates) ===
    mystical_focus: int = 0
    systemic_focus: int = 0
    relational_focus: int = 0
    practical_focus: int = 0
    dismissive_focus: int = 0

    # === ENVIRONMENTAL FACTORS ===
    weather_intensity: int = field(default_factory=lambda: randint(0, 3))
    _room_energy: int = 0  # -2 to +5: Drained to charged
    _tech_interference: int = 0  # 0 to 5: Electronic glitches

    # === CARD TRACKING ===
    past_card: Optional[str] = None  # Card drawn for past position
    present_card: Optional[str] = None  # Card drawn for present position
    future_card: Optional[str] = None  # Card drawn for future position
    # More cards will be added here for other types of spreads

    # === SESSION FLAGS ===
    deep_revelation_occurred: bool = False
    client_walked_out: bool = False
    mystical_event_happened: bool = False

    # === ARC-END SESSION REWARDS ===
    artifacts_awarded: list = field(default_factory=list)

    # === ATMOSPHERE (-3 to +5) ===

    @property
    def atmosphere(self) -> int:
        return self._atmosphere

    @atmosphere.setter
    def atmosphere(self, value: int):
        self._atmosphere = max(-3, min(5, value))

    def add_atmosphere(self, amount: int):
        """Modify atmosphere with automatic bounds checking"""
        self.atmosphere += amount

    # === QUALITY (0 to 5) ===

    @property
    def quality(self) -> int:
        return self._quality

    @quality.setter
    def quality(self, value: int):
        self._quality = max(0, min(5, value))

    # === PACING (-2 to +2) ===

    @property
    def pacing(self) -> int:
        return self._pacing

    @pacing.setter
    def pacing(self, value: int):
        self._pacing = max(-2, min(2, value))

    # === ROOM ENERGY (-2 to +5) ===

    @property
    def room_energy(self) -> int:
        return self._room_energy

    @room_energy.setter
    def room_energy(self, value: int):
        self._room_energy = max(-2, min(5, value))

    def add_room_energy(self, amount: int):
        """Modify room energy with automatic bounds checking"""
        self.room_energy += amount

    # === TECH INTERFERENCE (0 to 5) ===

    @property
    def tech_interference(self) -> int:
        return self._tech_interference

    @tech_interference.setter
    def tech_interference(self, value: int):
        self._tech_interference = max(0, min(5, value))

    def add_tech_interference(self, amount: int):
        """Increase tech interference with automatic bounds checking"""
        self.tech_interference += amount

    # === COMPUTED PROPERTIES ===

    @property
    def dominant_focus(self) -> str:
        """Which interpretive lens dominated this session"""
        focuses = {
            "mystical": self.mystical_focus,
            "systemic": self.systemic_focus,
            "relational": self.relational_focus,
            "practical": self.practical_focus,
            "dismissive": self.dismissive_focus,
        }
        return max(focuses.items(), key=lambda x: x[1])[0]

    @property
    def is_high_quality(self) -> bool:
        """Did this session go well?"""
        return self.quality >= 3

    @property
    def is_excellent(self) -> bool:
        """Was this an exceptional session?"""
        return self.quality >= 4

    @property
    def all_cards_drawn(self) -> bool:
        """Has the full spread been revealed?"""
        return all([self.past_card, self.present_card, self.future_card])

    @property
    def cards(self) -> List[str]:
        """All drawn cards in order"""
        return [c for c in [self.past_card, self.present_card, self.future_card] if c]

    @property
    def is_mystical(self) -> bool:
        """Session has strong mystical/spiritual energy"""
        return self.room_energy >= 3 or self.mystical_focus >= 4

    @property
    def is_tense(self) -> bool:
        """Session atmosphere is hostile or uncomfortable"""
        return self.atmosphere < 0


# === FACTORY FUNCTIONS ===


def create_session(client: Client) -> Session:
    """
    Create a fresh session with appropriate initialization.

    Randomizes environmental factors and applies character-specific modifiers.
    """
    session = Session(current_client=client.name)

    # Character-specific environmental modifiers
    if isinstance(client, Nyx):
        session.tech_interference = 1  # Nyx brings tech problems

    return session
