from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.stats_parser import ParserType, StatsParser


class SpellParser(StatsParser):
    def __init__(self):
        super().__init__()

        self.parser_type = ParserType.SPELL

        # TODO: add logic here if we add spells in other files
        self.filename: str = MOD_FILENAMES["spell_text_file_summons"]
