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
        self.parser = ItemComboParser()
        self.entries: set[ItemCombo | ItemComboName] = set([])

    def load_entries_from_file(self) -> set[ItemCombo | ItemComboName]:
        """
        Reads existing combo file and loads entries
        """
        combo_names = self.parser.get_combo_names_from_file_contents()
        for combo_name in combo_names:
            self.entries.add(ItemComboName(combo_name))
        return self.entries

    def add_entry(self, entry: ItemCombo | ItemComboName):
        self.entries.add(entry)

    def get_entries_content_string(self) -> str | None:
        """
        Builds a single newline delimited string
        from entries

        The entries set contains some instances which are just the
        name from existing combos, and then we filter those out
        for writing to file
        """
        if len(self.entries) == 0:
            logger.error("No entries")
        else:
            logger.debug(f"Building content string for {len(self.entries)} entries")
            combos = [entry for entry in self.entries if isinstance(entry, ItemCombo)]

            if len(combos) > 0:
                entry_templates = [
                    entry.get_tpl_with_replacements() for entry in combos
                ]
                logger.debug(f"Built {len(entry_templates)} template entries")
                return "\n".join(entry_templates)

    def update_item_combos(self) -> bool:
        """
        Updates item combos file with entries. Returns True if file update
        succeeds or the combo exists already
        """
        success = False
        with open(MOD_FILENAMES["item_combos"], "a+") as handle:
            # Create backup before writing
            handler = FileHandler()
            created_backup = handler.create_backup_file(MOD_FILENAMES["item_combos"])
            if created_backup:
                handle.seek(os.SEEK_END)
                entries_text: str | None = self.get_entries_content_string()

                if entries_text is not None and len(entries_text) > 0:
                    file_write_success = handle.write(entries_text)
                    success = bool(file_write_success)
                else:
                    logger.error("Empty content entries text")
            else:
                logger.error(
                    f"Failed to create backup of {MOD_FILENAMES["item_combos"]}"
                )
        if success:
            logger.info(f"Wrote {len(self.entries)} combo entries to file")
        else:
            logger.error("Error writing item combo entries to file")

        return success
