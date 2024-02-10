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

    def parse_spell(self, spell_text: str) -> dict[str, str]:
        """
        Parses spell text, bailing out early if any of the validation
        tests fail.
        1. Parse "new entry" line and identify spell name
        2. Parse spell type line, which should be the second one
        3. Strip comments?
        4. Parse base spell line
        5.
        """
        spell: dict[str, str] = {
            "name": "",
            "base_spell_name": "",
            "display_name_handle": "",
            "description_handle": "",
            "spell_properties": "",
        }
        quoted_value_props = ["DisplayName", "Description", "SpellProperties"]
        spell_text_lines = self.get_spell_text_lines(spell_text)
        if spell_text_lines:
            # Spell name
            spell_name = self.get_spell_name_from_lines(spell_text_lines)
            if spell_name:
                spell["name"] = spell_name
            # Base spell
            base_spell_name = self.get_base_spell_name_from_lines(spell_text_lines)
            if base_spell_name:
                spell["base_spell_name"] = base_spell_name
            # Named properties
            for quoted_value in quoted_value_props:
                value = self.get_property_value_by_name(spell_text_lines, quoted_value)
                if value:
                    spell[quoted_value] = value
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
