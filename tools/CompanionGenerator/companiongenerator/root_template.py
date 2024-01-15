from companiongenerator.template_replacer_base import TemplateReplacerBase
from uuid import uuid4


class RootTemplate(TemplateReplacerBase):
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


class CompanionRT(RootTemplate):
    """
    Root template with companion settings
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filename = f"{self.base_path}rt_companion.xml"
        # Companion specific replacements below
        archetype = "melee_smart"
        if "archetypeName" in kwargs:
            archetype = kwargs["archetypeName"]
        self.replacements["{{archetypeName}}"] = archetype
        self.replacements["{{parentTemplateId}}"] = kwargs["parentTemplateId"]
        self.replacements["{{equipmentSetName}}"] = kwargs["equipmentSetName"]
        title = ""
        if "title" in kwargs:
            title = kwargs["title"]
        self.replacements["{{title}}"] = title

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
