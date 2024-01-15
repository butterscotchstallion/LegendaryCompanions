from companiongenerator.item_combo import ItemCombo
from companiongenerator.template_fetcher import TemplateFetcher
from tests.template_validity_helper import assert_template_validity


def mock_combo_template_text():
    return """
        // {{comboName}}
        new ItemCombination "{{comboName}}"
                data "Type 1" "Object"
                data "Object 1" "{{objectOneName}}"
                data "Combine 1" "Base"
                data "Transform 1" "Transform"

                data "Type 2" "Object"
                data "Object 2" "{{objectTwoName}}"
                data "Combine 2" "Base"
                data "Transform 2" "Consume"

        new ItemCombinationResult "{{comboName}}_1"
                data "ResultAmount 1" "1"
                data "Result 1" "{{comboResultItemName}}"
                data "PreviewStatsID" "{{comboResultItemName}}"
                data "PreviewIcon" "Item_BOOK_GEN_Book_B"
    """


def test_item_combos(mocker):
    """
    Test generation of item combinations
    """
    fetcher = TemplateFetcher()
    mocker.patch.object(
        fetcher, "get_template_text", return_value=mock_combo_template_text()
    )
    combo_name = "LC_Book_Pages_Combo"
    object_one_name = "page_1"
    object_two_name = "page_2"
    combo_result_item_name = "LC_Book_of_Revelations"
    combo = ItemCombo(
        combo_name=combo_name,
        object_one_name=object_one_name,
        object_two_name=object_two_name,
        combo_result_item_name=combo_result_item_name,
        template_fetcher=fetcher,
    )
    value_line_map = {
        0: combo_name,
        1: combo_name,
        3: object_one_name,
        7: object_two_name,
        10: combo_result_item_name,
    }
    combo_text_with_replacements = combo.get_tpl_with_replacements()

    assert_template_validity(combo_text_with_replacements)

    """
    Iterate lines and check the line->value map to ensure we have the values
    we expect
    """
    combo_template_lines = combo_text_with_replacements.splitlines()
    line_number = 0
    for line in combo_template_lines:
        if line and line_number in value_line_map:
            assert value_line_map[line_number] in line
            line_number = line_number + 1
