from companiongenerator.localization_aggregator import LocalizationAggregator
from companiongenerator.root_template import BookRT, CompanionRT, PageRT, ScrollRT
from companiongenerator.root_template_aggregator import RootTemplateAggregator
from companiongenerator.template_fetcher import TemplateFetcher


def get_page_rt() -> PageRT:
    display_name = "Page 1"
    description = "A tattered page"
    stats_name = "OBJ_LC_Page_1"
    icon_name = "book_icon_name"
    return PageRT(
        displayName=display_name,
        description=description,
        statsName=stats_name,
        name=stats_name,
        icon=icon_name,
        template_fetcher=TemplateFetcher(),
        localization_aggregator=LocalizationAggregator(),
        root_template_aggregator=RootTemplateAggregator(is_dry_run=False),
    )


def get_book_rt() -> BookRT:
    display_name = "The Legend of Chip Chocolate"
    description = "A legendary muffin wizard"
    stats_name = "OBJ_LC_BOOK_1"
    icon_name = "Item_BOOK_GEN_Book_C"
    book_id = "LC_BOOK_Legendary_Muffin"
    return BookRT(
        displayName=display_name,
        description=description,
        statsName=stats_name,
        name=stats_name,
        icon=icon_name,
        bookId=book_id,
        template_fetcher=TemplateFetcher(),
        localization_aggregator=LocalizationAggregator(),
        root_template_aggregator=RootTemplateAggregator(is_dry_run=False),
    )


def get_companion_rt() -> CompanionRT:
    fetcher = TemplateFetcher()
    display_name = "Chip Chocolate"
    title = "Legendary Muffin"
    stats_name = "LC_Legendary_Muffin"
    parent_template_id = "1234"
    equipment_set_name = "LC_EQP_Legendary_Muffin"
    icon = "LC_icon_name"
    return CompanionRT(
        name=stats_name,
        displayName=display_name,
        statsName=stats_name,
        parentTemplateId=parent_template_id,
        equipmentSetName=equipment_set_name,
        title=title,
        icon=icon,
        template_fetcher=fetcher,
        localization_aggregator=LocalizationAggregator(),
        root_template_aggregator=RootTemplateAggregator(is_dry_run=False),
    )


def get_scroll_rt() -> ScrollRT:
    display_name = "Scroll of Summon Chip Chocolate"
    description = "A tattered scroll, glowing with power"
    stats_name = "OBJ_LC_SCROLL"
    scroll_spell_name = "LC_Summon_Legendary_Muffin"
    return ScrollRT(
        displayName=display_name,
        description=description,
        statsName=stats_name,
        name=stats_name,
        scrollSpellName=scroll_spell_name,
        template_fetcher=TemplateFetcher(),
        localization_aggregator=LocalizationAggregator(),
        root_template_aggregator=RootTemplateAggregator(is_dry_run=False),
    )
