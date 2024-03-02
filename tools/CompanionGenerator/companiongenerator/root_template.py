from typing import NotRequired, Required, TypedDict, Unpack
from uuid import uuid4

from tests.template_validity_helper import is_valid_uuid

from companiongenerator.constants import ARCH_MELEE_SMART_NAME
from companiongenerator.localization_aggregator import LocalizationAggregator
from companiongenerator.template_fetcher import TemplateFetcher
from companiongenerator.template_replacer_base import TemplateReplacerBase


class RootTemplateKeywords(TypedDict):
    localization_aggregator: Required[LocalizationAggregator]
    name: Required[str]
    displayName: Required[str]
    statsName: Required[str]
    parentTemplateId: NotRequired[str]


class RootTemplate(TemplateReplacerBase):
    """
    Creates XML file using template
    1. Set base path
    2. Add filename parameter
    3. Create RT template
    4. Add replacement variables
    """

    def __init__(self, **kwargs: Unpack[RootTemplateKeywords]) -> None:
        self.base_path: str = "../templates/"
        self.template_fetcher: TemplateFetcher = TemplateFetcher()
        self.loca_aggregator: LocalizationAggregator = kwargs["localization_aggregator"]
        self.name: str = kwargs["name"]
        self.display_name: str = kwargs["displayName"]
        self.display_name_handle: str = (
            self.loca_aggregator.add_entry_and_return_handle(
                text=kwargs["displayName"],
                comment=kwargs["displayName"],
            )
        )
        self.map_key: str = str(uuid4())
        self.replacements: dict[str, str] = {
            "{{name}}": self.name,
            "{{displayNameHandle}}": self.display_name_handle,
            "{{mapKey}}": self.map_key,
            "{{statsName}}": kwargs["statsName"],
        }

    def get_comment(self):
        return self.display_name


class CompanionRTKeywords(TypedDict):
    """
    This is pretty similar to the RootTemplateKeywords
    but we want the parentTemplateId to be required here.
    """

    localization_aggregator: Required[LocalizationAggregator]
    name: Required[str]
    displayName: Required[str]
    statsName: Required[str]
    equipmentSetName: Required[str]
    parentTemplateId: Required[str]
    # Optional
    title: NotRequired[str]
    archetypeName: NotRequired[str]
    icon: NotRequired[str]


class CompanionRT(RootTemplate):
    """
    Root template with companion settings
    """

    def __init__(self, **kwargs: Unpack[CompanionRTKeywords]) -> None:
        super().__init__(**kwargs)
        self.template_filename: str = f"{self.base_path}rt_companion.xml"
        self.title: str = ""
        self.equipment_set_name: str = kwargs["equipmentSetName"]

        # Companion specific replacements below
        archetype: str = ARCH_MELEE_SMART_NAME
        if "archetypeName" in kwargs:
            archetype = kwargs["archetypeName"]
        self.replacements["{{archetypeName}}"] = archetype
        self.replacements["{{equipmentSetName}}"] = self.equipment_set_name

        if "parentTemplateId" in kwargs and is_valid_uuid(kwargs["parentTemplateId"]):
            self.replacements["{{parentTemplateId}}"] = kwargs["parentTemplateId"]
        else:
            raise RuntimeError(
                "Invalid or no parentTemplateId supplied: " + kwargs["parentTemplateId"]
            )

        if "title" in kwargs:
            self.title = kwargs["title"]
            self.title_handle = self.loca_aggregator.add_entry_and_return_handle(
                text=kwargs["title"],
                comment=kwargs["title"],
            )
            self.replacements["{{titleHandle}}"] = self.title_handle

        if "tagList" in kwargs:
            tag_list = kwargs["tagList"]
            self.replacements["{{tagList}}"] = tag_list
        else:
            self.replacements["{{tagList}}"] = ""

    def get_comment(self):
        return self.title or self.display_name


class ItemRTKeywords(RootTemplateKeywords):
    name: str
    description: str
    icon: NotRequired[str]


class PageRT(RootTemplate):
    """
    Root template for objects like books and scrolls
    """

    def __init__(self, **kwargs: Unpack[ItemRTKeywords]):
        super().__init__(**kwargs)
        self.template_filename = f"{self.base_path}rt_object_page.xml"
        self.replacements["{{icon}}"] = "Item_BOOK_GEN_Paper_Sheet_F"
        self.name = kwargs["name"]

        if "icon" in kwargs:
            self.replacements["{{icon}}"] = kwargs["icon"]

        self.description_handle = self.loca_aggregator.add_entry_and_return_handle(
            text=kwargs["description"],
            comment=kwargs["description"],
        )
        self.replacements["{{descriptionHandle}}"] = self.description_handle

    def get_comment(self):
        return self.name


class BookRTKeywords(ItemRTKeywords):
    book_id: Required[str]


class BookRT(PageRT):
    """
    Root template for books
    """

    def __init__(self, **kwargs: Unpack[BookRTKeywords]):
        super().__init__(**kwargs)
        self.template_filename = f"{self.base_path}rt_object_book.xml"
        self.replacements["{{bookId}}"] = kwargs["book_id"]

        self.description_handle = self.loca_aggregator.add_entry_and_return_handle(
            text=kwargs["description"],
            comment=kwargs["description"],
        )
        self.replacements["{{descriptionHandle}}"] = self.description_handle


class ScrollRTKeywords(ItemRTKeywords):
    scrollSpellName: Required[str]


class ScrollRT(RootTemplate):
    """
    Root template for scrolls
    """

    def __init__(self, **kwargs: Unpack[ScrollRTKeywords]):
        super().__init__(**kwargs)
        self.template_filename = f"{self.base_path}rt_object_scroll.xml"
        self.replacements["{{scrollSpellName}}"] = kwargs["scrollSpellName"]

        self.description_handle = self.loca_aggregator.add_entry_and_return_handle(
            text=kwargs["description"],
            comment=kwargs["description"],
        )
        self.replacements["{{descriptionHandle}}"] = self.description_handle
