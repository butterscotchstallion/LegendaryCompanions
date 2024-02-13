from pathlib import Path

from companiongenerator.constants import MOD_FILENAMES
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
    assert parsed_spell["using"] == base_spell_name
    assert parsed_spell["DisplayName"] == display_name_handle
    assert parsed_spell["Description"] == description_handle
    assert parsed_spell["SpellProperties"] == spell_properties


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


def test_get_spells_from_file():
    """Gets a list of all spells in a file and
    tests parsing spell names from those results
    """
    handle = Path(MOD_FILENAMES["spell_text_file_summons"])
    spell_text_file_contents = handle.read_text()
    spells = parser.get_spells_from_spell_text(spell_text_file_contents)
    expected_length = 5
    actual_length = len(spells)

    assert expected_length == actual_length

    # I was verifying the whole spell here but I realized
    # that I only need the name. This is here in case
    # I find a reason to parse the entire spell again

    # Each spell should be at least three lines
    # for spell in spells:
    #    assert len(spell.splitlines()) >= 3, "Spell should be at least three lines"

    expected_spell_names: list[str] = [
        "LC_Summon",
        "LC_Summon_RSO_Legendary",
        "LC_Summon_Githzerai_Legendary",
        "LC_Summon_Muffin_Legendary",
        "LC_Upgrade_Companion",
    ]
    parsed_spells = []

    for spell_text in spells:
        parsed_spell = parser.parse_spell(spell_text)
        parsed_spells.append(parsed_spell)

    actual_spell_names = [spell["name"] for spell in parsed_spells]

    assert expected_spell_names == actual_spell_names
