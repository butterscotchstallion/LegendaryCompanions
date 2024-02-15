from companiongenerator.stats_parser import StatsParser


class ItemCombosParser:
    is_file_empty: bool

    def __init__(self):
        self.is_file_empty = False

    def get_combo_names_from_file_contents(self, file_contents: str) -> list[str]:
        combo_names: list[str] = []

        self.is_file_empty = not file_contents or len(file_contents) == 0

        if not self.is_file_empty:
            combo_file_lines = self.get_combo_file_lines(file_contents)
            stats_parser = StatsParser()
            for combo_line in combo_file_lines:
                if combo_line.startswith("new ItemCombination"):
                    combo_name = stats_parser.get_value_from_line_in_quotes(combo_line)
                    combo_names.append(combo_name)
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
        self, file_contents: str
    ) -> dict[str, list[str]]:
        """
        Fetches both combo names and result names from the file contents
        """
        combo_names: list[str] = []
        combo_result_names: list[str] = []
        combo_name_prefix = "new ItemCombination"
        combo_result_name_prefix = "new ItemCombinationResult"

        self.is_file_empty = not file_contents or bool(
            file_contents and len(file_contents) == 0
        )

        if not self.is_file_empty:
            combo_file_lines = self.get_combo_file_lines(file_contents)
            stats_parser = StatsParser()
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
                    combo_names.append(combo_name)

                if combo_line.startswith(combo_result_name_prefix):
                    combo_result_name = stats_parser.get_value_from_line_in_quotes(
                        combo_line
                    )
                    combo_result_names.append(combo_result_name)

        return {"combo_names": combo_names, "combo_result_names": combo_result_names}
