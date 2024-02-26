from companiongenerator.spell import Spell, SpellName
from companiongenerator.spell_parser import SpellParser


class SpellAggregator:
    """
    Aggregates spells and writes them to file
    """

    entries: set[Spell | SpellName] = set([])

    def __init__(self):
        pass

    def add_entry(self, entry: Spell | SpellName):
        self.entries.add(entry)

    def load_entries_from_file(self) -> bool:
        """
        Loads spell names from file.

        Returns True if there is at least one spell name in the file
        """
        parser = SpellParser()
        spell_names: set[str] = parser.get_entry_names_from_text()

        if len(spell_names) > 0:
            for spell_name in spell_names:
                spell_name_instance = SpellName()
                spell_name_instance.spell_name = spell_name
                self.add_entry(spell_name_instance)
            return True
        else:
            return False
