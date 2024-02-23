from companiongenerator.item_combo import ItemCombo
from companiongenerator.item_combo_aggregator import ItemComboAggregator


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
