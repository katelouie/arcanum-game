"""Classes for characters and player."""

import random
from dataclasses import dataclass, field
from typing import List, Literal, Set

from game_logic.tarot import Card

ReadingStyle = Literal["intuitive", "analytical", "storyteller", "practical"]
Background = Literal["inheritance", "self_taught", "unexpected_gift", "career_change"]


@dataclass
class Reader:
    """The player character -- the tarot read protagonist.

    Persistent across all sessions and represents the player's progression, skills, reputation,
    and ethical choices."""

    # Core stats (private, accessed via properties)
    # Identity and creation
    name = "Reader"
    style: ReadingStyle = "intuitive"
    background: Background = "self_taught"

    # Progression (unbounded)
    experience: int = 0  # Total XP, unlocks milestones
    money: int = 0  # Currency, goal: open a shop for 5k
    sessions_completed: int = 0  # Total readings given

    # Skills (how you read, 0-10)
    _empathy: int = 0  # 0-10: Emotional intelligence
    _insight: int = 0  # 0-10: Pattern recognition, perceptiveness
    _competence: int = 0  # 0-10: Overall reading quality
    _mystical_affinity: int = 0  # 0-10: Spiritual/occult attunement

    # Reputation and ethics
    _reputation: int = 0  # -10 to 10: public standing, social valence
    _manipulation: int = 0  # 0 to 5: exploitative behavior
    _corruption: int = 0  # 0 to 5: ethical compromise

    # Progression flags
    has_shop: bool = False  # Rented permanent reading space
    advanced_spreads_unlocked: bool = False

    # Achievements collection
    achievements = set()

    # Client completion artifacts
    artifacts: list[str] = field(default_factory=list)

    ### Bounded Properties ###
    # === EMPATHY (0-10) ===
    @property
    def empathy(self) -> int:
        return self._empathy

    @empathy.setter
    def empathy(self, value: int):
        self._empathy = max(0, min(10, value))

    def add_empathy(self, amount: int):
        self.empathy += amount

    # === INSIGHT (0-10) ===
    @property
    def insight(self) -> int:
        return self._insight

    @insight.setter
    def insight(self, value: int):
        self._insight = max(0, min(10, value))

    def add_insight(self, amount: int):
        self.insight += amount

    # === MYSTICAL AFFINITY (0-10) ===
    @property
    def mystical_affinity(self) -> int:
        return self._mystical_affinity

    @mystical_affinity.setter
    def mystical_affinity(self, value: int):
        self._mystical_affinity = max(0, min(10, value))

    def add_mystical_affinity(self, amount: int):
        """Add mystical affinity with automatic bounds checking"""
        self.mystical_affinity += amount

    # === COMPETENCE (0-10) ===
    @property
    def competence(self) -> int:
        return self._competence

    @competence.setter
    def competence(self, value: int):
        self._competence = max(0, min(10, value))

    def add_competence(self, amount: int):
        """Add competence with automatic bounds checking"""
        self.competence += amount

    # === REPUTATION (-10 to +10) ===
    @property
    def reputation(self) -> int:
        return self._reputation

    @reputation.setter
    def reputation(self, value: int):
        self._reputation = max(-10, min(10, value))

    def add_reputation(self, amount: int):
        """Add reputation with automatic bounds checking"""
        self.reputation += amount

    # === MANIPULATION (0 to +5) ===
    @property
    def manipulation(self) -> int:
        return self._manipulation

    @manipulation.setter
    def manipulation(self, value: int):
        self._manipulation = max(0, min(5, value))

    def add_manipulation(self, amount: int):
        """Add manipulation with automatic bounds checking"""
        self.manipulation += amount

    # === CORRUPTION (0 to 5) ===
    @property
    def corruption(self) -> int:
        return self._corruption

    @corruption.setter
    def corruption(self, value: int):
        self._corruption = max(0, min(5, value))

    def add_corruption(self, amount: int):
        """Add corruption with automatic bounds checking (can only increase)"""
        self.corruption += amount

    # === PROGRESSION METHODS ===
    def add_experience(self, amount: int):
        """Grant XP and check for milestone unlocks"""
        old_xp = self.experience
        self.experience += amount

        # Check milestone thresholds
        if old_xp < 100 <= self.experience and not self.advanced_spreads_unlocked:
            self.advanced_spreads_unlocked = True
            # Could trigger event here

    def add_money(self, amount: int):
        """Earn money from readings"""
        self.money = max(0, self.money + amount)

    def rent_shop(self) -> bool:
        """Spend 5000 to get permanent reading space"""
        if self.money >= 5000 and not self.has_shop:
            self.money -= 5000
            self.has_shop = True
            return True
        return False

    def get_level(self) -> str:
        if self.experience < 100:
            return "Novice"
        elif self.experience < 500:
            return "Apprentice"
        elif self.experience < 1000:
            return "Adept"
        else:
            return "Master"

    # === COMPUTED PROPERTIES ===
    @property
    def can_afford_shop(self) -> bool:
        """Has enough money to rent shop"""
        return self.money >= 5000

    @property
    def dominant_skill(self) -> str:
        """Which skill is highest"""
        skills = {
            "empathy": self.empathy,
            "insight": self.insight,
            "mystical": self.mystical_affinity,
        }
        return max(skills.items(), key=lambda x: x[1])[0]

    @property
    def is_competent(self) -> bool:
        """Can attempt advanced techniques"""
        return self.competence >= 5

    @property
    def is_master(self) -> bool:
        """Mastery level skill"""
        return self.competence >= 8

    @property
    def is_struggling(self) -> bool:
        """Low competence, giving poor readings"""
        return self.competence < 3

    @property
    def is_perceptive(self) -> bool:
        """Notices subtle details"""
        return self.insight >= 6

    @property
    def is_spiritually_attuned(self) -> bool:
        """Can perceive mystical phenomena"""
        return self.mystical_affinity >= 6

    @property
    def reading_archetype(self) -> str:
        """Combines reading style with dominant skill"""
        return f"{self.style}_{self.dominant_skill}"

    @property
    def reputation_tier(self) -> str:
        """Qualitative reputation description"""
        if self.reputation >= 7:
            return "renowned"
        elif self.reputation >= 4:
            return "respected"
        elif self.reputation >= 1:
            return "known"
        elif self.reputation >= -2:
            return "unknown"
        elif self.reputation >= -5:
            return "questionable"
        else:
            return "notorious"

    @property
    def is_ethical(self) -> bool:
        """Has maintained ethical practice"""
        return self.manipulation <= 0 and self.corruption <= 1

    @property
    def is_corrupted(self) -> bool:
        """Has compromised ethics significantly"""
        return self.corruption >= 3 or self.manipulation >= 3

    @property
    def is_exploitative(self) -> bool:
        """Uses readings to manipulate clients"""
        return self.manipulation >= 3

    # === COLLECTIONS: ACHIEVEMENTS AND ARTIFACTS ===
    def add_artifact(self, artifact_name: str):
        """Add artifact ID to collection."""
        self.artifacts.append(artifact_name)

    def add_achievement(self, achievement: str):
        """Add achievement to set."""
        self.achievements.add(achievement)


