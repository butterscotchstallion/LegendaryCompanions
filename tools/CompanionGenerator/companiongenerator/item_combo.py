from typing import TypedDict, Unpack

from companiongenerator.template_fetcher import TemplateFetcher
from companiongenerator.template_replacer_base import (
    TemplateReplacerBase,
)


class ItemComboName:
    """
    Instead of parsing the entire combo block,
    this is just the name which allows us to
    determine if a combo exists already
    """

    combo_name: str

    def __init__(self, combo_name: str):
        self.combo_name = combo_name

    # def __eq__(self, other):
    #    return self.combo_name == other.combo_name

    def __repr__(self) -> str:
        return self.combo_name


class ItemComboKeywords(TypedDict):
    combo_name: str
    object_one_name: str
    object_two_name: str
    combo_result_item_name: str


class ItemCombo(TemplateReplacerBase):
    """
    Handles combinations of items such as pages
    """

    def __init__(self, **kwargs: Unpack[ItemComboKeywords]):
        self.template_fetcher = TemplateFetcher()
        self.filename = "ItemCombos.txt"
        self.combo_name = kwargs["combo_name"]
        self.object_one_name = kwargs["object_one_name"]
        self.object_two_name = kwargs["object_two_name"]
        self.combo_result_item_name = kwargs["combo_result_item_name"]
        self.replacements = {
            "{{comboName}}": self.combo_name,
            "{{objectOneName}}": self.object_one_name,
            "{{objectTwoName}}": self.object_two_name,
            "{{comboResultItemName}}": self.combo_result_item_name,
        }

    def __repr__(self):
        return self.combo_name
