from uuid import uuid4
from companiongenerator.template_replacer_base import TemplateReplacerBase


class LocalizationEntry(TemplateReplacerBase):
    """
    Creates a XML tag for localization entry with optional
    comment
    """

    def generate_handle(self):
        reg_uuid = "h" + str(uuid4())
        return reg_uuid.replace("-", "g")

    def __init__(self, **kwargs):
        self.template_fetcher = kwargs["template_fetcher"]
        self.filename = "localization_entry.xml"
        self.handle = self.generate_handle()
        self.comment = kwargs["comment"]
        self.text = kwargs["text"]
        self.replacements = {
            "{{handle}}": self.handle,
            "{{comment}}": self.comment,
            "{{text}}": self.text,
        }
