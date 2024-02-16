from typing import TypedDict, Unpack

from companiongenerator.template_fetcher import TemplateFetcher
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
        self.template_fetcher = TemplateFetcher()
        self.filename = "object_book.txt"
        self.stats_name: str = kwargs["stats_name"]
        self.root_template_id: str = kwargs["root_template_id"]
        self.replacements = {
            "{{stats_name}}": self.stats_name,
            "{{root_template_id}}": self.root_template_id,
        }
