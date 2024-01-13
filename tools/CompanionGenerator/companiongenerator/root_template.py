# import logging as log

from companiongenerator.template_variable_replacer import TemplateVariableReplacer
from uuid import uuid4


class RootTemplate:
    """
    Creates XML file using template
    1. Set base path
    2. Add filename parameter
    3. Create RT template
    4. Add replacement variables
    """

    def __init__(self, **kwargs):
        self.base_path = "".join(
            [
                "../../../LegendaryCompanions/Mods/LegendaryCompanions/public/",
                "LegendaryCompanions/RootTemplates/",
            ]
        )
        tag_list = ""
        if "tagList" in kwargs:
            tag_list = kwargs["tagList"]
        self.replacements = {
            "displayName": kwargs["displayName"],
            "description": kwargs["description"],
            "mapKey": uuid4(),
            "statsName": kwargs["statsName"],
            "parentTemplateId": kwargs["parentTemplateId"],
            "tagList": tag_list,
        }
        self.template_fetcher = kwargs["template_fetcher"]

    def get_tpl_with_replacements(self):
        """
        Replaces using map
        """
        tpl_text = self.get_template_text()
        replacer = TemplateVariableReplacer()

        print(self.replacements)
        return replacer.replace(tpl_text, self.replacements)

    def get_template_text(self):
        return self.template_fetcher.get_template_text(self.filename)


class CompanionRT(RootTemplate):
    """
    Root template with companion settings
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filename = f"{self.base_path}rt_companion.xml"
        # Companion specific replacements below
        self.replacements["archetypeName"] = "melee_smart"


class PageRT(RootTemplate):
    """
    Root template for objects like books and scrolls
    """

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.filename = f"{self.base_path}rt_page.xml"
        # Book page specific replacements below
