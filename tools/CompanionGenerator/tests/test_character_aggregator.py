from companiongenerator.character_aggregator import CharacterAggregator
from companiongenerator.character_mindflayer import CharacterMindflayer


def test_char_aggregator():
    mindflayer = CharacterMindflayer(stats_name="LC_character_test")
    char_aggregator = CharacterAggregator()
    char_aggregator.add_entry(mindflayer)
    char_aggregator.add_entry(mindflayer)

    assert len(char_aggregator.entries) == 1
