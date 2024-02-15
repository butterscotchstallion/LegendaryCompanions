from pathlib import Path

from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.stats_parser import StatsParser


class ItemCombosParser:
    is_file_empty: bool

    def __init__(self):
        self.is_file_empty = False

    def get_combo_names_from_file(self) -> list[str]:
        handle = Path(MOD_FILENAMES["item_combos"])
        file_contents = handle.read_text()
        combo_names: list[str] = []

        self.is_file_empty = not file_contents or len(file_contents) == 0

        if not self.is_file_empty:
            combo_file_lines = [
                line.strip() for line in file_contents.splitlines() if line.strip()
            ]
            stats_parser = StatsParser()
            for combo_line in combo_file_lines:
                if combo_line.startswith("new ItemCombination"):
                    combo_name = stats_parser.get_value_from_line_in_quotes(combo_line)
                    combo_names.append(combo_name)
        return combo_names
