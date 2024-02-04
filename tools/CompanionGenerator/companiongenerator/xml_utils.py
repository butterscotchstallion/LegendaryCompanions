import io
import itertools as IT
import xml.etree.ElementTree as ET
from xml.etree import ElementTree

StringIO = io.StringIO


def get_comment_preserving_parser():
    return ElementTree.XMLParser(target=ElementTree.TreeBuilder(insert_comments=True))


def get_tag_with_id_from_root(
    root: ET.Element, tag_name: str, tag_id: str
) -> ET.Element | None:
    for tag in root.findall(tag_name):
        tree_tag_id = tag.attrib.get("id")
        if tree_tag_id is not None and tree_tag_id == tag_id:
            return tag


def get_error_message(content: str, err: ET.ParseError):
    lineno, column = err.position
    line = next(IT.islice(StringIO(content), lineno))
    caret = "{:=>{}}".format("^", column)
    return "{}\n{}\n{}".format(err, line, caret)
