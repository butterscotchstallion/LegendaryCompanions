from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.stats_parser import StatsParser


class CharacterParser(StatsParser):
    def __init__(self):
        super().__init__()

        self.filename = MOD_FILENAMES["character"]
