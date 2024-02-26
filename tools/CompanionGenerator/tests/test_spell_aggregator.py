from companiongenerator.spell_aggregator import SpellAggregator


def test_spell_aggregator():
    spell_aggregator = SpellAggregator()
    loaded_names = spell_aggregator.load_entries_from_file()
    assert loaded_names, "Failed to load spell names from file"
