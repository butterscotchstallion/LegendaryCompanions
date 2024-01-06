class RootTemplate:
    """
    Creates XML file using template
    1. Set base path
    2. Add filename parameter
    3. Create RT template
    4. Add replacement variables
    """

    def __init__(self, **kwargs):
        self.base_path = [
            "../../../LegendaryCompanions/Mods/LegendaryCompanions/public/",
            "LegendaryCompanions/RootTemplates/",
        ].join("")
        self.replacements = {}
        self.template_fetcher = kwargs["template_fetcher"]

    def get_tpl_with_replacements():
        """
        Replaces using map
        """
        pass


class CompanionRT(RootTemplate):
    """
    Root template with companion settings
    """

    def __init__(self):
        super().__init__()
        self.filename = f"{self.base_path}rt_companion.xml"

    def get_template_text(self):
        return self.template_fetcher.get_template_text(self.filename)


class ObjectRT(RootTemplate):
    """
    Root template for objects like books and scrolls
    """

    def __init__(self):
        super().__init__()
        # do books need to be different than scrolls?
        self.filename = f"{self.base_path}rt_book.xml"

    def get_template_text(self):
        return self.template_fetcher.get_template_text(self.filename)
