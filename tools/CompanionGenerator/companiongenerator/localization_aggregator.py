import xml.etree.ElementTree as ET
from typing import Literal, Unpack

from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.localization_entry import (
    LocalizationEntry,
    LocalizationEntryKeyWords,
)
from companiongenerator.localization_parser import LocalizationParser
from companiongenerator.logger import logger
from companiongenerator.xml_utils import get_comment_preserving_parser


class LocalizationAggregator:
    """
    Handles localization entries by adding entries each time
    a handle is created. As part of the file generation process,
    all entries will be written to the localization file.
    """

    def __init__(self):
        self.entries: set[LocalizationEntry] = set([])

    def load_localization_entries_from_file(self):
        """
        Reads existing localization file and loads entries
        into LocalizationAggregator
        """
        loca_parser = LocalizationParser()
        xml_parser = get_comment_preserving_parser()
        self.tree = ET.parse(MOD_FILENAMES["localization"], xml_parser)
        content_list = self.tree.getroot()
        content_entries = loca_parser.get_content_list(content_list)

        if len(content_entries) > 0:
            loca_entries_added = 0
            for entry in content_entries:
                if "contentuid" in entry.attrib and entry.text:
                    loca_entries_added = loca_entries_added + 1
                    self.add_entry_and_return_handle(
                        text=entry.text,
                        handle=entry.attrib["contentuid"],
                        comment=entry.text,
                    )
            logger.info(
                f"LocalizationAggregator: added {loca_entries_added} existing localization entries"
            )
        else:
            logger.info("No existing localization to load")

    def set_entries(self, entries: set[LocalizationEntry]):
        """
        Sets initial entries from localization file
        """
        logger.info(f"Added {len(entries)} from localization file")
        self.entries = entries

    def entry_with_text_exists(self, entry_text: str) -> LocalizationEntry | None:
        for entry in self.entries:
            if entry.text == entry_text:
                return entry

    def entry_with_handle_exists(
        self, entry_handle: str
    ) -> LocalizationEntry | Literal[False]:
        for entry in self.entries:
            if entry.handle == entry_handle:
                return entry
        return False

    def add_entry_and_return_handle(
        self, **kwargs: Unpack[LocalizationEntryKeyWords]
    ) -> str:
        existing_entry = self.entry_with_text_exists(kwargs["text"])

        """
        NOTE: this breaks without the check
        even though we're using sets. Maybe figure
        this out later.
        """
        if existing_entry is not None:
            return existing_entry.handle
        else:
            entry = LocalizationEntry(**kwargs)
            self.entries.add(entry)
            return entry.handle
