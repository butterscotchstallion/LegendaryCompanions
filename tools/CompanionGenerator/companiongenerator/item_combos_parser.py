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

    def get_combo_entries_from_file_contents(
        self, file_contents: str
    ) -> dict[str, list[str]]:
        """
        Fetches both combo names and result names from the file contents
        """
        combo_names: list[str] = []
        combo_result_names: list[str] = []
        self.is_file_empty = not file_contents or bool(
            file_contents and len(file_contents) == 0
        )

        if not self.is_file_empty:
            combo_file_lines = self.get_combo_file_lines(file_contents)
            stats_parser = StatsParser()
            for combo_line in combo_file_lines:
                """
                We need a quote after the ItemCombination otherwise
                we get result names too!
                """
                if combo_line.startswith('new ItemCombination "'):
                    combo_name = stats_parser.get_value_from_line_in_quotes(combo_line)
                    combo_names.append(combo_name)

                if combo_line.startswith("new ItemCombinationResult"):
                    combo_result_name = stats_parser.get_value_from_line_in_quotes(
                        combo_line
                    )
                    combo_result_names.append(combo_result_name)

        return {"combo_names": combo_names, "combo_result_names": combo_result_names}
