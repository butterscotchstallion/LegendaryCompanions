"""
Spells
"""

from typing import NotRequired, TypedDict, Unpack

from tests.template_validity_helper import is_valid_uuid

from companiongenerator.localization_aggregator import LocalizationAggregator
from companiongenerator.template_fetcher import TemplateFetcher
from companiongenerator.template_replacer_base import TemplateReplacerBase


class SpellKeywords(TypedDict):
    localization_aggregator: LocalizationAggregator
    spell_name: str
    display_name: str
    description: str


class SpellNameKeywords(TypedDict):
    spell_name: NotRequired[str]


class SpellName:
    spell_name: str

    def __init__(self, **kwargs: Unpack[SpellNameKeywords]):
        if "spell_name" in kwargs:
            self.spell_name = kwargs["spell_name"]

    def __repr__(self):
        return self.spell_name


class Spell(TemplateReplacerBase):
    """
    Base spell definition which contains the properties
    shared by all varieties of spells
    """

    base_spell_name: str
    spell_properties: str
    spell_name: str
    display_name_handle: str
    description_handle: str
    replacements: dict[str, str]
    loca_aggregator: LocalizationAggregator

    def __init__(self, **kwargs: Unpack[SpellKeywords]) -> None:
        self.base_spell_name = ""
        self.spell_properties = ""
        self.loca_aggregator = kwargs["localization_aggregator"]
        self.template_fetcher = TemplateFetcher()
        self.spell_name = kwargs["spell_name"]
        self.display_name_handle = self.loca_aggregator.add_entry_and_return_handle(
            text=kwargs["display_name"],
            comment=kwargs["display_name"],
        )
        self.description_handle = self.loca_aggregator.add_entry_and_return_handle(
            text=kwargs["description"],
            comment=kwargs["description"],
        )
        self.replacements = {
            "{{display_name}}": kwargs["display_name"],
            "{{description}}": kwargs["description"],
            "{{display_name_handle}}": self.display_name_handle,
            "{{description_handle}}": self.description_handle,
            "{{spell_name}}": self.spell_name,
        }

    def __repr__(self):
        return self.spell_name


class SummonSpellKeywords(SpellKeywords):
    summon_uuid: str


class SummonSpell(Spell, TemplateReplacerBase):
    """
    The spell used to summon the companion
    """

    filename: str
    summon_uuid: str

    def __init__(self, **kwargs: Unpack[SummonSpellKeywords]) -> None:
        super().__init__(**kwargs)
        self.template_filename = "summon_spell.txt"
        self.replacements["{{summon_uuid}}"] = kwargs["summon_uuid"]
        self.summon_uuid = kwargs["summon_uuid"]

        if not is_valid_uuid(kwargs["summon_uuid"]):
            raise ValueError(f'Invalid summon UUID supplied: {kwargs['summon_uuid']}')
