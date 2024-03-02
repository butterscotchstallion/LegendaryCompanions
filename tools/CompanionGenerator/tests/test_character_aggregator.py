from uuid import uuid4

from companiongenerator.character_aggregator import CharacterAggregator
from companiongenerator.character_mindflayer import CharacterMindflayer
from companiongenerator.character_parser import CharacterParser
from companiongenerator.logger import logger


def test_add_entry():
    test_stats_name = f"LC_character_test_{uuid4()}"
    mindflayer = CharacterMindflayer(stats_name=test_stats_name)
    char_aggregator = CharacterAggregator()
    char_aggregator.add_entry(mindflayer)
    char_aggregator.add_entry(mindflayer)

    num_entries_with_this_name = len(
        [
            entry
            for entry in char_aggregator.entries
            if entry.stats_name == test_stats_name
        ]
    )
    assert num_entries_with_this_name == 1


def test_update_character_file():
    # Add entry
    chr_stats_name = f"LC_character_test_{uuid4()}"
    mindflayer = CharacterMindflayer(stats_name=chr_stats_name)
    char_aggregator = CharacterAggregator()
    char_aggregator.add_entry(mindflayer)

    # Verify file contents
    char_parser = CharacterParser()
    updated = char_aggregator.update_character_file()

    assert updated, "Failed to update character file"

    entries_from_file = char_parser.get_entry_names_from_text()

    logger.debug(f"CharacterAggregatorTest: {entries_from_file}")

    assert (
        chr_stats_name in entries_from_file
    ), "Failed to read new character entry from file"
