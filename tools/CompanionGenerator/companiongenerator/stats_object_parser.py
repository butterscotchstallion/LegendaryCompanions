from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.stats_parser import ParserType, StatsParser


class StatsObjectParser(StatsParser):
    def __init__(self):
        super().__init__()
        self.filename = MOD_FILENAMES["books_object_file"]
        self.parser_type = ParserType.BOOK
