from companiongenerator.item_combos_parser import ItemCombosParser
from companiongenerator.logger import logger


def test_item_combos_parser():
    parser = ItemCombosParser()
    combo_names = parser.get_combo_names_from_file()

    if parser.is_file_empty:
        logger.error("Empty combo file")

    assert not parser.is_file_empty and len(combo_names) > 0, "Failed to parse combos"

    for combo_name in combo_names:
        assert "new ItemCombination" not in combo_name
        assert '"' not in combo_name
