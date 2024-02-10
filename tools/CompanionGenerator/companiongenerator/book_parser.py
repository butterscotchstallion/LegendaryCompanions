import os
import xml.etree.ElementTree as ET
from pathlib import Path

from companiongenerator.book_loca_entry import BookLocaEntry
from companiongenerator.logger import logger
from companiongenerator.xml_utils import (
    get_comment_preserving_parser,
    get_error_message,
    get_tag_with_id_from_root,
)


class BookParser:
    """Handles parsing and writing of book entries"""

    def __init__(self):
        self.filename: str = ""
        self.tree: ET.ElementTree

    def get_attrs_from_children(self, children_node: ET.Element):
        book_nodes = children_node.findall("node")
        attrs = []
        if book_nodes is not None:
            for book_node in book_nodes:
                attrs.append(book_node.findall("attribute"))
            return attrs

    def get_book_uuids(self, children_node: ET.Element) -> list[str]:
        """Get book UUIDs from children node element

        Args:
            children_node (ET.Element): This contains book nodes

        Returns:
            list[str]: book uuids
        """
        book_uuids: list[str] = []
        all_book_attrs = self.get_attrs_from_children(children_node)
        logger.info(all_book_attrs)
        if all_book_attrs:
            for book_attr_set in all_book_attrs:
                for attr in book_attr_set:
                    if attr.attrib["id"] == "UUID":
                        book_uuids.append(attr.attrib["value"])
        return book_uuids

    def get_children_node_from_root(self, root: ET.Element) -> ET.Element | None:
        """Gets the children node to which we will
        append new book nodes

        Args:
            root (ET.Element): root element
        """
        region = get_tag_with_id_from_root(root, "region", "TranslatedStringKeys")
        if region is not None:
            region_node = get_tag_with_id_from_root(
                region, "node", "TranslatedStringKeys"
            )
            if region_node is not None:
                region_node_children = region_node.find("children")
                if region_node_children is not None:
                    """
                    <children>
                        <node id="TranslatedStringKey">...</node>
                    </children>
                    """
                    return region_node_children

    def update_book_file(self, filename: str, books: list[BookLocaEntry]):
        """
        Parses book file and appends new books

        Args:
            filename (str): _description_
        """
        new_node = ""
        try:
            if not os.path.exists(filename):
                raise FileNotFoundError()

            if len(books) == 0:
                logger.error("No books provided. This is probably an error")

            logger.debug(f"Parsing {filename}")

            self.filename = filename
            parser = get_comment_preserving_parser()
            self.tree = ET.parse(filename, parser)
            root = self.tree.getroot()
            """
            Example structure
            <save>
                <version major="4" minor="0" revision="9" build="322" />
                <region id="TranslatedStringKeys">
                    <node id="TranslatedStringKeys">
                        <children>
                            <node id="TranslatedStringKey">
                                <attribute id="Content" type="TranslatedString" handle="{{content_handle}}" version="1" />
                                <attribute id="UUID" type="FixedString" value="{{name}}" />
                                <attribute id="Speaker" type="FixedString" value="4a405fba-3000-4c63-97e5-a8001ebb883c" />
                                <attribute id="ExtraData" type="LSString" value="" />
                                <attribute id="Stub" type="bool" value="True" />
                                <attribute id="UnknownDescription" type="TranslatedString" handle="{{unknown_description_handle}}" version="1" />
                            </node>
                        </children>
                    </node>
                </region>
            </save>
            """
            children = self.get_children_node_from_root(root)

            if children is not None:
                # Build list of book names so we don't add duplicates
                # Also, an empty list is valid when it's a new template
                book_name_list = self.get_book_uuids(children)

                logger.info(f"Book names: {",".join(book_name_list)}")

                # Append new books
                books_added = 0
                for book_entry in books:
                    # I called it name for some reason but here it's called a UUID
                    if book_entry.name not in book_name_list:
                        book_element = ET.fromstring(
                            book_entry.get_tpl_with_replacements()
                        )
                        # children.append(ET.Comment(loca_entry.comment))
                        children.append(book_element)
                        books_added = books_added + 1

                logger.info(f"{books_added} books added to {Path(self.filename)}")

                if books_added > 0:
                    ET.indent(root, "\t")

                return children
            else:
                logger.error("Failed to find book XML tree")
        except ET.ParseError as err:
            logger.error(f"Error parsing book file: {get_error_message(new_node, err)}")

    def write_tree(self):
        self.tree.write(self.filename, "unicode", True)
