from typing import NotRequired, TypedDict, Unpack

from companiongenerator.loca_helper import generate_handle
from companiongenerator.template_fetcher import TemplateFetcher
from companiongenerator.template_replacer_base import TemplateReplacerBase


class LocalizationEntryKeyWords(TypedDict):
    text: str
    comment: NotRequired[str]
    handle: NotRequired[str]


class LocalizationEntry(TemplateReplacerBase):
    """
    Creates a XML tag for localization entry with optional
    comment
    """

    def __init__(self, **kwargs: Unpack[LocalizationEntryKeyWords]):
        self.template_fetcher = TemplateFetcher()
        self.filename = "localization_entry.xml"
        self.comment = ""

        """
        Use handle if provided in the case of existing localization
        entries
        """
        if "handle" in kwargs and kwargs["handle"]:
            self.handle = kwargs["handle"]
        else:
            self.handle = generate_handle()

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
