import os
import xml.etree.ElementTree as ET

from companiongenerator.logger import logger
from companiongenerator.root_template_node_entry import RootTemplateNodeEntry
from companiongenerator.xml_utils import (
    get_comment_preserving_parser,
    get_error_message,
    get_tag_with_id_from_root,
)


class RootTemplateParser:
    """
    Handles parsing XML in root templates
    """

    def get_templates_children(self, root: ET.Element) -> ET.Element | None:
        # Get region#Templates
        templates_region = get_tag_with_id_from_root(root, "region", "Templates")
        if templates_region is not None:
            node = get_tag_with_id_from_root(templates_region, "node", "Templates")
            if node is not None:
                return node.find("children")

    def append_nodes_to_children(
        self, filename: str, nodes: list[RootTemplateNodeEntry]
    ) -> str | None:
        """
        Finds templates node, appends nodes, and returns
        updated structure.
        """
        new_node = None
        try:
            if not os.path.exists(filename):
                raise FileNotFoundError()

            parser = get_comment_preserving_parser()
            tree = ET.parse(filename, parser)
            root = tree.getroot()
            """
            <region id="Templates">
		        <node id="Templates">
			        <children>
                        <node id="GameObjects">
            """
            node_children = self.get_templates_children(root)
            if node_children is not None:
                # Build name list from children
                existing_names: list[str] = []
                all_nodes = node_children.findall("node")

                if all_nodes is not None:
                    for node_child in node_children:
                        attributes = node_child.findall("attribute")
                        if attributes and len(attributes) > 0:
                            for attribute_tag in attributes:
                                if attribute_tag.attrib["id"] == "Name":
                                    name_value = attribute_tag.attrib["value"]
                                    existing_names.append(name_value)
                        else:
                            logger.error(
                                "Unexpected XML format: no attributes found in node tag!"
                            )

                    # Iterate supplied nodes and append if not existent
                    for new_node in nodes:
                        if new_node.name not in existing_names:
                            node_children.append(ET.Comment(new_node.comment))
                            node_children.append(
                                ET.fromstring(new_node.root_template_xml)
                            )

                    ET.indent(tree, space="\t", level=0)
                    return ET.tostring(root, encoding="unicode")

        except ET.ParseError as err:
            if new_node:
                err_msg = get_error_message(new_node.root_template_xml, err)
            else:
                err_msg = "unknown"
            logger.error(f"Failed to parse XML: {err_msg}")
