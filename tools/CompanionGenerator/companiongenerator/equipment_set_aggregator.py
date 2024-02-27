from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.equipment_set import EquipmentSet
from companiongenerator.file_handler import FileHandler


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
        self.entries: set[EquipmentSet] = set([])

    def add_entry(self, entry: EquipmentSet):
        self.entries.add(entry)

    def get_content_text(self) -> str:
        return "\n\n".join(
            [entry.get_tpl_with_replacements() for entry in self.entries]
        )

    def update_equipment_sets(self) -> bool:
        """
        Appends equipment sets to file
        """
        handler = FileHandler()
        return handler.append_to_file(
            MOD_FILENAMES["equipment"], self.get_content_text()
        )
