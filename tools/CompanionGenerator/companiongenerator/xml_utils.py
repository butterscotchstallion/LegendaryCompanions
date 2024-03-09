import io
import itertools as IT
import xml.etree.ElementTree as ET
from xml.etree import ElementTree

StringIO = io.StringIO


class getElementById:
    def __init__(self, tree):
        self.di = {}

        def v(node):
            i = node.attrib.get("id")
            if i is not None:
                self.di[i] = node

            for child in node:
                v(child)

        v(tree.getroot())

    def __call__(self, k):
        return self.di[k]


def get_comment_preserving_parser():
    return ElementTree.XMLParser(target=ElementTree.TreeBuilder(insert_comments=True))


def get_text_from_entries(entries: set) -> list[str]:
    """Extracts text from elements and localization entries"""
    return [entry.text for entry in entries if entry.text]


def get_tag_with_id_from_node(
    node: ET.Element, tag_name: str, tag_id: str
) -> ET.Element | None:
    for el in node.findall(tag_name):
        if el.tag == tag_name:
            tree_tag_id = el.attrib.get("id")
            if tree_tag_id is not None and tree_tag_id == tag_id:
                return el


def get_error_message(content: str, err: ET.ParseError):
    lineno, column = err.position
    line = next(IT.islice(StringIO(content), lineno))
    caret = "{:=>{}}".format("^", column)
    return "{}\n{}\n{}".format(err, line, caret)
