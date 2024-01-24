"""
Spells
"""
import logging as log

from .template_variable_replacer import TemplateVariableReplacer


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


class SummonSpell(Spell):
    """
    The spell used to summon the companion
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.summon_uuid = kwargs["summon_uuid"]
        self.template_fetcher = kwargs["template_fetcher"]

    def get_spell_template_text(self):
        return self.template_fetcher.get_template_text("summon_spell.txt")

    def get_spell_text(self):
        spell_tpl = self.get_spell_template_text()
        if spell_tpl:
            replacements = {
                "{{display_name}}": self.display_name,
                "{{description}}": self.description,
                "{{summon_uuid}}": self.summon_uuid,
                "{{spell_name}}": self.spell_name,
                "{{integration_name}}": self.integration_name,
            }

            replacer = TemplateVariableReplacer()
            replaced_text = replacer.replace_placeholders(spell_tpl, replacements)

            return replaced_text
        else:
            log.error("Error reading summon spell template")
