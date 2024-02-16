import os
import shutil
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

    def create_template_if_not_exists(self, filename: str, template_filename: str):
        """Creates template file if it doesn't exist"""
        try:
            if not os.path.exists(filename):
                tpl_file = Path(template_filename).read_text()
                logger.info(f"Creating file from template: {filename}")
                return Path(filename).write_text(tpl_file)
            else:
                return True
        except IOError as err:
            logger.error(f"Error creating file from template: {err}")
            return False

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
        Writes list to file and confirms it was successful by checking
        that it exists
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

    def create_backup_file(self, file_path: str) -> bool | None:
        """
        Creates backup file from provided filename
        """
        try:
            origin_path_obj = Path(file_path)
            origin_parent = origin_path_obj.parent
            origin_filename = origin_path_obj.stem
            backup_path = f"{origin_parent}/{origin_filename}.lcbackup"
            result = shutil.copy2(file_path, backup_path)
            if result:
                logger.info(f"Created backup file: {backup_path}")
                return True
            else:
                raise RuntimeError("Error creating backup file: failed to copy")
        except IOError as err:
            raise RuntimeError(f"Error creating backup file: {os.strerror(err.errno)}")

    def get_file_contents(self, file_path: str):
        try:
            return Path(file_path).read_text()
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return ""
