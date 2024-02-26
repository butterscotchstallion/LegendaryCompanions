from uuid import uuid4

from companiongenerator.localization_aggregator import LocalizationAggregator
from companiongenerator.spell import SpellName, SummonSpell
from companiongenerator.spell_aggregator import SpellAggregator


def test_spell_aggregator():
    spell_aggregator = SpellAggregator()
    loaded_names = spell_aggregator.load_entries_from_file()
    assert loaded_names, "Failed to load spell names from file"


def test_get_eligible_entries():
    spell_aggregator = SpellAggregator()
    spell_aggregator.add_entry(
        SummonSpell(
            display_name="Test spell",
            spell_name="Test Spell",
            description="Spell description",
            summon_uuid=str(uuid4()),
            localization_aggregator=LocalizationAggregator(),
        )
    )
    spell_aggregator.add_entry(SpellName(spell_name="Test spell name"))
    eligible_entries = spell_aggregator.get_eligible_entries()
    assert (
        len(eligible_entries) == 1
    ), "Failed to excluse SpellName entries from eligibility"
