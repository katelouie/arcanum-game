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
        physical_properties="",
        spiritual_resonance="",
        cultural_context="",
        reader_effect="",
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
        self.physical_properties = physical_properties
        self.spiritual_resonance = spiritual_resonance
        self.cultural_context = cultural_context
        self.reader_effect = reader_effect

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

# ============================================================================
# NYX SESSION 3B ARTIFACTS (Ghost Protocol / Espionage Path)
# ============================================================================

SPIRIT_GUIDANCE_CHARM = Artifact(
    id="spirit_guidance_charm",
    name="Spirit Guidance Charm",
    description="A small carved wooden charm. Warm to the touch. Unfamiliar style.",
    lore="The freed spirits left this on Nyx's shrine after the heist. Gratitude made manifest. Protection for the one who freed them. When you hold it, you feel presence—watching, guiding, protecting. Hidden magic surviving in a corporate world. The spirits remember. They're watching. You're never truly alone.",
    origin_session="nyx_session_3b",
    origin_character="Freed Spirits",
    rarity="rare",
)

CORPORATE_WARNING_TOKEN = Artifact(
    id="corporate_warning_token",
    name="Corporate Warning Token",
    description="Small metal disc. Kitsune logo on one side. Matsuda's personal seal on the other.",
    lore="Matsuda left this somehow. During the investigation. Before the call. A message without words: 'I'm watching you.' Not quite proof. Not quite threat. But weight. Pressure. The edge Nyx walks every day after Ghost Protocol. She kept her cover but Matsuda's suspicion lingers, cold and heavy as this token. Corporate surveillance made physical.",
    origin_session="nyx_session_3b",
    origin_character="Matsuda Kenji",
    rarity="uncommon",
)

INSIDER_KEYCARD = Artifact(
    id="insider_keycard",
    name="The Insider's Keycard",
    description="Nyx's Kitsune employee badge. Gamma-7 clearance. But it means more now.",
    lore="No longer just corporate ID. It's access. Power. The ability to change things from within. Nicole Dimayuga—shadow operative. The deepest of deep cover. She stayed inside Kitsune not from fear but from strategy. Long game thinking. This badge is proof: infiltration can be liberation. Sometimes the most radical act is staying where you're planted and rotting the system from inside.",
    origin_session="nyx_session_3b",
    origin_character="Nyx (herself)",
    rarity="rare",
)

WANDERERS_COMPASS = Artifact(
    id="wanderers_compass",
    name="Wanderer's Compass",
    description="Small brass compass. Old. Tarnished. The needle doesn't point north.",
    lore="It appeared in Nyx's pocket on the bus leaving Seattle. She didn't pack it. The spirits left it. The needle points toward meaning. Toward purpose. Toward the path needed—not the path expected. For the ghost who chose neither crew nor corpo. For the wanderer building new identity in new city. Guidance for those brave enough to walk alone. The compass never lies but it rarely points where you think you're going.",
    origin_session="nyx_session_3b",
    origin_character="Unknown (Spirit Gift)",
    rarity="legendary",
)

ANCESTRAL_TRAVEL_BLESSING = Artifact(
    id="ancestral_travel_blessing",
    name="Ancestral Travel Blessing",
    description="Lola's photograph. But something changed. It's warmer now. More present.",
    lore="When Nyx left Seattle—alone, ghost protocol, complete severance—she took her grandmother's photo. And Lola came with her. Not just memory. Presence. Blessing. Protection. 'Wherever you go, we go. You're never truly alone. Walk safely, child.' The anito traveling with her. Guardian spirits for a wandering soul. No matter how far she runs, no matter what name she takes, her ancestors walk beside her. That's the blessing: solitude, yes. But never abandonment.",
    origin_session="nyx_session_3b",
    origin_character="Lola (Grandmother's Spirit)",
    rarity="legendary",
)

ENCRYPTED_SKILLS_DATACORE = Artifact(
    id="encrypted_skills_datacore",
    name="Encrypted Skills Datacore",
    description="Dense datacore. Black. Heavily encrypted. Contains compressed knowledge.",
    lore="Before disappearing, Nyx encoded everything. Her knowledge. Her skills. Kitsune systems architecture. Hacking techniques. Shamanic insights. Street wisdom. All compressed into this core. Her value made portable. She can rebuild anywhere. Offer her skills. Start fresh. But never start from zero. The ghost carries her power with her. No corpo owns it. No crew demands it. It's hers. Fully. Finally.",
    origin_session="nyx_session_3b",
    origin_character="Nyx (herself)",
    rarity="rare",
)

