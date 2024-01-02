"""
Spells
"""

from pathlib import Path
import logging as log

log.basicConfig(format="%(levelname)s:%(message)s", level=log.DEBUG)


class Spell:
    def __init__(self, spell_name) -> None:
        self.spell_name = spell_name


class SummonSpell(Spell):
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
                replacers = {
                    "{{display_name}}": self.display_name,
                    "{{description}}": self.description,
                    "{{summon_uuid}}": self.summon_uuid,
                    "{{spell_name}}": self.spell_name,
                    "{{integration_name}}": self.integration_name,
                }

                for replacer_var_name in replacers:
                    if replacer_var_name in spell_tpl:
                        spell_tpl = spell_tpl.replace(
                            replacer_var_name, replacers[replacer_var_name]
                        )
                        log.debug(
                            "Replaced {name} with {value}",
                            extra=dict(
                                name=replacer_var_name,
                                value=replacers[replacer_var_name],
                            ),
                        )
                    else:
                        log.error(
                            "Could not find replacer variable in template: {name}",
                            extra=dict(name=replacer_var_name),
                        )

                return spell_tpl
            else:
                log.error("Error reading summon spell template")
        except FileNotFoundError:
            log.error("Spell template file not found")
