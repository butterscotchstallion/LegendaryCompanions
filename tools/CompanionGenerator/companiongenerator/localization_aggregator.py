from typing import Literal

from companiongenerator.localization_entry import (
    LocalizationEntry,
)


class LocalizationAggregator:
    """
    Handles localization entries by adding entries each time
    a handle is created. As part of the file generation process,
    all entries will be written to the localization file.
    """

    def __init__(self, **kwargs):
        self.entries: set[LocalizationEntry] = set([])
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
            if entry is LocalizationEntry and entry.handle == entry_handle:
                return entry
        return False

    def add_entry_and_return_handle(self, **kwargs) -> str:
        existing_entry = self.entry_with_text_exists(kwargs["text"])

        """
        NOTE: this breaks without the check
        even though we're using sets. Maybe figure
        this out later.
        """
        if existing_entry is not False:
            return existing_entry.handle
        else:
            entry = LocalizationEntry(**kwargs)
            self.entries.add(entry)
            return entry.handle
