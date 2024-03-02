from companiongenerator.constants import ARCH_MELEE_SMART_TPL_ID
from companiongenerator.localization_aggregator import (
    LocalizationAggregator,
)
from companiongenerator.localization_entry import LocalizationEntry
from companiongenerator.root_template import CompanionRT, PageRT

from tests.template_validity_helper import is_valid_handle_uuid


def test_add_entry() -> None:
    loca_aggregator = LocalizationAggregator()

    # TODO: test retrieval of entries here
    # Test that entries remain after multiple instantiations

    # Companion
    display_name = "Chip Chocolate"
    title = "Legendary Muffin"
    stats_name = "LC_Legendary_Muffin"
    parent_template_id = ARCH_MELEE_SMART_TPL_ID
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
        localization_aggregator=loca_aggregator,
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
        localization_aggregator=loca_aggregator,
    )
    assert is_valid_handle_uuid(page_rt.display_name_handle)
    assert is_valid_handle_uuid(page_rt.description_handle)

    """
    Verify localization manager values
    There should be four entries, one for each localized
    value
    """
    assert len(loca_aggregator.entries) == 4

    entry_map: dict[str, LocalizationEntry] = {}
    entries = loca_aggregator.entries
    for entry in entries:
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


def test_deduplication():
    """
    Ensure that duplicate text entries aren't added
    """
    loca_aggregator = LocalizationAggregator()
    text = "Chill: I ain't got none, but if I'm gonna be a mess I'm a hot one"
    loca_aggregator.add_entry_and_return_handle(text=text)
    loca_aggregator.add_entry_and_return_handle(text=text)
    assert len(loca_aggregator.entries) == 1, "Failed to de-duplicate loca entries"
