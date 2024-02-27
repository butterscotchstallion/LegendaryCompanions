from companiongenerator.item_combo import ItemCombo
from companiongenerator.item_combo_aggregator import ItemComboAggregator
from companiongenerator.item_combo_parser import ItemComboParser
from companiongenerator.logger import logger


def test_combo_aggregation():
    combo_aggregator = ItemComboAggregator()
    combo = ItemCombo(
        combo_name="Test_Combo",
        object_one_name="Page 1",
        object_two_name="Page 2",
        combo_result_item_name="Combo_Result",
    )
    combo_aggregator.add_entry(combo)
    combo_aggregator.add_entry(combo)

    assert len(combo_aggregator.entries) == 1, "Duplicate entry added :("


def test_load_from_file():
    """
    Tests loading combo entries from file
    and verifies the resulting entries
    """
    parser = ItemComboParser()
    combo_file_contents: str = parser.get_file_contents()

    if len(combo_file_contents) > 0:
        combo_entries = parser.get_combo_entries_from_file_contents(combo_file_contents)
        file_combo_names_len: int = len(combo_entries["combo_names"])
        file_combo_result_names_len: int = len(combo_entries["combo_result_names"])
        assert file_combo_names_len == file_combo_result_names_len

        # Add each entry to the aggregator
        combo_aggregator = ItemComboAggregator()
        entries = combo_aggregator.load_entries_from_file()

        assert len(entries) > 0
    else:
        logger.info("Empty combo file")
