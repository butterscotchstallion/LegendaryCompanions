import os

from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.file_handler import FileHandler
from companiongenerator.logger import logger
from companiongenerator.spell import Spell, SpellName
from companiongenerator.spell_parser import SpellParser


class SpellAggregator:
    """
    Aggregates spells and writes them to file
    """

    entries: set[Spell | SpellName]

    def __init__(self):
        self.entries: set[Spell | SpellName] = set([])
        self.filename = MOD_FILENAMES["spell_text_file_summons"]
        self.parser = SpellParser()
        self.file_handler = FileHandler()
        self.last_num_entries_written: int = 0

    def add_entry(self, entry: Spell | SpellName):
        self.entries.add(entry)

    def load_entries_from_file(self) -> bool:
        """
        Loads spell names from file.

        Returns True if there is at least one spell name in the file
        """
        spell_names: set[str] = self.parser.get_entry_names_from_text()

        if len(spell_names) > 0:
            for spell_name in spell_names:
                spell_name_instance = SpellName()
                spell_name_instance.spell_name = spell_name
                self.add_entry(spell_name_instance)
            return True
        else:
            return False

    def get_eligible_entries(self) -> list[Spell]:
        return [entry for entry in self.entries if isinstance(entry, Spell)]

    def get_spell_entries_text(self) -> str | None:
        """
        Joins spell entries by a new line and returns the resulting
        string.
        """
        if len(self.entries) == 0:
            logger.error("No entries")
        else:
            logger.debug(f"Building content string for {len(self.entries)} entries")
            eligible_spells: list[Spell] = self.get_eligible_entries()
            eligible_spells_len = len(eligible_spells)

            if eligible_spells_len > 0:
                logger.debug(
                    f"Eligible spells ({eligible_spells_len}): {eligible_spells}"
                )
                entry_templates = [
                    entry.get_tpl_with_replacements() for entry in eligible_spells
                ]
                logger.debug(f"Built {len(entry_templates)} template entries")
                self.last_num_entries_written = len(eligible_spells)
                return "\n\n" + "\n\n".join(entry_templates)

    def update_spells(self) -> bool | None:
        """
        Writes spell entries to file

        Returns True if successful in writing at least one entry
        """
        # Open spell file and append new spell if it doesn't exist
        success = False
        try:
            # Open file for reading and writing, creating if not exists
            with open(self.filename, "a+") as handle:
                # New spell: create backup before proceeding
                backup_created = self.file_handler.create_backup_file(self.filename)

                if backup_created:
                    # Seek to end before appending
                    handle.seek(os.SEEK_END)
                    # Append to existing file
                    spells_with_new_line = self.get_spell_entries_text()
                    if spells_with_new_line is not None:
                        success = bool(handle.write(spells_with_new_line))
                        if success:
                            logger.info(
                                f"Appended {self.last_num_entries_written} spells to spell file"
                            )
                            return success
                        else:
                            logger.error("Failed to write to spell file")
        except IOError as err:
            logger.error(f"Error opening summon spell file: {err}")
            return False
