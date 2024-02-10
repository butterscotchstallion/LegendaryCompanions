from companiongenerator.stats_parser import StatsParser

parser = StatsParser()
spell_text = """
    new entry "LC_Summon_Legendary_Kobold"
    type "SpellData"
    using "LC_Summon"
        // Summon Legendary Kobold
        data "DisplayName" "haa04541egb497g4784gba4eg32ef2c8c2dda"
        // A powerful summoning scroll
        data "Description" "hee641648g2248g4ea5g8dc4g78fb27c8e7c7"
        data "SpellProperties" "GROUND:Summon(01b2da71-18fb-45de-9e21-a50cfc09a1bd,Permanent,,,UNSUMMON_ABLE,SHADOWCURSE_SUMMON_CHECK,LC_AUTOMATED)"
"""


def get_spell_text_lines() -> list[str]:
    return parser.get_spell_text_lines(spell_text)


def test_parse_stats():
    """Tests parsing of stats files"""
    spell_name = "LC_Summon_Legendary_Kobold"
    base_spell_name = "LC_Summon"
    display_name_handle = "haa04541egb497g4784gba4eg32ef2c8c2dda"
    description_handle = "hee641648g2248g4ea5g8dc4g78fb27c8e7c7"
    spell_properties = "GROUND:Summon(01b2da71-18fb-45de-9e21-a50cfc09a1bd,Permanent,,,UNSUMMON_ABLE,SHADOWCURSE_SUMMON_CHECK,LC_AUTOMATED)"

    parsed_spell = parser.parse_spell(spell_text)

    assert parsed_spell["name"] == spell_name
    assert parsed_spell["DisplayName"] == display_name_handle
    assert parsed_spell["Description"] == description_handle
    assert parsed_spell["SpellProperties"] == spell_properties
    assert parsed_spell["base_spell_name"] == base_spell_name


def test_get_spell_name_from_lines():
    expected = "LC_Summon_Legendary_Kobold"
    lines = parser.get_spell_text_lines(spell_text)
    actual = parser.get_spell_name_from_lines(lines)
    assert expected == actual


def test_parse_quoted_value():
    """Parses spell name from new entry line"""
    # Normal input
    spell_input = 'new entry "LC_Summon_Legendary_Kobold"'
    actual_value = parser.get_value_from_line_in_quotes(spell_input)
    expected_value = "LC_Summon_Legendary_Kobold"
    assert actual_value == expected_value, "Failed to get value from quotes"

    # Malformed input
    mal_spell_input = "new entry bandersnatch"
    mal_actual_value = parser.get_value_from_line_in_quotes(mal_spell_input)
    expected_value = ""
    assert (
        mal_actual_value == expected_value
    ), "Unexpected value for malformed spell input"
