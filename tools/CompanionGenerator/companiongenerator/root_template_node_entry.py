class RootTemplateNodeEntry:
    """
    Each entry contains the root template instance
    along with a comment
    """

    def __init__(self, **kwargs):
        self.comment: str = kwargs["comment"]
        self.root_template_xml: str = kwargs["root_template_xml"]
        # We need to know the name of each RT to avoid adding duplicates
        self.name = kwargs["name"]