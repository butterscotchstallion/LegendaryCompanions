from companiongenerator.logger import logger


class StatsParser:
    """Parses spell files into a dictionary

    Example structure:
    new entry "LC_Summon_Legendary_Kobold"
        using "LC_Summon"
            // Summon Legendary Kobold
            data "DisplayName" "haa04541egb497g4784gba4eg32ef2c8c2dda"
            // A powerful summoning scroll
            data "Description" "hee641648g2248g4ea5g8dc4g78fb27c8e7c7"
            data "SpellProperties" "GROUND:Summon(01b2da71-18fb-45de-9e21-a50cfc09a1bd,Permanent,,,UNSUMMON_ABLE,SHADOWCURSE_SUMMON_CHECK,LC_AUTOMATED)"

    """

    def get_spell_name_from_lines(self, spell_text_lines: list[str]) -> str | None:
        """
        Parses out spell name from a single spell
        """
        for line in spell_text_lines:
            if line.startswith("new entry"):
                return self.get_value_from_line_in_quotes(line)

    def get_spell_text_lines(self, spell_text: str) -> list[str]:
        lines = spell_text.splitlines()
        return [line.strip() for line in lines if line.strip()]

    def get_property_value_by_name(
        self, spell_text_lines: list[str], property_name: str
    ):
        for line in spell_text_lines:
            if line.startswith("data "):
                quoted_values = self.get_quoted_values(line)
                if len(quoted_values) == 2:
                    if quoted_values[0] == property_name:
                        return quoted_values[1]

    def get_base_spell_name_from_lines(self, spell_text_lines: list[str]):
        for line in spell_text_lines:
            if line.startswith("using "):
                quoted_values = self.get_quoted_values(line)
                if len(quoted_values) == 1:
                    return quoted_values[0]

    def is_comment(self, input: str) -> bool:
        return input.startswith("//")

    def parse_spell(self, spell_text: str) -> dict[str, str]:
        """
        Parses spell text, bailing out early if any of the validation
        tests fail.
        1. Parse "new entry" line and identify spell name
        2. Parse spell type line, which should be the second one
        3. Strip comments?
        4. Parse base spell line
        """
        spell: dict[str, str] = {}

        """
        Iterate each line and split it into parts based on the
        portion before the quoted property, then the quoted value
        """
        spell_text_lines = self.get_spell_text_lines(spell_text)
        for line in spell_text_lines:
            line_parts = [ls.strip() for ls in line.split('"') if ls.strip()]

            if len(line_parts) >= 2:
                first_element = line_parts[0]
                # Data line: we only care about what's after data
                if first_element == "data":
                    spell[line_parts[1]] = line_parts[2]
                # Non-data line has other keywords
                elif first_element == "new entry":
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

    def spell_name_exists_in_spell_text(
        self, spell_name: str, spell_text_file_contents: str
    ) -> bool:
        """
        1. Get spells from supplied spell file text
        2. Parse each spell to get spell names
        3. Check if supplied spell name exists in this set
        """
        spell_name_list: list[str] = self.get_spell_names_from_spell_text(
            spell_text_file_contents
        )

        if len(spell_text_file_contents) > 0 and len(spell_name_list) == 0:
            logger.error("Failed to parse spells from file!")
        else:
            logger.info(f"Spell list: {spell_name_list}")

        return spell_name in spell_name_list

    def get_spell_names_from_spell_text(self, spell_text: str) -> list[str]:
        """Parses spell name from file contents"""
        spell_text_lines = self.get_spell_text_lines(spell_text)
        spells: list[str] = []
        for line in spell_text_lines:
            if line.startswith("new entry"):
                spell_name = self.get_value_from_line_in_quotes(line)
                spells.append(spell_name)
        return spells