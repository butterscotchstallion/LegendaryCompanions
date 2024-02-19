from typing import TypedDict, Unpack

from companiongenerator.loca_helper import generate_handle
from companiongenerator.template_fetcher import TemplateFetcher
from companiongenerator.template_replacer_base import TemplateReplacerBase


class LocalizationEntryKeyWords(TypedDict):
    handle: str
    comment: str
    text: str


class LocalizationEntry(TemplateReplacerBase):
    """
    Creates a XML tag for localization entry with optional
    comment
    """

    def __init__(self, **kwargs: Unpack[LocalizationEntryKeyWords]):
        self.template_fetcher = TemplateFetcher()
        self.filename = "localization_entry.xml"
        self.handle = generate_handle()
        self.comment = ""

        if "comment" in kwargs:
            self.comment = kwargs["comment"]

        self.text = kwargs["text"]
        self.replacements = {
            "{{handle}}": self.handle,
            "{{comment}}": self.comment,
            "{{text}}": self.text,
        }

    def to_xml(self):
        return self.get_tpl_with_replacements()

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text
