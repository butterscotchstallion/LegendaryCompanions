from companiongenerator.localization_aggregator import LocalizationAggregator
from companiongenerator.root_template import BookRT, CompanionRT, PageRT, ScrollRT
from companiongenerator.root_template_aggregator import RootTemplateAggregator
from companiongenerator.template_fetcher import TemplateFetcher

from tests.template_validity_helper import (
    assert_template_validity,
    verify_xml_values,
)


def test_generate_companion_rt() -> None:
    """
    Tests generation of companion root template
    """
    fetcher = TemplateFetcher()
    display_name = "Chip Chocolate"
    title = "Legendary Muffin"
    stats_name = "LC_Legendary_Muffin"
    parent_template_id = "1234"
    equipment_set_name = "LC_EQP_Legendary_Muffin"
    icon = "LC_icon_name"
    companion_rt = CompanionRT(
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
    attribute_value_map = {
        "DisplayName": companion_rt.display_name_handle,
        "Stats": stats_name,
        "ParentTemplateId": parent_template_id,
        "Name": stats_name,
        "EquipmentSetName": equipment_set_name,
        "Title": companion_rt.title_handle,
        "Icon": icon,
        "MapKey": companion_rt.map_key,
    }
    xml_with_replacements = companion_rt.get_tpl_with_replacements()

    assert_template_validity(xml_with_replacements)
    verify_xml_values(xml_with_replacements, attribute_value_map)


def test_generate_page_xml() -> None:
    """
    Tests generation of book pages
    """
    fetcher = TemplateFetcher()
    display_name = "Page 1"
    description = "A tattered page"
    stats_name = "OBJ_LC_Page_1"
    icon_name = "book_icon_name"
    page_rt = PageRT(
        displayName=display_name,
        description=description,
        statsName=stats_name,
        name=stats_name,
        icon=icon_name,
        template_fetcher=fetcher,
        localization_aggregator=LocalizationAggregator(),
        root_template_aggregator=RootTemplateAggregator(is_dry_run=False),
    )
    attribute_value_map = {
        "DisplayName": page_rt.display_name_handle,
        "Description": page_rt.description_handle,
        "Stats": stats_name,
        "Name": stats_name,
        "Icon": icon_name,
        "MapKey": page_rt.map_key,
    }
    xml_with_replacements = page_rt.get_tpl_with_replacements()

    assert_template_validity(xml_with_replacements)
    verify_xml_values(xml_with_replacements, attribute_value_map)


def test_generate_book_xml() -> None:
    """
    Tests generation of books
    """
    fetcher = TemplateFetcher()
    display_name = "The Legend of Chip Chocolate"
    description = "A legendary muffin wizard"
    stats_name = "OBJ_LC_BOOK_1"
    icon_name = "Item_BOOK_GEN_Book_C"
    book_id = "LC_BOOK_Legendary_Muffin"
    book_rt = BookRT(
        displayName=display_name,
        description=description,
        statsName=stats_name,
        name=stats_name,
        icon=icon_name,
        bookId=book_id,
        template_fetcher=fetcher,
        localization_aggregator=LocalizationAggregator(),
        root_template_aggregator=RootTemplateAggregator(is_dry_run=False),
    )
    attribute_value_map = {
        "DisplayName": book_rt.display_name_handle,
        "Description": book_rt.description_handle,
        "Stats": stats_name,
        "Name": stats_name,
        "Icon": icon_name,
        "MapKey": book_rt.map_key,
    }
    xml_with_replacements = book_rt.get_tpl_with_replacements()

    assert_template_validity(xml_with_replacements)
    verify_xml_values(xml_with_replacements, attribute_value_map)


def test_generate_scroll_xml() -> None:
    """
    Tests generation of scrolls
    """
    fetcher = TemplateFetcher()
    display_name = "Scroll of Summon Chip Chocolate"
    description = "A tattered scroll, glowing with power"
    stats_name = "OBJ_LC_SCROLL"
    scroll_spell_name = "LC_Summon_Legendary_Muffin"
    scroll_rt = ScrollRT(
        displayName=display_name,
        description=description,
        statsName=stats_name,
        name=stats_name,
        scrollSpellName=scroll_spell_name,
        template_fetcher=fetcher,
        localization_aggregator=LocalizationAggregator(),
        root_template_aggregator=RootTemplateAggregator(is_dry_run=False),
    )
    attribute_value_map = {
        "DisplayName": scroll_rt.display_name_handle,
        "Description": scroll_rt.description_handle,
        "Stats": stats_name,
        "Name": stats_name,
        "MapKey": scroll_rt.map_key,
    }
    xml_with_replacements = scroll_rt.get_tpl_with_replacements()

    assert_template_validity(xml_with_replacements)
    verify_xml_values(xml_with_replacements, attribute_value_map)
