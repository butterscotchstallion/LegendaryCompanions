from companiongenerator.loca_helper import generate_handle
from companiongenerator.template_replacer_base import TemplateReplacerBase


class LocalizationEntry(TemplateReplacerBase):
    """
    Creates a XML tag for localization entry with optional
    comment
    """

    def __init__(self, **kwargs):
        self.template_fetcher = kwargs["template_fetcher"]
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
