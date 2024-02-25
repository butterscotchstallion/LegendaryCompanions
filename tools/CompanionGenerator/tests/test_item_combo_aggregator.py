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
    TODO: test loading combos from file and the name stuff
    """
    parser = ItemComboParser()
    combo_file_contents: str = parser.get_file_contents()

    if len(combo_file_contents) > 0:
        combo_entries = parser.get_combo_entries_from_file_contents(combo_file_contents)

        assert len(combo_entries["combo_names"]) == len(
            combo_entries["combo_result_names"]
        )
    else:
        logger.info("Empty combo file")
