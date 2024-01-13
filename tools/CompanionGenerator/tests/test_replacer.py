from companiongenerator import TemplateVariableReplacer


def test_replacer_basic():
    """
    Tests the basic functionality of the replacer
    """
    spell_text = """
        new entry "{{spell_name}}"
            type "SpellData"
            data "SpellType" "Target"
            using "{{spell_name}}"
            data "AmountOfTargets" "4"
            data "DescriptionParams" "1d4;4"
            data "UseCosts" "ActionPoint:1;SpellSlotsGroup:1:1:2"
            data "RootSpellID" "{{spell_name}}"
            data "PowerLevel" "{{power_level}}"
            data "CombatAIOverrideSpell" "Target_Bless_2_AI"
    """
    spell_name: str = "Target_Bless_2"
    power_level: int = 2
    replacements: dict = {
        "{{spell_name}}": spell_name,
        "{{power_level}}": power_level,
    }
    replacer = TemplateVariableReplacer()
    replaced_text = replacer.replace_placeholders(spell_text, replacements)
    assert replaced_text is not None
    assert spell_name in replaced_text
    assert str(power_level) in replaced_text
