import xml.etree.ElementTree as ET

from companiongenerator import logger
from companiongenerator.constants import MOD_FILENAMES
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
    num_skipped: int = 0
    for node_child in node_children:
        # Don't try to parse comments
        if node_child.tag is ET.Comment:
            continue

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
                    logger.info(
                        f"Duplicate entry found: \"{attr.attrib['value']}\"! Skipping"
                    )
                    num_skipped = num_skipped + 1
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

    if num_skipped > 0:
        logger.debug(f"Skipped {num_skipped} RT entries")
        return True

    return False


def test_parse_skill_list():
    """
    Parses RT template and gets skill list children,
    then adds a skill and verifies it was added
    """
    parser = RootTemplateParser()

    # Get companion node XML
    companion_rt = get_companion_rt()
    companion_xml = companion_rt.get_tpl_with_replacements()

    # Parse it into an element
    root_companion_node = ET.fromstring(companion_xml)
    skill_list_node = parser.get_skill_list_node(root_companion_node)

    assert skill_list_node is not None
    # The node should have a children tag inside it
    assert skill_list_node.find("children") is not None


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

    new_nodes = set(
        [
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
            RootTemplateNodeEntry(
                comment=scroll_rt.get_comment(),
                root_template_xml=scroll_xml,
                name=scroll_rt.name,
            ),
        ]
    )

    # Parse XML and verify children tag exists
    xml_with_new_nodes = parser.get_updated_children(
        MOD_FILENAMES["root_template_merged"],
        new_nodes,
    )
    assert (
        xml_with_new_nodes is not None
    ), "Failed to parse children from XML file contents"

    if xml_with_new_nodes:
        # Parse XML and verify children
        root = ET.fromstring(xml_with_new_nodes)
        children_el = parser.get_templates_children(root)
        assert children_el is not None

        """
        Verify XML by checking each root template against
        the parsed XML
        """
        names_list: list[str] = sorted(parser.get_names_from_children(children_el))
        names_set: set[str] = set(names_list)
        names_list_len = len(names_list)
        names_set_len = len(names_set)

        for name in names_list:
            if name not in names_set:
                assert False, f"Duplicate name found: {name}"

        assert names_list_len == names_set_len
