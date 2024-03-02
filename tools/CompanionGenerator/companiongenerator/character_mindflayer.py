from typing import Unpack

from companiongenerator.character import Character, CharacterKeywords


class CharacterMindflayer(Character):
    def __init__(self, **kwargs: Unpack[CharacterKeywords]):
        super().__init__(**kwargs)
        self.template_filename = "character_mindflayer.txt"
