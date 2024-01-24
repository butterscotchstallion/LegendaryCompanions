import logging as log
from uuid import uuid4

from companiongenerator.localization_manager import (
    LocalizationManager,
)
from companiongenerator.template_fetcher import TemplateFetcher
from companiongenerator.template_replacer_base import TemplateReplacerBase


class RootTemplate(TemplateReplacerBase):
    """
    Creates XML file using template
    1. Set base path
    2. Add filename parameter
    3. Create RT template
    4. Add replacement variables
    """

    def __init__(self, **kwargs) -> None:
        self.base_path: str = "".join(
            [
                "../../../LegendaryCompanions/Mods/LegendaryCompanions/public/",
                "LegendaryCompanions/RootTemplates/",
            ]
        )
        self.template_fetcher: TemplateFetcher = kwargs["template_fetcher"]
        loca_mgr = LocalizationManager()
        self.display_name_handle = loca_mgr.add_entry_and_return_handle(
            text=kwargs["displayName"],
            comment=kwargs["displayName"],
            template_fetcher=self.template_fetcher,
        )
        self.replacements: dict[str, str] = {
            "{{name}}": kwargs["name"],
            "{{displayNameHandle}}": self.display_name_handle,
            "{{mapKey}}": str(uuid4()),
            "{{statsName}}": kwargs["statsName"],
        }


class CompanionRT(RootTemplate):
    """
    Root template with companion settings
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.filename = f"{self.base_path}rt_companion.xml"
        loca_mgr = LocalizationManager()
        # Companion specific replacements below
        archetype: str = "melee_smart"
        if "archetypeName" in kwargs:
            archetype = kwargs["archetypeName"]
        self.replacements["{{archetypeName}}"] = archetype
        self.replacements["{{parentTemplateId}}"] = kwargs["parentTemplateId"]
        self.replacements["{{equipmentSetName}}"] = kwargs["equipmentSetName"]

        if "title" in kwargs:
            self.title_handle = loca_mgr.add_entry_and_return_handle(
                text=kwargs["title"],
                comment=kwargs["title"],
                template_fetcher=self.template_fetcher,
            )
            self.replacements["{{titleHandle}}"] = self.title_handle
            log.info("Replacing title")
        else:
            raise RuntimeError("No title specified")

        if "tagList" in kwargs:
            tag_list = kwargs["tagList"]
            self.replacements["{{tagList}}"] = tag_list
        else:
            self.replacements["{{tagList}}"] = ""


class PageRT(RootTemplate):
    """
    Root template for objects like books and scrolls
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filename = f"{self.base_path}rt_page.xml"
        self.replacements["{{icon}}"] = kwargs["icon"]

        loca_mgr = LocalizationManager()
        self.description_handle = loca_mgr.add_entry_and_return_handle(
            text=kwargs["description"],
            comment=kwargs["description"],
            template_fetcher=self.template_fetcher,
        )
        self.replacements["{{descriptionHandle}}"] = self.description_handle


class BookRT(PageRT):
    """
    Root template for books
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filename = f"{self.base_path}rt_book.xml"
        self.replacements["{{bookId}}"] = kwargs["bookId"]
