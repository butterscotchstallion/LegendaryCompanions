from typing import TypedDict, Unpack

from companiongenerator.template_replacer_base import TemplateReplacerBase


class StatsObjectKeywords(TypedDict):
    stats_name: str
    root_template_id: str


class StatsObject(TemplateReplacerBase):
    """
    Represents objects in text files linked
    to a RT entry
    """

    def __init__(self, **kwargs: Unpack[StatsObjectKeywords]):
        super().__init__()

        self.template_filename = "object_book.txt"
        self.stats_name: str = kwargs["stats_name"]
        self.root_template_id: str = kwargs["root_template_id"]
        self.replacements = {
            "{{stats_name}}": self.stats_name,
            "{{root_template_id}}": self.root_template_id,
        }

    def __hash__(self) -> int:
        return hash(repr(self))

    def __eq__(self, other):
        return self.root_template_id == other.root_template_id

    def __lt__(self, other):
        return self.stats_name > other.stats_name

    def __repr__(self) -> str:
        return self.stats_name