@dataclass
class Client:
    """
    Base class for all clients.

    Represents relationship progression, topics discussed, and shared attributes
    across all client types.
    """

    # === IDENTITY ===
    name: str
    age: int
    total_sessions: int
    sessions_completed: int = 0

    # === RELATIONSHIP STATS (0-100) ===
    _trust: int = 50  # 0-100: Will they open up?
    _comfort: int = 50  # 0-100: Do they feel safe?

    # === EMOTIONAL STATE (-10 to +10) ===
    _openness: int = 0  # -10 to +10: Defensive vs vulnerable

    # === STORY TRACKING ===
    topics_discussed: Set[str] = field(default_factory=set)
    cards_seen: List[str] = field(default_factory=list)

    # === DISPLAY ===
    flavor_text: str = "Client Flavor Text"

    # === TRUST (0-100) ===

    @property
    def trust(self) -> int:
        return self._trust

    @trust.setter
    def trust(self, value: int):
        self._trust = max(0, min(100, value))

    def add_trust(self, amount: int):
        """Add trust with automatic threshold checks"""
        old_trust = self.trust
        self.trust += amount

        # Trigger threshold events
        if old_trust < 60 <= self.trust:
            self.on_trust_threshold_60()
        if old_trust < 80 <= self.trust:
            self.on_trust_threshold_80()

    def on_trust_threshold_60(self):
        """Override in subclasses for threshold events"""
        pass

    def on_trust_threshold_80(self):
        """Override in subclasses for threshold events"""
        pass

    # === COMFORT (0-100) ===

    @property
    def comfort(self) -> int:
        return self._comfort

    @comfort.setter
    def comfort(self, value: int):
        self._comfort = max(0, min(100, value))

    def add_comfort(self, amount: int):
        """Add comfort with automatic bounds checking"""
        self.comfort += amount

    # === OPENNESS (-10 to +10) ===

    @property
    def openness(self) -> int:
        return self._openness

    @openness.setter
    def openness(self, value: int):
        self._openness = max(-10, min(10, value))

    def add_openness(self, amount: int):
        """Add openness with automatic bounds checking"""
        self.openness += amount

    # === STORY TRACKING METHODS ===

    def discuss_topic(self, topic: str):
        """Mark a topic as discussed"""
        self.topics_discussed.add(topic)

    def has_discussed(self, topic: str) -> bool:
        """Check if topic was covered"""
        return topic in self.topics_discussed

    def see_card(self, card_id: str):
        """Track that client has seen this card"""
        if card_id not in self.cards_seen:
            self.cards_seen.append(card_id)

    # === COMPUTED PROPERTIES ===

    @property
    def is_ready_for_deep_work(self) -> bool:
        """Has sufficient trust/openness for vulnerable topics"""
        return self.trust >= 60 and self.openness >= 1

    @property
    def relationship_quality(self) -> str:
        """Qualitative assessment of relationship"""
        if self.trust >= 80:
            return "close_confidant"
        elif self.trust >= 60:
            return "trusted_guide"
        elif self.trust >= 40:
            return "professional"
        elif self.trust >= 20:
            return "cautious"
        else:
            return "guarded"

    @property
    def is_defensive(self) -> bool:
        """Client is guarded and closed off"""
        return self.openness <= -3

    @property
    def is_vulnerable(self) -> bool:
        """Client is open and sharing deeply"""
        return self.openness >= 5

    def start_session(self) -> None:
        self.sessions_completed += 1


