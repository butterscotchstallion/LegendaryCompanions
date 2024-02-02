import os
from collections.abc import Iterable
from pathlib import Path

from companiongenerator.logger import logger


class FileHandler:
    """
    Handles file operations
    """

    def __init__(self, **kwargs):
        self.is_dry_run = True

        if "is_dry_run" in kwargs:
            self.is_dry_run = kwargs["is_dry_run"]

    def convert_bytes(self, num):
        """
        this function will convert bytes to MB.... GB... etc
        """
        for x in ["bytes", "KB", "MB", "GB", "TB"]:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0

    def write_string_to_file(self, file_path: str, contents: str) -> bool:
        """
        Writes list to file
        """
        if not self.is_dry_run:
            if not os.path.exists(file_path):
                with open(file_path, "w") as handle:
                    handle.write(contents)

                file_written_successfully = os.path.exists(file_path)

                if file_written_successfully:
                    readable_size = self.convert_bytes(os.path.getsize(file_path))
                    filename = Path(file_path).stem
                    logger.info(f'Wrote file "{filename}" ({readable_size})')
                else:
                    logger.error(f"Error writing to file {file_path}")

                return file_written_successfully
            else:
                logger.error(f"File exists: {file_path}!")
                return False
        else:
            logger.info(f"Dry run: not writing to file {file_path}")
            return True

    def write_list_to_file(self, file_path: str, lines: Iterable[str]):
        file_contents = "\n".join(lines)
        return self.write_string_to_file(file_path, file_contents)

    def get_file_contents(self, file_path: str):
        try:
            return Path(file_path).read_text()
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return ""
