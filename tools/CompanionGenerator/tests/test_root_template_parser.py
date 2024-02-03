import xml.etree.ElementTree as ET

from companiongenerator.root_template_aggregator import RootTemplateNodeEntry
from companiongenerator.root_template_parser import RootTemplateParser

from tests.rt_test_helper import get_companion_rt, get_page_rt, get_scroll_rt


def verify_node_children(node_children: list[ET.Element], root_template_object) -> bool:
    """
    Iterates node children and verifies one of them has the root
    template object map key which is unique

    Create list of names from RT objects, and if we find multiple
    then we know there is a duplicate and this test should fail
    """
    rt_names: list[str] = []
    for node_child in node_children:
        """
        Each node has a series of attribute tags
        """
        attrs = node_child.findall("attribute")
        for attr in attrs:
            # Get value of name attribute
            # Check if this name exists
            name_value = ""
            if attr.attrib["id"] == "Name":
                name_value = attr.attrib["value"]
                if name_value in rt_names:
                    raise RuntimeError("Duplicate entry found")
                else:
                    if name_value:
                        rt_names.append(name_value)

            # Example: <attribute id="MapKey" type="FixedString" value="{{mapKey}}" />
            is_map_key = attr.attrib["id"] == "MapKey"
            has_value = "value" in attr.attrib
            # Localization entries do not have a value
            map_key_match = (
                has_value and attr.attrib["value"] == root_template_object.map_key
            )
            if is_map_key and map_key_match:
                return True
    return False


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

    scroll_entry = RootTemplateNodeEntry(
        comment=scroll_rt.get_comment(),
        root_template_xml=scroll_xml,
        name=scroll_rt.name,
    )

    new_nodes = [
        RootTemplateNodeEntry(
            comment=companion_rt.get_comment(),
            root_template_xml=companion_xml,
            name=companion_rt.name,
        ),
        RootTemplateNodeEntry(
            comment=page_rt.get_comment(),
            root_template_xml=page_xml,
            name=page_rt.name,
        ),
        scroll_entry,
        # Intentional duplicate
        scroll_entry,
    ]

    # Parse XML and verify children tag exists
    xml_with_new_nodes = parser.append_nodes_to_children(
        "./companiongenerator/templates/merged_with_contents.lsf.lsx",
        new_nodes,
    )
    assert (
        xml_with_new_nodes is not None
    ), "Failed to parse children from XML file contents"

    # Parse XML and verify children
    root = ET.fromstring(xml_with_new_nodes)
    children_el = parser.get_templates_children(root)
    assert children_el is not None

    """
    Verify XML by checking each root template against
    the parsed XML
    """
    root_templates_to_verify = [companion_rt, page_rt, scroll_rt]
    node_children = children_el.findall("node")

    for template in root_templates_to_verify:
        assert verify_node_children(node_children, template)
