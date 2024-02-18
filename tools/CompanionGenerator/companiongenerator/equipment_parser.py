from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.stats_parser import StatsParser


class EquipmentParser(StatsParser):
    """
    Quite similar to StatsParser but has a
    slightly different "new entry" style
    """

    def __init__(self):
        self.new_entry_text = "new equipment"
        self.filename = MOD_FILENAMES["equipment"]
