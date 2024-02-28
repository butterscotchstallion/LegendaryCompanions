from pathlib import Path

from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.stats_parser import StatsParser


class ItemComboParser(StatsParser):
    is_file_empty: bool

    def __init__(self):
        super().__init__()
        self.is_file_empty = False
        self.filename = MOD_FILENAMES["item_combos"]

    def get_file_contents(self) -> str:
        handle = Path(self.filename)
        return handle.read_text()

    def get_combo_names_from_file_contents(self, file_contents: str = "") -> set[str]:
        combo_names: set[str] = set()

        if len(file_contents) == 0:
            file_contents = self.get_file_contents()

        self.is_file_empty = not file_contents or len(file_contents) == 0

        if not self.is_file_empty:
            combo_file_lines = self.get_combo_file_lines(file_contents)
            stats_parser = StatsParser()
            for combo_line in combo_file_lines:
                if combo_line.startswith("new ItemCombination"):
                    combo_name = stats_parser.get_value_from_line_in_quotes(combo_line)
                    combo_names.add(combo_name)
        return combo_names

    def get_combo_file_lines(self, file_contents: str):
        return [line.strip() for line in file_contents.splitlines() if line.strip()]

    def combo_name_exists(self, combo_name: str, file_contents: str) -> bool:
        entries = self.get_combo_entries_from_file_contents(file_contents)
        if len(entries["combo_names"]) > 0:
            return combo_name in entries["combo_names"]
        else:
            return False

    def get_combo_entries_from_file_contents(
        self, file_contents: str = ""
    ) -> dict[str, set[str] | dict[str, set[str]]]:
        """
        Fetches pages, combo names, and result names from the file contents

        The second return type is for pages

        @return dict[str, set[str]] combo_names, combo_result_names, pages
        """
        combo_names: set[str] = set()
        combo_result_names: set[str] = set()
        pages: dict[str, set[str]] = {}
        combo_name_prefix = "new ItemCombination"
        combo_result_name_prefix = "new ItemCombinationResult"

        if len(file_contents) == 0:
            file_contents = self.get_file_contents()

        self.is_file_empty = not file_contents or bool(
            file_contents and len(file_contents) == 0
        )

        if not self.is_file_empty:
            combo_file_lines = self.get_combo_file_lines(file_contents)
            stats_parser = StatsParser()
            combo_name: str = ""
            for combo_line in combo_file_lines:
                """
                These names are pretty similar so we need to check
                that the combo name doesn't start with the result name
                too
                """
                if combo_line.startswith(
                    combo_name_prefix
                ) and not combo_line.startswith(combo_result_name_prefix):
                    combo_name = stats_parser.get_value_from_line_in_quotes(combo_line)
                    combo_names.add(combo_name)

                if combo_name and combo_line.startswith('data "Object '):
                    # Initialize set if not existent
                    if combo_name not in pages:
                        pages[combo_name] = set([])
                    # Example: data "Object 1" "OBJ_BeerBarrel"
                    quoted_values = self.get_quoted_values(combo_line)
                    if len(quoted_values) == 2:
                        pages[combo_name].add(quoted_values[1])

                if combo_line.startswith(combo_result_name_prefix):
                    combo_result_name = stats_parser.get_value_from_line_in_quotes(
                        combo_line
                    )
                    combo_result_names.add(combo_result_name)

        return {
            "combo_names": combo_names,
            "combo_result_names": combo_result_names,
            "pages": pages,
        }
