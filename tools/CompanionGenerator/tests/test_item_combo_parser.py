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
