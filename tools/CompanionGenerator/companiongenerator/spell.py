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
        self.template_fetcher = kwargs["template_fetcher"]
        self.replacements["{{summon_uuid}}"] = kwargs["summon_uuid"]
