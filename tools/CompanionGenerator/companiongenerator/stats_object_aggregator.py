import os
from pathlib import Path

from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.file_handler import FileHandler
from companiongenerator.logger import logger
from companiongenerator.stats_object import StatsObject
from companiongenerator.stats_parser import ParserType, StatsParser


class StatsObjectAggregator:
    def __init__(self):
        self.entries: set[StatsObject] = set([])

    def add_entry(self, stats_object: StatsObject):
        self.entries.add(stats_object)

    def append_entries(self) -> bool:
        """
        Appends all entries that do not exist already
        to the object file
        """
        success: bool = False
        parser = StatsParser(
            filename=MOD_FILENAMES["books_object_file"], parser_type=ParserType.BOOK
        )
        handle = Path(MOD_FILENAMES["books_object_file"])
        object_file_contents: str = handle.read_text()
        entry_names: set[str] = parser.get_entry_names_from_text(object_file_contents)
        append_entries: set[str] = set([])

        total_existing_entries: int = len(entry_names)

        logger.info(f"There are {total_existing_entries} entries in the object file")

        if total_existing_entries == 0:
            logger.info("There are NO existing object entries")

        """
        1. Find all entries that don't exist in the file
        2. Iterating here instead of using difference or something
        because we want the log lines telling us about what is
        a duplicate or not
        """
        for entry in self.entries:
            if entry.stats_name in entry_names:
                logger.info(f"Skipping existing entry '{entry.stats_name}'")
            else:
                logger.info(f"Adding object entry for '{entry.stats_name}'")
                append_entries.add(entry.get_tpl_with_replacements())

        # Add newline and append to file once
        append_content: str = os.linesep
        append_content += os.linesep.join(append_entries)

        total_entries_to_append: int = len(append_entries)

        if total_entries_to_append > 0:
            handler = FileHandler()
            backup_created = handler.create_backup_file(
                MOD_FILENAMES["books_object_file"]
            )

            if backup_created:
                success = handler.append_to_file(
                    MOD_FILENAMES["books_object_file"], append_content
                )
                if success:
                    logger.info(
                        f"Appended {total_entries_to_append} entries to object file"
                    )
                else:
                    logger.error("Failed to append entries to object file")
        else:
            """
            This indicates we found duplicates and there is nothing to do,
            which is not an error
            """
            success = True

        return success
