from companiongenerator.item_combo_parser import ItemComboParser
from companiongenerator.logger import logger


def test_item_combo_parser():
    parser = ItemComboParser()
    combo_entries = parser.get_combo_entries_from_file_contents()
    combo_names = combo_entries["combo_names"]
    combo_result_names = combo_entries["combo_result_names"]

    assert combo_names, "Empty combo names"
    assert combo_result_names, "Empty combo result names"

    # Test that each combo entry has an accompanying combo result
    assert len(combo_names) == len(combo_result_names), "Unbalanced combo entries!"

    for combo_name in combo_names:
        assert (
            f"{combo_name}_1" in combo_result_names
        ), f"Missing combo result for {combo_name}!"

    if parser.is_file_empty:
        logger.error("Empty combo file")

    assert not parser.is_file_empty and len(combo_names) > 0, "Failed to parse combos"

    for combo_name in combo_names:
        assert "new ItemCombination" not in combo_name
        assert '"' not in combo_name


def test_pages_in_combo_file():
    """
    Verifies all pages are present in the combo file
    """
    parser = ItemComboParser()
    combo_entries = parser.get_combo_entries_from_file_contents()
    if len(combo_entries["combo_names"]) > 0:
        pages = combo_entries["pages"]

        # Check we have at least one two pages
        assert len(pages) >= 2, "No pages"

        # Check if first entry is in pages
        for combo_name in combo_entries["combo_names"]:
            assert combo_name in pages
    else:
        logger.error("No combo names in file")
