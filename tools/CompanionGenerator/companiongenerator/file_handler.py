import os
import shutil
from collections.abc import Iterable
from pathlib import Path

from companiongenerator.logger import logger


class FileHandler:
    """
    Handles file operations
    """

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
                logger.info(f"Created backup file: {origin_filename}.lcbackup")
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

    def append_to_file(self, file_path: str, contents: str) -> bool:
        """
        Creates backup and appends content file at supplied path.
        """
        try:
            if len(contents) > 0:
                created_backup = self.create_backup_file(file_path)
                if created_backup:
                    with open(file_path, "a+") as handle:
                        handle.seek(os.SEEK_END)
                        contents = f"\n\n{contents}"
                        return bool(handle.write(contents))
                else:
                    return False
            else:
                logger.error("Empty contents")
                return False
        except IOError as err:
            logger.error(f"Error appending to file {file_path}: {err}")
            return False
