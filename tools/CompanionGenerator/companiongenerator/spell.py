"""
Spells
"""
from companiongenerator.template_replacer_base import TemplateReplacerBase


class Spell:
    """
    Base spell definition which contains the properties
    shared by all varieties of spells
    """

    def __init__(self, **kwargs) -> None:
        self.spell_name = kwargs["spell_name"]
        self.display_name = kwargs["display_name"]
        self.description = kwargs["description"]
        self.integration_name = kwargs["integration_name"]
        self.replacements = {
            "{{display_name}}": self.display_name,
            "{{description}}": self.description,
            "{{spell_name}}": self.spell_name,
            "{{integration_name}}": self.integration_name,
        }


class SummonSpell(Spell, TemplateReplacerBase):
    """
    The spell used to summon the companion
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.filename = "summon_spell.txt"
        self.summon_uuid = kwargs["summon_uuid"]
        self.template_fetcher = kwargs["template_fetcher"]
        self.replacements["{{summon_uuid}}"] = self.summon_uuid

    """
    def get_spell_template_text(self):
        return self.template_fetcher.get_template_text("summon_spell.txt")

    def get_spell_text(self):
        spell_tpl = self.get_spell_template_text()
        if spell_tpl:
            replacer = TemplateVariableReplacer()
            replaced_text = replacer.replace_placeholders(spell_tpl, self.replacements)
            return replaced_text
        else:
            log.error("Error reading summon spell template")
    """
