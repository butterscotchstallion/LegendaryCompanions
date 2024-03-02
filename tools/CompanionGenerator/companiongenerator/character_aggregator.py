from companiongenerator.character import Character


class CharacterAggregator:
    entries: set[Character] = set()

    def add_entry(self, entry: Character):
        self.entries.add(entry)

    def load_entries_from_file(self):
        pass

    def update_character_file(self):
        pass
