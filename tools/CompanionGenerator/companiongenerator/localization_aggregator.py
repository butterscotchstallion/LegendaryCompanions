from typing import Literal

from companiongenerator.file_handler import FileHandler
from companiongenerator.localization_entry import (
    LocalizationEntry,
)
from companiongenerator.logger import logger


class LocalizationAggregator:
    """
    Handles localization entries by adding entries each time
    a handle is created. As part of the file generation process,
    all entries will be written to the localization file.
    """

    entries: list[LocalizationEntry] = []

    def __init__(self, **kwargs):
        self.entries = []
        self.is_dry_run = True

        if "is_dry_run" in kwargs:
            self.is_dry_run = kwargs["is_dry_run"]

    def entry_with_text_exists(
        self, entry_text: str
    ) -> LocalizationEntry | Literal[False]:
        for entry in self.entries:
            if entry.text == entry_text:
                return entry
        return False

    def entry_with_handle_exists(
        self, entry_handle: str
    ) -> LocalizationEntry | Literal[False]:
        for entry in self.entries:
            if entry.handle == entry_handle:
                return entry
        return False

    def add_entry_and_return_handle(self, **kwargs) -> str:
        existing_entry = self.entry_with_text_exists(kwargs["text"])

        if existing_entry:
            return existing_entry.handle
        else:
            entry = LocalizationEntry(**kwargs)
            self.entries.append(entry)
            return entry.handle

    def write_entries(self, file_path: str) -> bool:
        """
        Writes entries to file or edits existing localization file
        """
        if len(self.entries) > 0:
            xml_entries: list[str] = [entry.to_xml() for entry in self.entries]
            handler = FileHandler(is_dry_run=self.is_dry_run)
            return handler.write_list_to_file(file_path, xml_entries)
        else:
            logger.error("No localization entries. This is probably an error.")
            return False
