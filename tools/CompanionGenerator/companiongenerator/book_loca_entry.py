from companiongenerator.localization_aggregator import LocalizationAggregator
from companiongenerator.template_fetcher import TemplateFetcher
from companiongenerator.template_replacer_base import TemplateReplacerBase


class BookLocaEntry(TemplateReplacerBase):
    """
    Book localization entry
    """

    # Book file entry
    content: str
    unknown_description: str
    name: str
    # Handles
    content_handle: str
    unknown_description_handle: str

    def __init__(self, **kwargs):
        # Basic book loca entry properties
        self.name = kwargs["name"]
        self.content = kwargs["content"]
        self.unknown_description = kwargs["unknown_description"]
        # Template replacement configuration
        self.base_path = "../templates/"
        self.filename = f"{self.base_path}book_loca_entry.xml"
        self.template_fetcher = TemplateFetcher()
        self.localization_aggregator: LocalizationAggregator = kwargs[
            "localization_aggregator"
        ]

        # Generate handles for what must be localized
        self.content_handle = self.localization_aggregator.add_entry_and_return_handle(
            text=self.content
        )
        self.unknown_description_handle = (
            self.localization_aggregator.add_entry_and_return_handle(
                text=self.unknown_description
            )
        )

        # Set up template replacements
        self.replacements = {"{{name}}": kwargs["name"]}
        self.replacements[
            "{{unknown_description_handle}}"
        ] = self.unknown_description_handle
        self.replacements["{{content_handle}}"] = self.content_handle
