from uuid import uuid4

from companiongenerator import SummonSpell
from companiongenerator.localization_aggregator import LocalizationAggregator
from companiongenerator.template_fetcher import TemplateFetcher


def test_generate_spell():
    """
    Tests basic spell generation
    """
    spell_name = "LC_Summon_Kobold_Legendary"
    summon_uuid = str(uuid4())
    display_name = "h1150f154g3281g44d8gb790g461d6a3e9b84"
    description = "hcb9c97fcg3eafg43f0g81d7gc478ec34a6f0"
    integration_name = "LC_Muffin_Integration"
    fetcher = TemplateFetcher()
    spell = SummonSpell(
        spell_name=spell_name,
        summon_uuid=summon_uuid,
        display_name=display_name,
        description=description,
        integration_name=integration_name,
        template_fetcher=fetcher,
        localization_manager=LocalizationAggregator(),
    )

    generated_spell_text = spell.get_tpl_with_replacements()

    if generated_spell_text:
        all_lines = generated_spell_text.splitlines()
        spell_text_lines = [line for line in all_lines if line]
        assert generated_spell_text is not None
        assert spell_name in spell_text_lines[0]
        assert spell.display_name_handle in generated_spell_text
        assert spell.description_handle in generated_spell_text
        assert summon_uuid in generated_spell_text
    else:
        assert False
