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
        self.replacements = {
            "{{name}}": kwargs["name"],
            "{{displayName}}": kwargs["displayName"],
            "{{mapKey}}": uuid4(),
            "{{statsName}}": kwargs["statsName"],
        }
        self.template_fetcher = kwargs["template_fetcher"]

    def _get_template_text(self):
        """
        Fetches template from filesystem
        """
        return self.template_fetcher.get_template_text(self.filename)

    def get_tpl_with_replacements(self):
        """
        Replaces using map
        """
        tpl_text = self._get_template_text()
        replacer = TemplateVariableReplacer()
        return replacer.replace_placeholders(tpl_text, self.replacements)


class CompanionRT(RootTemplate):
    """
    Root template with companion settings
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filename = f"{self.base_path}rt_companion.xml"
        # Companion specific replacements below
        self.replacements["{{archetypeName}}"] = "melee_smart"
        self.replacements["{{parentTemplateId}}"] = kwargs["parentTemplateId"]
        self.replacements["{{equipmentSetName}}"] = kwargs["equipmentSetName"]
        self.replacements["{{title}}"] = kwargs["title"]
        tag_list = ""
        if "tagList" in kwargs:
            tag_list = kwargs["tagList"]
        self.replacements["{{tagList}}"] = tag_list


class PageRT(RootTemplate):
    """
    Root template for objects like books and scrolls
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filename = f"{self.base_path}rt_page.xml"
        self.replacements["{{icon}}"] = kwargs["icon"]
        self.replacements["{{description}}"] = kwargs["description"]


class BookRT(PageRT):
    """
    Root template for books
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filename = f"{self.base_path}rt_book.xml"
        self.replacements["{{bookId}}"] = kwargs["bookId"]
