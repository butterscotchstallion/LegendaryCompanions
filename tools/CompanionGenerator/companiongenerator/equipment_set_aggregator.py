from companiongenerator.equipment_set import EquipmentSet


class EquipmentSetAggregator:
    """
    Aggregates equipment sets in order to
    write them to the file
    """

    def __init__(self):
        self.entries: set[EquipmentSet] = set([])

    def add_entry(self, entry: EquipmentSet):
        self.entries.add(entry)
