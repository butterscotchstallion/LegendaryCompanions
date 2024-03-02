import os
from enum import StrEnum
from pathlib import Path
from typing import Required, TypedDict

from companiongenerator.file_handler import FileHandler
from companiongenerator.logger import logger


class ParserType(StrEnum):
    SPELL = "Spell"
    EQUIPMENT = "Equipment"
    BOOK = "Book"
    ITEM_COMBOS = "ItemCombos"
    DEFAULT_TYPE = "Stats"


class StatsParserKeywords(TypedDict):
    filename: Required[str]
    parser_type: Required[ParserType]


class StatsParser:
    """Parses stats files into a dictionary

    Example structure:
    new entry "LC_Summon_Legendary_Kobold"
        using "LC_Summon"
            // Summon Legendary Kobold
            data "DisplayName" "haa04541egb497g4784gba4eg32ef2c8c2dda"
            // A powerful summoning scroll
            data "Description" "hee641648g2248g4ea5g8dc4g78fb27c8e7c7"
            data "SpellProperties" "GROUND:Summon(01b2da71-18fb-45de-9e21-a50cfc09a1bd,Permanent,,,UNSUMMON_ABLE,SHADOWCURSE_SUMMON_CHECK,LC_AUTOMATED)"

    """

    def __init__(self):
        """
        This is what the line for a new entry starts with in Stats entries.
        In other files, like equipment sets, the format is similar but it
        starts with "new equipment" instead.
        """
        self.new_entry_text: str = "new entry"
        self.filename: str = ""
        self.parser_type: ParserType = ParserType.DEFAULT_TYPE
        self.is_file_empty: bool = True

    def get_entry_name_from_lines(self, text_lines: list[str]) -> str | None:
        """
        Parses out entry name from a single entry
        """
        for line in text_lines:
            if line.startswith(self.new_entry_text):
                return self.get_value_from_line_in_quotes(line)

    def get_stripped_text_lines(self, stats_text: str) -> list[str]:
        lines = stats_text.splitlines()
        return [line.strip() for line in lines]

    def get_property_value_by_name(
        self, stats_text_lines: list[str], property_name: str
    ):
        for line in stats_text_lines:
            if line.startswith("data "):
                quoted_values = self.get_quoted_values(line)
                if len(quoted_values) == 2:
                    if quoted_values[0] == property_name:
                        return quoted_values[1]

    def get_base_spell_name_from_lines(self, stats_text_lines: list[str]):
        for line in stats_text_lines:
            if line.startswith("using "):
                quoted_values = self.get_quoted_values(line)
                if len(quoted_values) == 1:
                    return quoted_values[0]

    def is_comment(self, input: str) -> bool:
        return input.startswith("//")

    def parse_stats_entry(self, stats_text: str) -> dict[str, str]:
        """
        Parses stats text, bailing out early if any of the validation
        tests fail.
        1. Parse "new entry" line and identify stats name
        2. Parse stats type line, which should be the second one
        3. Strip comments?
        4. Parse base spell line
        """
        spell: dict[str, str] = {}

        """
        Iterate each line and split it into parts based on the
        portion before the quoted property, then the quoted value
        """
        stats_text_lines = self.get_stripped_text_lines(stats_text)
        for line in stats_text_lines:
            line_parts = [ls.strip() for ls in line.split('"') if ls.strip()]

            if len(line_parts) >= 2:
                first_element = line_parts[0]
                # Data line: we only care about what's after data
                if first_element == "data":
                    spell[line_parts[1]] = line_parts[2]
                # Non-data line has other keywords
                elif first_element == self.new_entry_text:
                    spell["name"] = line_parts[1]
                else:
                    spell[first_element] = line_parts[1]
        return spell

    def get_quoted_values(self, input: str) -> list[str]:
        values = input.split('"')[1::]
        return [value.strip() for value in values if value.strip()]

    def get_value_from_line_in_quotes(self, input: str) -> str:
        """Parses value from within quotes"""
        values = self.get_quoted_values(input)
        value = ""
        if len(values):
            value = values[0]
        return value

    def entry_name_exists_in_text(
        self, spell_name: str, spell_text_file_contents: str
    ) -> bool:
        """
        1. Get spells from supplied stats file text
        2. Parse each entry to get entry names
        3. Check if supplied entry name exists in this set
        """
        spell_name_list: set[str] = self.get_entry_names_from_text(
            spell_text_file_contents
        )

        if len(spell_text_file_contents) > 0 and len(spell_name_list) == 0:
            logger.error("Failed to parse spells from file!")

        return spell_name in spell_name_list

    def get_entry_names_from_text(self, stats_text: str = "") -> set[str]:
        """Parses entry names from file"""

        # Read from filename if no text supplied
        if len(stats_text) == 0:
            stats_text = self.get_file_contents()

        stripped_text_lines = self.get_stripped_text_lines(stats_text)
        spells: set[str] = set([])
        for line in stripped_text_lines:
            if line and line.startswith(self.new_entry_text):
                spell_name = self.get_value_from_line_in_quotes(line)
                spells.add(spell_name)
        return spells

    def get_entry_info_from_text(self, stats_text: str = "") -> dict[str, dict]:
        """Parses entry name and root template id from file"""

        # Read from filename if no text supplied
        if len(stats_text) == 0:
            stats_text = self.get_file_contents()

        stripped_text_lines = self.get_stripped_text_lines(stats_text)
        entry_info: dict[str, dict] = {}
        entry_name = ""
        for line in stripped_text_lines:
            quoted_values = self.get_quoted_values(line)

            if len(quoted_values) > 0:
                # Entry name
                if line.startswith(self.new_entry_text):
                    entry_name = quoted_values[0]
                    # logger.info(f"Entry name: {entry_name}")

                    # Initialize if not existent
                    if entry_name not in entry_info:
                        entry_info[entry_name] = {}

                # Root template id
                if line.startswith('data "RootTemplate"'):
                    # logger.info(f"Root template ID: {quoted_values[1]}")
                    entry_info[entry_name]["root_template_id"] = quoted_values[1]

                # Summon UUID
                # data "SpellProperties"
                # "GROUND:Summon(9b4518f1-7141-4d18-855f-edeafcaf4477,Permanent,,,UNSUMMON_ABLE,SHADOWCURSE_SUMMON_CHECK,LC_AUTOMATED)"
                if len(quoted_values) == 2 and line.startswith(
                    'data "SpellProperties"'
                ):
                    spell_properties_value = quoted_values[1]
                    looks_like_summon_spell = (
                        "Summon(" in spell_properties_value
                        and ")" in spell_properties_value
                    )
                    if looks_like_summon_spell:
                        # Get the values inside of the parenthesis
                        summon_spell_params = spell_properties_value[
                            spell_properties_value.find("(")
                            + 1 : spell_properties_value.find(")")
                        ]
                        spell_props = summon_spell_params.split(",")
                        if len(spell_props) > 0:
                            entry_info[entry_name]["summon_uuid"] = spell_props[0]

        return entry_info

    def get_file_contents(self) -> str:
        """
        Gets file contents from stats file
        """
        if self.filename:
            logger.trace(f"Loading file contents: {self.filename}")
            handle = Path(self.filename)
            contents = handle.read_text()
            self.is_file_empty = len(contents) == 0

            return contents
        else:
            logger.error(f"No filename set for {__class__}")
            return ""

    def add_entry(self, entry_name: str, entry_text: str) -> bool:
        """
        Adds new entry if it doesn't exist
        """
        existing_names: set[str] = self.get_entry_names_from_text(
            self.get_file_contents()
        )

        if entry_name not in existing_names:
            handler = FileHandler()
            backup_created = handler.create_backup_file(self.filename)
            if backup_created:
                with open(self.filename, "a+") as handle:
                    handle.seek(os.SEEK_END)

                    # Make sure we add a new line if it's not there
                    contents = entry_text
                    if not contents.startswith("\n"):
                        contents = "\n\n" + contents

                    success = bool(handle.write(contents))

                    if success:
                        logger.trace(f"Added {self.parser_type} entry to file")

                    return success
            else:
                return False
        else:
            return True
