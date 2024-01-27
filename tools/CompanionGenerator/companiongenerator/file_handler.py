import os

from companiongenerator.logger import log


class FileHandler:
    """
    Handles file operations
    """

    def __init__(self, **kwargs):
        self.is_dry_run = True

        if "is_dry_run" in kwargs:
            self.is_dry_run = kwargs["is_dry_run"]

    def write_list_to_file(self, file_path: str, lines: list[str]):
        """
        Writes list to file
        """
        if not self.is_dry_run:
            if not os.exists(file_path):
                with open(file_path) as handle:
                    handle.writelines(lines)

                file_written_successfully = os.exists(file_path)

                if file_written_successfully:
                    log.info(f"Wrote to file {file_path} successfully")
                else:
                    log.error(f"Error writing to file {file_path}")

                return file_written_successfully
            else:
                log.error(f"File exists: {file_path}!")
                return False
        else:
            log.info(f"Dry run: not writing to file {file_path}")
            return True
