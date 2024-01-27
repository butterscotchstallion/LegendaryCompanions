import logging as log

from companiongenerator.file_handler import FileHandler
from companiongenerator.localization_entry import (
    LocalizationEntry,
)


class LocalizationManager:
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

    def add_entry_and_return_handle(self, **kwargs) -> str:
        entry = LocalizationEntry(**kwargs)
        self.entries.append(entry)
        return entry.handle

    def write_entries(self, file_path: str):
        """
        Writes entries to file or edits existing localization file
        """
        if len(self.entries) > 0:
            handler = FileHandler(is_dry_run=self.is_dry_run)
            handler.write_list_to_file(file_path, self.entries)
        else:
            log.error("No localization entries. This is probably an error.")
