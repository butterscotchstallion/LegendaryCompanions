import os

from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.file_handler import FileHandler
from companiongenerator.item_combo import ItemCombo, ItemComboName
from companiongenerator.item_combo_parser import ItemComboParser
from companiongenerator.logger import logger


class ItemComboAggregator:
    """
    Aggregates item combos in order to
    encapsulate collection and writing
    of item combos to file
    """

    def __init__(self):
        self.entries: set[ItemCombo | ItemComboName] = set([])

    def load_combo_entries_from_file(self):
        """
        Reads existing combo file and loads entries
        """
        parser = ItemComboParser()
        combo_names = parser.get_combo_names_from_file_contents()
        for combo_name in combo_names:
            self.entries.add(ItemComboName(combo_name))

    def add_entry(self, entry: ItemCombo | ItemComboName):
        self.entries.add(entry)

    def get_entries_content_string(self) -> str:
        """
        Builds a single newline delimited string
        from entries

        The entries set contains some instances which are just the
        name from existing combos, and then we filter those out
        for writing to file
        """
        combo_names = (entry.combo_name for entry in self.entries)
        combos = (entry for entry in self.entries if isinstance(entry, ItemCombo))
        entry_templates = (
            entry.get_tpl_with_replacements()
            for entry in combos
            if entry.combo_name not in combo_names
        )
        return "\n".join(entry_templates)

    def update_item_combos(self, **kwargs):
        """
        Updates item combos file with entries. Returns True if file update
        succeeds or the combo exists already
        """
        with open(MOD_FILENAMES["item_combos"], "a+") as handle:
            # Create backup before writing
            handler = FileHandler()
            created_backup = handler.create_backup_file(MOD_FILENAMES["item_combos"])
            if created_backup:
                handle.seek(os.SEEK_END)
                entries_text: str = self.get_entries_content_string()
                success = handle.write(entries_text)

                if success:
                    logger.info("Wrote combos to file")

                return success
            else:
                logger.error(
                    f"Failed to create backup of {MOD_FILENAMES["item_combos"]}"
                )
                return False