# ============================================================================
# NYX PATH C ARTIFACTS - Session 3C: The Reckoning
# ============================================================================

SPIRIT_FUSED_CYBEREYES = Artifact(
    id="spirit_fused_cybereyes",
    name="Spirit-Fused Cybereyes",
    description="Chrome and circuitry. Glowing soft white-gold. Warm to touch. Baybayin script etched impossibly into metal. Hum subsonic. Spirit-marks permanent.",
    lore="During apotheosis, the spirits didn't destroy her augments. They transformed them. Chrome became sacred. Technology became altar. The glitching stopped not through removal but through integration. These eyes saw thousands of spirits flooding IN. Saw Lola manifest fully. Saw the moment Nyx became vessel. They remember. The neural interfaces still hold traces of divine presence. When you hold them, you feel it. Not hostile. Just present. Undeniable. Occasionally faces appear in the chrome's reflection. Not yours. Spirit faces. Watching. Blessing. Acknowledging the witness. This is proof that flesh and chrome and magic can dance together. That the war between worlds can end. That techno-shamanism isn't dream—it's destiny. Nyx became it. These eyes prove it.",
    origin_session="Nyx Session 3C (The Reckoning)",
    origin_character="Nyx (transformed)",
    rarity="legendary",
    physical_properties="Warm. Subsonic hum. Glows white-gold. Never corrodes.",
    spiritual_resonance="High. Attracts spirits. Responds to awakened presence.",
    cultural_context="Filipino baybayin script. Ancestral blessing made tangible.",
    reader_effect="Mystical affinity +2. Occasional spirit whispers in Tagalog.",
)

VESSELS_MARK = Artifact(
    id="vessels_mark",
    name="Vessel's Mark",
    description="Paper rubbing. Baybayin script glowing faintly. Ancestral blessings captured in ink that remembers being light. Sacred. Fragile. Heavy.",
    lore="When the ancestors inhabited Nyx, they wrote on her body. Not metaphor. Actual script. Light-made-letters flowing across her arms, neck, face. Filipino baybayin—ancient, sacred, powerful. The translations are clear: 'Daughter of spirits.' 'Vessel of the forgotten.' 'Bridge between worlds.' 'She who breaks chains.' This rubbing captured those marks before they faded from her skin. But they didn't fully fade. The paper remembers. The ink glows. Soft gold-white, persistent, gentle. You don't want to fold it. Don't want to damage it. It demands care. Reverence. The ancestors signed their names on her flesh and this paper bears witness. When you trace the characters, you feel SEEN. Not by Nyx. By them. By the vast, ancient, judging-and-blessing presence that chose her. That claimed her. That made her MORE. This is legacy. This is proof. This is the moment divinity touched humanity and said: 'You. Yes. YOU.'",
    origin_session="Nyx Session 3C (The Reckoning)",
    origin_character="The Ancestors (through Nyx)",
    rarity="legendary",
    physical_properties="Glows softly in darkness. Paper feels warm. Ink never fades.",
    spiritual_resonance="Ancestral. Spirits recognize and honor it.",
    cultural_context="Filipino shamanic tradition. Baybayin script. Lola's bloodline.",
    reader_effect="Mystical affinity +1. Feel witnessed by something vast.",
)

