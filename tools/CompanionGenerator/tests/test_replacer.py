from companiongenerator import TemplateVariableReplacer


def test_replacer_basic():
    replacer = TemplateVariableReplacer()
    spell_text = """
        new entry "{{spell_name}}"
            type "SpellData"
            data "SpellType" "Target"
            using "Target_Bless"
            data "AmountOfTargets" "4"
            data "DescriptionParams" "1d4;4"
            data "UseCosts" "ActionPoint:1;SpellSlotsGroup:1:1:2"
            data "RootSpellID" "Target_Bless"
            data "PowerLevel" "2"
            data "CombatAIOverrideSpell" "Target_Bless_2_AI"
    """
    spell_name = "Target_Bless_2"
    replacements = {"{{spell_name}}": spell_name}
    replaced_text = replacer.replace(spell_text, replacements)
    assert replaced_text is not None
    assert spell_name in replaced_text
