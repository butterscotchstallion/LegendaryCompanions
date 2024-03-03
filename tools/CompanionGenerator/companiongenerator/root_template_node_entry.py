from typing import Required, TypedDict, Unpack


class RootTemplateNodeEntryKeywords(TypedDict):
    name: Required[str]
    comment: Required[str]
    root_template_xml: Required[str]


class RootTemplateNodeEntry:
    """
    Each entry contains the root template instance
    along with a comment
    """

    def __init__(self, **kwargs: Unpack[RootTemplateNodeEntryKeywords]):
        self.comment: str = kwargs["comment"]
        self.root_template_xml: str = kwargs["root_template_xml"]
        # We need to know the name of each RT to avoid adding duplicates
        self.name = kwargs["name"]