@dataclass
class Nyx(Client):
    """
    Nyx - Cyberpunk corporate shaman (special client).

    A data architect at Kitsune Dynamics who is experiencing "technical difficulties"
    that are actually her suppressed shamanic abilities reasserting themselves.
    """

    # === DEFAULT STARTING VALUES ===
    _trust = 40  # Starts slightly cautious
    _comfort = 45
    _openness = -2  # Starts slightly guarded

    # === NYX-SPECIFIC PROGRESSION (0-5) ===
    _shamanic_awakening: int = 0  # 0-5: Reclaiming ancestral wisdom
    _kitsune_suspicion: int = 0  # 0-5: Corporate awareness/danger
    _cyber_glitches: int = 1  # 0-5: Tech malfunction symptoms

    # === SHAMANIC AWAKENING (0-5) ===

    @property
    def shamanic_awakening(self) -> int:
        return self._shamanic_awakening

    @shamanic_awakening.setter
    def shamanic_awakening(self, value: int):
        self._shamanic_awakening = max(0, min(5, value))

    def add_shamanic_awakening(self, amount: int):
        """Add shamanic awakening with threshold checks"""
        old_value = self.shamanic_awakening
        self.shamanic_awakening += amount

        # Threshold event: spiritual breakthrough
        if old_value < 3 <= self.shamanic_awakening:
            self.discuss_topic("spiritual_breakthrough")

        # Full integration
        if old_value < 5 <= self.shamanic_awakening:
            self.discuss_topic("shamanic_integration")

    # === KITSUNE SUSPICION (0-5) ===

    @property
    def kitsune_suspicion(self) -> int:
        return self._kitsune_suspicion

    @kitsune_suspicion.setter
    def kitsune_suspicion(self, value: int):
        self._kitsune_suspicion = max(0, min(5, value))

    def add_kitsune_suspicion(self, amount: int):
        """Add corporate suspicion with danger thresholds"""
        old_value = self.kitsune_suspicion
        self.kitsune_suspicion += amount

        # Danger threshold
        if old_value < 4 <= self.kitsune_suspicion:
            self.discuss_topic("corporate_danger")

        # Critical - cover blown
        if old_value < 5 <= self.kitsune_suspicion:
            self.discuss_topic("cover_blown")

    # === CYBER GLITCHES (0-5) ===

    @property
    def cyber_glitches(self) -> int:
        return self._cyber_glitches

    @cyber_glitches.setter
    def cyber_glitches(self, value: int):
        self._cyber_glitches = max(0, min(5, value))

    def add_cyber_glitches(self, amount: int):
        """Add cyber glitches with automatic bounds checking"""
        self.cyber_glitches += amount

    # === COMPUTED FLAGS (derived from topics_discussed) ===

    @property
    def heritage_revealed(self) -> bool:
        """Has shamanic background been discussed"""
        return self.has_discussed("heritage")

    @property
    def grandmother_discussed(self) -> bool:
        """Has grandmother's story been shared"""
        return self.has_discussed("grandmother")

    @property
    def project_tsukuyomi_mentioned(self) -> bool:
        """Has the dark corporate project been revealed"""
        return self.has_discussed("project_tsukuyomi")

    @property
    def digital_spirits_acknowledged(self) -> bool:
        """Has she admitted the spirits are real"""
        return self.has_discussed("digital_spirits")

    @property
    def is_ally(self) -> bool:
        """Trusts reader completely and committed to liberation"""
        return (
            self.trust >= 80
            and self.shamanic_awakening >= 3
            and self.has_discussed("liberation_path")
        )

    @property
    def suspects_reader(self) -> bool:
        """Thinks reader might work for Kitsune"""
        return self.has_discussed("reader_suspicion")

    # === COMPUTED PROPERTIES ===

    @property
    def glitches_are_spiritual(self) -> bool:
        """Tech problems are actually spiritual awakening"""
        return self.cyber_glitches >= 2 and self.shamanic_awakening >= 1

    @property
    def awakening_stage(self) -> str:
        """Current stage of shamanic reclamation"""
        if self.shamanic_awakening >= 5:
            return "integrated"
        elif self.shamanic_awakening >= 4:
            return "awakening"
        elif self.shamanic_awakening >= 2:
            return "stirring"
        elif self.shamanic_awakening >= 1:
            return "nascent"
        else:
            return "suppressed"

    @property
    def danger_level(self) -> str:
        """How much danger is she in from Kitsune"""
        if self.kitsune_suspicion >= 5:
            return "critical"
        elif self.kitsune_suspicion >= 4:
            return "high"
        elif self.kitsune_suspicion >= 2:
            return "elevated"
        else:
            return "minimal"


