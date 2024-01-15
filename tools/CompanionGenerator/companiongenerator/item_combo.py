from companiongenerator.template_replacer_base import (
    TemplateReplacerBase,
)


class ItemCombo(TemplateReplacerBase):
    """
    Handles combinations of items such as pages
    """

    def __init__(self, **kwargs):
        self.template_fetcher = kwargs["template_fetcher"]
        self.filename = "ItemCombos.txt"
        self.combo_name = kwargs["combo_name"]
        self.object_one_name = kwargs["object_one_name"]
        self.object_two_name = kwargs["object_two_name"]
        self.combo_result_item_name = kwargs["combo_result_item_name"]
        self.replacements = {
            "{{comboName}}": self.combo_name,
            "{{objectOneName}}": self.object_one_name,
            "{{objectTwoName}}": self.object_two_name,
            "{{comboResultItemName}}": self.combo_result_item_name,
        }