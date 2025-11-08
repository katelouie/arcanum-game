"""Artifacts from completed Client sessions."""

# artifacts.py


class Artifact:
    def __init__(
        self,
        id,
        name,
        description,
        lore,
        origin_session,
        origin_character=None,
        rarity="common",
    ):
        self.id = id  # Unique identifier (e.g., "razor_lucky_token")
        self.name = name  # Display name
        self.description = description  # Short description (what it is)
        self.lore = lore  # Longer flavor text (why it matters)
        self.origin_session = origin_session  # Which session it came from
        self.origin_character = (
            origin_character  # Which character gave it (if applicable)
        )
        self.rarity = rarity  # "common", "rare", "legendary" (for UI display)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "lore": self.lore,
            "origin_session": self.origin_session,
            "origin_character": self.origin_character,
            "rarity": self.rarity,
        }


# ============================================================================
# NYX SESSION 3A ARTIFACTS
# ============================================================================

RAZOR_LUCKY_TOKEN = Artifact(
    id="razor_lucky_token",
    name="Razor's Lucky Token",
    description="A small metal token. Ork-made. Engraved with crude runes.",
    lore="Razor carried this through three wars and a dozen shadow runs. He says the cards saved his life, so now his luck is yours. It's warm to the touch, smells like gun oil and old blood. Survivor's charm.",
    origin_session="Nyx: Session 3 (The Heist)",
    origin_character="Razor",
    rarity="rare",
)

SPIRIT_DATA_CORE = Artifact(
    id="spirit_data_core",
    name="Spirit-Touched Data Core",
    description="A data chip that glows faintly—not with electricity, but with something else.",
    lore="One of the freed spirits encoded itself here as gratitude. A fragment of presence. Spirit-touched tech. It's warm. Alive. When you hold it, you can almost hear whispers in frequencies that don't exist. Magic and chrome united.",
    origin_session="Nyx: Session 3 (The Heist)",
    origin_character="Freed Spirit",
    rarity="legendary",
)

LIBERATION_CHIP = Artifact(
    id="liberation_chip",
    name="Liberation Proof Chip",
    description="A black data chip. Encrypted. Glowing softly.",
    lore="Proof that thousands of spirits went free that night. Names, timestamps, liberation protocols. Evidence that you changed the world. Nyx wanted you to remember. You did something that mattered.",
    origin_session="Nyx: Session 3 (The Heist)",
    origin_character="Nyx",
    rarity="rare",
)

BYRON_WING = Artifact(
    id="byron_wing",
    name="Byron's Wing-Circuit",
    description="A tiny drone part. Circuit board shaped like a wing.",
    lore="Byron died in the Kitsune facility. But he died free, helping liberate spirits. Whisper wanted you to have a piece of him. So you'd remember—courage isn't just human. The wing-circuit is delicate, beautiful, and utterly dead. But meaningful.",
    origin_session="Nyx: Session 3 (The Heist)",
    origin_character="Whisper",
    rarity="rare",
)

TSUKUYOMI_EVIDENCE = Artifact(
    id="tsukuyomi_evidence",
    name="Project Tsukuyomi Evidence (Copy)",
    description="A storage chip. Encrypted to hell and back.",
    lore="Copy of the evidence that will destroy Kitsune. Cipher gave it to you as insurance. If anything happens to the crew, YOU have proof. You can expose them. Complete the mission. It's cold. Heavy with responsibility. Power and burden in one small chip.",
    origin_session="Nyx: Session 3 (The Heist)",
    origin_character="Cipher",
    rarity="legendary",
)

# Registry for easy lookup
ARTIFACTS = {
    "razor_lucky_token": RAZOR_LUCKY_TOKEN,
    "spirit_data_core": SPIRIT_DATA_CORE,
    "liberation_chip": LIBERATION_CHIP,
    "byron_wing": BYRON_WING,
    "tsukuyomi_evidence": TSUKUYOMI_EVIDENCE,
}


def get_artifact(artifact_id):
    """Retrieve an artifact by ID"""
    return ARTIFACTS.get(artifact_id)