@dataclass
class Chen(Client):
    """
    Margaret Chen - Retired librarian, HK diaspora, gentle first client.

    NEW ATTRIBUTES (justification):
    - trust: Tracks how much she trusts you (affects payment, return)
    - comfort: How comfortable she feels opening up (affects depth)
    - clarity: How much clarity she's gained (reading success metric)
    - discussed_grief: Flag for if you named David's death
    - discussed_culture: Flag for if you acknowledged cultural pressure
    - discussed_guilt: Flag for if you recognized her guilt
    - will_return: Whether she books Session 2
    """

    _trust: int = 5  # Starts neutral-positive (5/10)
    _comfort: int = 4  # Starts slightly guarded (4/10)
    _clarity: int = 0  # Starts confused (0/10)

    # Conversation flags
    discussed_grief: bool = False
    discussed_culture: bool = False
    discussed_guilt: bool = False
    discussed_practical: bool = False
    discussed_fear: bool = False
    discussed_house: bool = False
    discussed_daughter: bool = False
    mentioned_david_name: bool = False

    # Session outcome
    will_return: bool = False
    gave_gift: bool = False

    # Session tracking
    session_one_quality: str = ""
    session_one_cards: list[Card] = field(default_factory=list)
    session_two_quality: str = ""
    session_two_cards: list[Card] = field(default_factory=list)
    session_three_quality: str = ""
    session_three_cards: list[Card] = field(default_factory=list)

    @property
    def clarity(self) -> int:
        return self._clarity

    @clarity.setter
    def clarity(self, value: int):
        self._clarity = max(0, min(10, value))

    def add_clarity(self, amount: int):
        self.clarity += amount

    def determine_session_three_path(self):
        crisis_weight = 50
        acceptance_weight = 50

        # Session 1 flags
        if self.discussed_grief:
            crisis_weight += 15
        if self.discussed_culture:
            acceptance_weight += 15
        if self.discussed_guilt:
            crisis_weight += 10
        if self.discussed_practical:
            acceptance_weight += 10

        # Session 2 flags
        if self.discussed_fear:
            acceptance_weight += 15
        if self.discussed_house:
            acceptance_weight += 10
        if self.discussed_daughter:
            crisis_weight += 20
        if self.mentioned_david_name:
            crisis_weight += 5

        # Quality modifier
        if self.session_two_quality == "profound":
            acceptance_weight += 15
        elif self.session_two_quality == "adequate":
            crisis_weight += 15

        # Roll
        total_weight = crisis_weight + acceptance_weight
        roll = random.randint(1, total_weight)

        if roll <= crisis_weight:
            self.session_three_path = "final_push"
        else:
            self.session_three_path = "acceptance"

        return self.session_three_path
