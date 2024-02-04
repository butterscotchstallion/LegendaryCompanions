import os
import xml.etree.ElementTree as ET

from companiongenerator import logger
from companiongenerator.localization_entry import LocalizationEntry
from companiongenerator.xml_utils import (
    get_comment_preserving_parser,
    get_error_message,
)


class LocalizationParser:
    """Handles parses and modifying localization XML"""

    tree: ET.ElementTree
    loca_filename: str

    def __init__(self):
        self.original_parsed_entries: list[str] = []
        self.loca_filename = ""

    def get_content_list(self, root: ET.Element) -> list[ET.Element]:
        return root.findall("content")

    def get_text_from_entries(
        self, entries: list[ET.Element] | list[LocalizationEntry]
    ) -> list[str]:
        """Extracts text from elements and localization entries"""
        return [entry.text for entry in entries if entry.text]

    def append_entries(
        self, filename: str, entries: list[LocalizationEntry]
    ) -> ET.Element | None:
        # Appends localization entries and returns updated content list
        new_node = ""
        try:
            if not os.path.exists(filename):
                raise FileNotFoundError()

            self.loca_filename = filename

            parser = get_comment_preserving_parser()
            self.tree = ET.parse(filename, parser)
            # Root is contentList
            content_list = self.tree.getroot()

            """
            Example structure
            <contentList>
                <content contentuid="h78e6ba11gea6ag4627g983fg592126b8f047" version="1">
                    Legendary Companion
                </content>
            </contentList>
            """
            content_entries = self.get_content_list(content_list)

            if content_entries is not None:
                self.original_parsed_entries = self.get_text_from_entries(
                    content_entries
                )

                # Build list of text so we don't add duplicates
                content_text_list: list[str] = self.get_text_from_entries(
                    content_entries
                )

                # Append new entries
                entries_added = 0
                for loca_entry in entries:
                    if loca_entry.text not in content_text_list:
                        loca_entry_element = ET.fromstring(
                            loca_entry.get_tpl_with_replacements()
                        )
                        # Append new nodes to content list (root)
                        if loca_entry.comment:
                            content_list.append(ET.Comment(loca_entry.comment))
                        content_list.append(loca_entry_element)
                        entries_added = entries_added + 1

                if entries_added > 0:
                    ET.indent(content_list, "\t")
                    return content_list
            else:
                logger.error("Failed to find content list loca XML tree")
        except ET.ParseError as err:
            logger.error(f"Error parsing loca file: {get_error_message(new_node, err)}")

    def write_tree(self):
        self.tree.write(self.loca_filename, "unicode", True)
