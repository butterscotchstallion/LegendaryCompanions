import io
import itertools as IT
import os
import xml.etree.ElementTree as ET

from companiongenerator.logger import logger
from companiongenerator.root_template_node_entry import RootTemplateNodeEntry

StringIO = io.StringIO


class RootTemplateParser:
    """
    Handles parsing XML in root templates
    """

    def get_error_message(self, content: str, err: ET.ParseError):
        lineno, column = err.position
        line = next(IT.islice(StringIO(content), lineno))
        caret = "{:=>{}}".format("^", column)
        return "{}\n{}\n{}".format(err, line, caret)

    def get_tag_with_id_from_root(
        self, root, tag_name: str, tag_id: str
    ) -> ET.Element | None:
        for tag in root.findall(tag_name):
            tree_tag_id = tag.attrib.get("id")
            if tree_tag_id is not None and tree_tag_id == tag_id:
                return tag

    def get_templates_children(self, root) -> ET.Element | None:
        # Get region#Templates
        templates_region = self.get_tag_with_id_from_root(root, "region", "Templates")
        if templates_region is not None:
            node = self.get_tag_with_id_from_root(templates_region, "node", "Templates")
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

            tree = ET.parse(filename)
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
                                    logger.info(f"Name value is: {name_value}")
                                    existing_names.append(name_value)
                        else:
                            logger.error(
                                "Unexpected XML format: no attributes found in node tag!"
                            )

                    logger.info(f"Existing names: {existing_names}")

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
                err_msg = self.get_error_message(new_node.root_template_xml, err)
            else:
                err_msg = "unknown"
            logger.error(f"Failed to parse XML: {err_msg}")
