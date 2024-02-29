from companiongenerator.constants import ARCH_MELEE_SMART_TPL_ID

from tests.rt_test_helper import (
    get_book_rt,
    get_companion_rt,
    get_page_rt,
    get_scroll_rt,
)
from tests.template_validity_helper import (
    assert_template_validity,
    verify_xml_values,
)


def test_generate_companion_rt() -> None:
    """
    Tests generation of companion root template
    """
    stats_name = "LC_Legendary_Muffin"
    parent_template_id = ARCH_MELEE_SMART_TPL_ID
    equipment_set_name = "LC_EQP_Legendary_Muffin"
    icon = "LC_icon_name"
    companion_rt = get_companion_rt()
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
    stats_name = "OBJ_LC_Page_1"
    icon_name = "book_icon_name"
    page_rt = get_page_rt()
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
    stats_name = "OBJ_LC_BOOK_1"
    icon_name = "Item_BOOK_GEN_Book_C"
    book_rt = get_book_rt()
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
    stats_name = "OBJ_LC_SCROLL"
    scroll_rt = get_scroll_rt()
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
