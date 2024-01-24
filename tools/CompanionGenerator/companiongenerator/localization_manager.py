import logging as log

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
        self.is_dry_run = True

        if "is_dry_run" in kwargs:
            self.is_dry_run = kwargs["is_dry_run"]

    def add_entry_and_return_handle(self, **kwargs) -> str:
        entry = LocalizationEntry(**kwargs)
        self.entries.append(entry)
        return entry.handle

    def write_entries(self):
        """
        Writes entries to file or edits existing localization file
        """
        if len(self.entries):
            for entry in self.entries:
                log.info(f"Writing localization entry '{entry.handle}")

                if not self.is_dry_run:
                    # add writing here
                    pass
        else:
            log.error("No localization entries. This is probably an error.")
