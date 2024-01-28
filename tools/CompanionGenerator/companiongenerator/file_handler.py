import os
from collections.abc import Iterable

from companiongenerator.logger import logger


class FileHandler:
    """
    Handles file operations
    """

    def __init__(self, **kwargs):
        self.is_dry_run = True

        if "is_dry_run" in kwargs:
            self.is_dry_run = kwargs["is_dry_run"]

    def write_list_to_file(self, file_path: str, lines: Iterable[str]):
        """
        Writes list to file
        """
        if not self.is_dry_run:
            if not os.path.exists(file_path):
                with open(file_path, "w") as handle:
                    file_contents = "\n".join(lines)
                    handle.write(file_contents)

                file_written_successfully = os.path.exists(file_path)

                if file_written_successfully:
                    logger.info(f"Wrote to file {file_path} successfully")
                else:
                    logger.error(f"Error writing to file {file_path}")

                return file_written_successfully
            else:
                logger.error(f"File exists: {file_path}!")
                return False
        else:
            logger.info(f"Dry run: not writing to file {file_path}")
            return True
