from companiongenerator.localization_entry import LocalizationEntry
from companiongenerator.localization_manager import (
    LocalizationManager,
)
from companiongenerator.root_template import CompanionRT, PageRT
from companiongenerator.template_fetcher import TemplateFetcher

from tests.template_validity_helper import is_valid_handle_uuid


def test_add_entry() -> None:
    loca_mgr = LocalizationManager()

    # TODO: test retrieval of entries here
    # Test that entries remain after multiple instantiations

    # Companion
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
        template_fetcher=TemplateFetcher(),
        localization_manager=loca_mgr,
    )
    assert is_valid_handle_uuid(companion_rt.display_name_handle)
    assert is_valid_handle_uuid(companion_rt.title_handle)

    # Page
    pg_display_name = "Page 1"
    pg_description = "A tattered page"
    pg_stats_name = "OBJ_LC_Page_1"
    pg_icon_name = "book_icon_name"
    page_rt = PageRT(
        displayName=pg_display_name,
        description=pg_description,
        statsName=pg_stats_name,
        name=pg_stats_name,
        icon=pg_icon_name,
        template_fetcher=TemplateFetcher(),
        localization_manager=loca_mgr,
    )
    assert is_valid_handle_uuid(page_rt.display_name_handle)
    assert is_valid_handle_uuid(page_rt.description_handle)

    """
    Verify localization manager values
    There should be four entries, one for each localized
    value
    """
    assert len(loca_mgr.entries) == 4

    entry_map: dict[str, LocalizationEntry] = {}
    for entry in loca_mgr.entries:
        assert not is_valid_handle_uuid(entry.text), "Text should not be a handle"
        entry_map[entry.handle] = entry

    # Companion values
    assert companion_rt.display_name_handle in entry_map
    assert entry_map[companion_rt.display_name_handle].text == display_name
    assert entry_map[companion_rt.title_handle].text == title

    # Page values
    assert page_rt.display_name_handle in entry_map
    assert entry_map[page_rt.display_name_handle].text == pg_display_name
    assert entry_map[page_rt.description_handle].text == pg_description

    # Test writing entries