REMOVED_CYBEREYES_INERT = Artifact(
    id="removed_cybereyes_inert",
    name="Removed Cybereyes (Inert)",
    description="Chrome and circuitry. Cold. Dead. Silent. Scorch marks visible on neural interfaces. No glow. No life. Just weight.",
    lore="She chose safety. She chose herself. She chose to walk away from magic and build something human instead. These eyes—once glitching with spirit pressure, once potential vessels for divine sight—were surgically removed three weeks after the reckoning. Replaced with standard optical implants. Mundane. Safe. Normal. The chrome is scarred. Scorch marks where spirits tried to break through. Evidence of the war her body fought. But now? Silent. The spirits gave up. Let her go. Sad but accepting. She wasn't strong enough. Wasn't ready. That's allowed. That's human. These eyes remember what they could have become. Chrome-and-magic unified. Spirit-sight permanent. Techno-shamanic transcendence. But she said no. And they died. Not destroyed—abandoned. When you hold them, you feel grief. Not yours. Absorbed. Residual. The grief of doors closing. Of potential unrealized. Of 'what if.' They're heavier than they should be. Not physically. Emotionally. The weight of retreat. Of choosing survival over purpose. She built a good life after. Meaningful. Ethical. Kind. But these eyes will never see spirits again. And they mourn.",
    origin_session="Nyx Session 3C (The Reckoning)",
    origin_character="Nyx (withdrawn)",
    rarity="uncommon",
    physical_properties="Cold. Heavy. Inert. Scorch marks permanent.",
    spiritual_resonance="Absent. Spirits avoid—too painful.",
    reader_effect="Empathy +2. Feel her choice's cost.",
)

NEW_LIFE_JOURNAL = Artifact(
    id="new_life_journal",
    name="New Life Journal",
    description="Single journal page. Three months after. Neat handwriting. Describes nonprofit work, therapy, garden volunteering. Small confession at bottom.",
    lore="Portland. Or maybe Vancouver. Somewhere rainy. Somewhere quiet. Somewhere she could disappear and rebuild as someone ordinary. Three months after choosing ash, she writes in her journal. Daily practice. Therapist recommended it. Helps with 'processing trauma from previous employment.' She describes her new life carefully. Gratefully. Nonprofit environmental justice work. Therapy twice monthly. Community garden on weekends. Coffee dates with someone kind who doesn't ask about her past. She's healing. She's growing. She's building something small but good. The entry is positive. Deliberately positive. Convince herself. Convince the universe. Convince anyone who might read this that she made the right choice. That survival is enough. That ordinary is okay. But at the bottom—smaller text, almost hidden, written late at night when the mask slips—the truth: 'I still dream about them sometimes. The spirits. The light. What I could have been. I wake up crying and tell myself it's okay. That I made the right choice. That survival is enough. Most days I believe it.' Most days. Not all. The ink is ordinary but the words are heavy. When you read them, you feel her trying. Trying so hard. To be okay. To accept. To move on. And you wonder: did she succeed? Is the life she built enough to fill the space where magic used to be? You don't know. Neither does she. But she keeps trying. That's something. Maybe that's everything.",
    origin_session="Nyx Session 3C (The Reckoning)",
    origin_character="Nyx (three months after)",
    rarity="uncommon",
    physical_properties="Ordinary paper. Neat handwriting. Bottom text smaller, shakier.",
    spiritual_resonance="Absent. Painful absence. Spirits can't bear it.",
    reader_effect="Empathy +2. Understand the cost of choosing safety.",
)


# Registry for easy lookup
ARTIFACTS = {
    "razor_lucky_token": RAZOR_LUCKY_TOKEN,
    "spirit_data_core": SPIRIT_DATA_CORE,
    "liberation_chip": LIBERATION_CHIP,
    "byron_wing": BYRON_WING,
    "tsukuyomi_evidence": TSUKUYOMI_EVIDENCE,
    "spirit_guidance_charm": SPIRIT_GUIDANCE_CHARM,
    "corporate_warning_token": CORPORATE_WARNING_TOKEN,
    "insider_keycard": INSIDER_KEYCARD,
    "wanderers_compass": WANDERERS_COMPASS,
    "ancestral_travel_blessing": ANCESTRAL_TRAVEL_BLESSING,
    "encrypted_skills_datacore": ENCRYPTED_SKILLS_DATACORE,
    # Nyx Session 3C - Path C (Catharsis)
    "spirit_fused_cybereyes": SPIRIT_FUSED_CYBEREYES,
    "vessels_mark": VESSELS_MARK,
    # Nyx Session 3C - Path C (Sad)
    "removed_cybereyes_inert": REMOVED_CYBEREYES_INERT,
    "new_life_journal": NEW_LIFE_JOURNAL,
}


def get_artifact(artifact_id):
    """Retrieve an artifact by ID"""
    return ARTIFACTS.get(artifact_id)
