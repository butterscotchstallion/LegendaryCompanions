from companiongenerator.character import Character
from companiongenerator.character_aggregator import CharacterAggregator


def test_char_aggregator():
    char = Character()
    char_aggregator = CharacterAggregator()
    char_aggregator.add_entry(char)
    char_aggregator.add_entry(char)

    assert len(char_aggregator.entries) == 1
