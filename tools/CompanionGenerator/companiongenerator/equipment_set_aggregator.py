from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.equipment_set import EquipmentSet, EquipmentSetName
from companiongenerator.equipment_set_parser import EquipmentSetParser
from companiongenerator.file_handler import FileHandler
from companiongenerator.logger import logger


class EquipmentSetAggregator:
    """
    Aggregates equipment sets in order to
    write them to the file

    NOTE: At the time of creation I didn't realize this
    wasn't necessary because usually there won't be a reason
    to create multiple equipment sets in a single run. Maybe
    this will change later though, so leaving this here.
    """

    def __init__(self):
        self.entries: set[EquipmentSet | EquipmentSetName] = set([])

    def add_entry(self, entry: EquipmentSet | EquipmentSetName):
        self.entries.add(entry)

    def get_eligible_entries(self) -> set[EquipmentSet]:
        return set([entry for entry in self.entries if isinstance(entry, EquipmentSet)])

    def get_content_text(self) -> str | None:
        eligible_entries = self.get_eligible_entries()

        logger.info(f"EquipmentSetAggregator: {len(eligible_entries)} eligible entries")

        if len(eligible_entries) > 0:
            return "\n\n".join(
                [entry.get_tpl_with_replacements() for entry in eligible_entries]
            )

    def load_entries_from_file(self):
        parser = EquipmentSetParser()
        entry_names: set[str] = parser.get_entry_names_from_text()
        for entry in entry_names:
            self.add_entry(EquipmentSetName(entry))

        logger.info(f"EquipmentSetAggregator: Loaded {len(entry_names)} entries")

    def update_equipment_sets(self) -> bool:
        """
        Appends equipment sets to file
        """
        handler = FileHandler()
        content_text = self.get_content_text()
        if content_text is not None and content_text:
            content_text_with_newline = "\n" + content_text
            success = handler.append_to_file(
                MOD_FILENAMES["equipment"], content_text_with_newline
            )
            if success:
                logger.info("Updated equipment sets")
            else:
                logger.error("Error updating equipment sets file")
            return success
        else:
            logger.error("Empty content text for EquipmentSets")
            return False
