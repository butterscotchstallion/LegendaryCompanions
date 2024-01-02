"""
Spells
"""
from pathlib import Path
import logging as log
from .template_variable_replacer import TemplateVariableReplacer

log.basicConfig(format="%(levelname)s:%(message)s", level=log.DEBUG)


class Spell:
    def __init__(self, spell_name) -> None:
        self.spell_name = spell_name


class SummonSpell(Spell):
    """
    The spell used to summon the companion
    """

    def __init__(self, **kwargs) -> None:
        self.spell_name = kwargs["spell_name"]
        self.summon_uuid = kwargs["summon_uuid"]
        self.display_name = kwargs["display_name"]
        self.description = kwargs["description"]
        self.integration_name = kwargs["integration_name"]
        self.validate_parameters(kwargs)

    def validate_parameters(self, kwargs):
        valid_summon_uuid = self.is_valid_summon_uuid(kwargs["summon_uuid"])
        if not valid_summon_uuid:
            raise Exception("Invalid summon_uuid!")

    def is_valid_summon_uuid(self, summon_uuid) -> bool:
        return summon_uuid and len(summon_uuid) == 36

    def get_spell_text(self):
        try:
            spell_tpl = Path(
                "./companiongenerator/templates/summon_spell.txt"
            ).read_text()
            if spell_tpl:
                replacements = {
                    "{{display_name}}": self.display_name,
                    "{{description}}": self.description,
                    "{{summon_uuid}}": self.summon_uuid,
                    "{{spell_name}}": self.spell_name,
                    "{{integration_name}}": self.integration_name,
                }

                replacer = TemplateVariableReplacer()
                replaced_text = replacer.replace(spell_tpl, replacements)

                return replaced_text
            else:
                log.error("Error reading summon spell template")
        except FileNotFoundError:
            log.error("Spell template file not found")
