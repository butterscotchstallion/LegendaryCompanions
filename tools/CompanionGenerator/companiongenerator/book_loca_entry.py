from companiongenerator.template_replacer_base import TemplateReplacerBase


class BookLocaEntry(TemplateReplacerBase):
    """
    Book localization entry
    """

    def __init__(self, **kwargs):
        self.base_path = "../templates/"
        self.filename = f"{self.base_path}book_loca_entry.xml"
        self.localization_aggregator = kwargs["localization_aggregator"]
        self.template_fetcher = kwargs["template_fetcher"]
        self.replacements = {"{{name}}": kwargs["name"]}

        # Content
        self.content_handle = self.localization_aggregator.add_entry_and_return_handle(
            text=kwargs["content"],
            comment=kwargs["content"],
            template_fetcher=self.template_fetcher,
        )
        self.replacements["{{contentHandle}}"] = self.content_handle

        # Unknown description
        self.unknown_description_handle = (
            self.localization_aggregator.add_entry_and_return_handle(
                text=kwargs["unknownDescription"],
                comment=kwargs["unknownDescription"],
                template_fetcher=self.template_fetcher,
            )
        )
        self.replacements[
            "{{unknownDescriptionHandle}}"
        ] = self.unknown_description_handle
