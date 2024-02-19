from pathlib import Path

from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.logger import logger
from companiongenerator.stats_parser import ParserType, StatsParser

parser = StatsParser(
    filename=MOD_FILENAMES["spell_text_file_summons"], parser_type=ParserType.SPELL
)
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
    return parser.get_stripped_text_lines(spell_text)


def test_parse_stats():
    """Tests parsing of stats files"""
    spell_name = "LC_Summon_Legendary_Kobold"
    base_spell_name = "LC_Summon"
    display_name_handle = "haa04541egb497g4784gba4eg32ef2c8c2dda"
    description_handle = "hee641648g2248g4ea5g8dc4g78fb27c8e7c7"
    spell_properties = "GROUND:Summon(01b2da71-18fb-45de-9e21-a50cfc09a1bd,Permanent,,,UNSUMMON_ABLE,SHADOWCURSE_SUMMON_CHECK,LC_AUTOMATED)"

    parsed_spell = parser.parse_stats_entry(spell_text)

    assert parsed_spell["name"] == spell_name
    assert parsed_spell["using"] == base_spell_name
    assert parsed_spell["DisplayName"] == display_name_handle
    assert parsed_spell["Description"] == description_handle
    assert parsed_spell["SpellProperties"] == spell_properties


def test_get_entry_name_from_lines():
    expected = "LC_Summon_Legendary_Kobold"
    lines = parser.get_stripped_text_lines(spell_text)
    actual = parser.get_entry_name_from_lines(lines)
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


def test_get_entry_names_from_file():
    """Gets a list of all entries in a file and
    tests parsing entry names from those results
    """
    handle = Path(MOD_FILENAMES["spell_text_file_summons"])
    spell_text_file_contents = handle.read_text()
    spell_list = parser.get_entry_names_from_text(spell_text_file_contents)
    spells_set: set[str] = set(spell_list)

    if len(spell_text_file_contents) > 0 and len(spell_list) == 0:
        assert len(spell_list) > 0, "No spells in list!"

    expected_spell_names: set[str] = set(
        [
            "LC_Summon",
            "LC_Summon_RSO_Legendary",
            "LC_Summon_Githzerai_Legendary",
            "LC_Summon_Muffin_Legendary",
            "LC_Upgrade_Companion",
        ]
    )

    assert expected_spell_names.issubset(spells_set)


def test_parse_book_objects_file():
    handle = Path(MOD_FILENAMES["books_object_file"])
    objects_file_text = handle.read_text()
    book_name_list = parser.get_entry_names_from_text(objects_file_text)

    if objects_file_text:
        assert len(book_name_list) > 0, "Failed to get book object names"
    else:
        logger.info("Empty object file")
