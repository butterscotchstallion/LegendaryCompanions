from companiongenerator.equipment_set import EquipmentSet


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
