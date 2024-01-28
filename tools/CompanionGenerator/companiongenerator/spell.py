"""
Spells
"""

from tests.template_validity_helper import is_valid_uuid

from companiongenerator.template_replacer_base import TemplateReplacerBase


class Spell:
    """
    Base spell definition which contains the properties
    shared by all varieties of spells
    """

    def __init__(self, **kwargs) -> None:
        self.loca_mgr = kwargs["localization_manager"]
        self.template_fetcher = kwargs["template_fetcher"]
        self.spell_name = kwargs["spell_name"]
        self.display_name_handle = self.loca_mgr.add_entry_and_return_handle(
            text=kwargs["display_name"],
            comment=kwargs["display_name"],
            template_fetcher=self.template_fetcher,
        )
        self.description_handle = self.loca_mgr.add_entry_and_return_handle(
            text=kwargs["description"],
            comment=kwargs["description"],
            template_fetcher=self.template_fetcher,
        )
        self.replacements = {
            "{{display_name_handle}}": self.display_name_handle,
            "{{description_handle}}": self.description_handle,
            "{{spell_name}}": self.spell_name,
        }


class SummonSpell(Spell, TemplateReplacerBase):
    """
    The spell used to summon the companion
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.filename = "summon_spell.txt"
        self.replacements["{{summon_uuid}}"] = kwargs["summon_uuid"]

        if not is_valid_uuid(kwargs["summon_uuid"]):
            raise ValueError(f'Invalid summon UUID supplied: {kwargs['summon_uuid']}')
