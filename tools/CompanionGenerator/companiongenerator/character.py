from typing import Required, TypedDict, Unpack

from companiongenerator.template_replacer_base import TemplateReplacerBase


class CharacterKeywords(TypedDict):
    stats_name: Required[str]


class Character(TemplateReplacerBase):
    """
    Base class for character templates. This should not be used
    directly
    """

    stats_name: str

    def __init__(self, **kwargs: Unpack[CharacterKeywords]):
        super().__init__()
        self.stats_name = kwargs["stats_name"]
        self.replacements = {"{{stats_name}}": self.stats_name}

    def __repr__(self):
        return self.stats_name
