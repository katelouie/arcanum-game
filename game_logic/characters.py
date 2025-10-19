"""Classes for characters and player."""


class Client:
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age
        self.trust_level = 50
        self.cards_seen = []
        self.session_count = 0
        self.flavor_text: str = "Client Flavor Text"

    def add_card_seen(self, card) -> None:
        self.cards_seen.append(card.name)

    def modify_trust(self, amount) -> None:
        self.trust_level = max(0, min(100, self.trust_level + amount))

    def get_trust_description(self) -> str:
        if self.trust_level > 75:
            return "deeply trusts you"
        elif self.trust_level > 50:
            return "trusts you"
        elif self.trust_level > 25:
            return "is uncertain"
        else:
            return "is skeptical"

    def start_session(self) -> None:
        self.session_count += 1


class Reader:
    def __init__(self, name) -> None:
        self.name = name
        self.experience = 0
        self.style = "traditional"
        self.specialties = []

    def add_experience(self, points) -> None:
        self.experience += points

    def get_level(self) -> str:
        if self.experience < 100:
            return "Novice"
        elif self.experience < 500:
            return "Apprentice"
        elif self.experience < 1000:
            return "Adept"
        else:
            return "Master"
