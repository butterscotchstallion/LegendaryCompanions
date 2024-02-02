import xml.etree.ElementTree as ET

from companiongenerator.root_template_aggregator import RootTemplateNodeEntry
from companiongenerator.root_template_parser import RootTemplateParser

from tests.rt_test_helper import get_companion_rt, get_page_rt, get_scroll_rt


def test_parse_and_append():
    """
    Tests parsing XML files and appending to the
    the children tag
    """
    parser = RootTemplateParser()
    companion_rt = get_companion_rt()
    companion_xml = companion_rt.get_tpl_with_replacements()
    page_rt = get_page_rt()
    page_xml = page_rt.get_tpl_with_replacements()
    scroll_rt = get_scroll_rt()
    scroll_xml = scroll_rt.get_tpl_with_replacements()

    new_nodes = [
        RootTemplateNodeEntry(
            comment=companion_rt.get_comment(),
            root_template_xml=companion_xml,
        ),
        RootTemplateNodeEntry(
            comment=page_rt.get_comment(),
            root_template_xml=page_xml,
        ),
        RootTemplateNodeEntry(
            comment=scroll_rt.get_comment(),
            root_template_xml=scroll_xml,
        ),
    ]

    # Parse XML and verify children tag exist
    xml_with_new_nodes = parser.append_nodes_to_children(
        "./companiongenerator/templates/merged.lsx",
        new_nodes,
    )
    assert (
        xml_with_new_nodes is not None
    ), "Failed to parse children from XML file contents"

    # Parse XML and verify children
    root = ET.fromstring(xml_with_new_nodes)
    children_el = parser.get_templates_children(root)
    assert children_el is not None

    node_children = children_el.findall("node")

    assert len(node_children) == len(new_nodes), "Failed to append to children"
