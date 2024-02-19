import os
import xml.etree.ElementTree as ET

from companiongenerator.localization_entry import LocalizationEntry
from companiongenerator.logger import logger
from companiongenerator.xml_utils import (
    get_comment_preserving_parser,
    get_error_message,
    get_text_from_entries,
)


class LocalizationParser:
    """Handles parses and modifying localization XML"""

    tree: ET.ElementTree | None
    filename: str
    entries_added: int

    def __init__(self):
        self.filename = ""
        self.entries_added = 0
        self.tree = None

    def get_content_list(self, root: ET.Element) -> list[ET.Element]:
        return root.findall("content")

    def append_entries(
        self, filename: str, entries: set[LocalizationEntry]
    ) -> ET.Element | None:
        # Appends localization entries and returns updated content list
        new_node = ""
        try:
            if not os.path.exists(filename):
                raise FileNotFoundError()

            self.filename = filename

            parser = get_comment_preserving_parser()
            self.tree = ET.parse(filename, parser)
            # Root is contentList
            content_list = self.tree.getroot()
            content_entries = self.get_content_list(content_list)
            """
            Example structure
            <contentList>
                <content contentuid="h78e6ba11gea6ag4627g983fg592126b8f047" version="1">
                    Legendary Companion
                </content>
            </contentList>
            """
            if content_entries is not None:
                content_entries_set = set(content_entries)

                # Build list of text so we don't add duplicates
                content_text_list: list[str] = get_text_from_entries(
                    content_entries_set
                )

                logger.info(
                    f"Localization content list has {len(content_text_list)} entries"
                )

                # Append new entries
                for loca_entry in entries:
                    if loca_entry.text not in content_text_list:
                        loca_entry_element = ET.fromstring(
                            loca_entry.get_tpl_with_replacements()
                        )
                        # Append new nodes to content list (root)
                        if loca_entry.comment:
                            content_list.append(ET.Comment(loca_entry.comment))
                        content_list.append(loca_entry_element)
                        self.entries_added = self.entries_added + 1

                if self.entries_added > 0:
                    ET.indent(content_list, "\t")

                return content_list
            else:
                logger.error("Failed to find content list loca XML tree")
        except ET.ParseError as err:
            logger.error(f"Error parsing loca file: {get_error_message(new_node, err)}")

    def write_tree(self):
        if self.tree and self.entries_added > 0:
            self.tree.write(self.filename, "unicode", True)
            logger.info(f"Wrote {self.entries_added} localization entries")
