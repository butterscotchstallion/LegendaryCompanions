from companiongenerator import SummonSpell


def test_gen_spell():
    spell_name = "LC_Summon_Kobold_Legendary"
    summon_uuid = "1419101c-3be0-431d-b607-0ac16071a695"
    display_name = "h1150f154g3281g44d8gb790g461d6a3e9b84"
    description = "hcb9c97fcg3eafg43f0g81d7gc478ec34a6f0"

    spell = SummonSpell(
        spell_name=spell_name,
        summon_uuid=summon_uuid,
        display_name=display_name,
        description=description,
    )

    generated_spell_text = spell.get_spell_text()

    assert generated_spell_text is not None
    assert spell_name in generated_spell_text
    assert display_name in generated_spell_text
    assert description in generated_spell_text
    assert summon_uuid in generated_spell_text
