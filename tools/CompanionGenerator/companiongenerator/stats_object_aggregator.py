from companiongenerator.stats_object import StatsObject


class StatsObjectAggregator:
    def __init__(self):
        self.entries: set[StatsObject] = set([])

    def add_entry(self, stats_object: StatsObject):
        self.entries.add(stats_object)
