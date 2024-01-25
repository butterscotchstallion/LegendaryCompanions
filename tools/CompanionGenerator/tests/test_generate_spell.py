from companiongenerator import SummonSpell
from companiongenerator.template_fetcher import TemplateFetcher


def test_generate_spell():
    """
    Tests basic spell generation
    """
    spell_name = "LC_Summon_Kobold_Legendary"
    summon_uuid = "1419101c-3be0-431d-b607-0ac16071a695"
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
    )

    generated_spell_text = spell.get_spell_text()

    if generated_spell_text is not None:
        all_lines = generated_spell_text.splitlines()
        spell_text_lines = [line for line in all_lines if line]
        assert generated_spell_text is not None
        assert integration_name in spell_text_lines[0]
        assert spell_name in spell_text_lines[1]
        assert display_name in generated_spell_text
        assert description in generated_spell_text
        assert summon_uuid in generated_spell_text
    else:
        assert False
