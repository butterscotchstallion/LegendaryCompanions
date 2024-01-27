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

    def create_output_dir(self, dir_path: str):
        """
        Creates output directory where mod files will be created
        """
        if not os.path.exists(dir_path) and not os.path.isdir(dir_path):
            if not self.is_dry_run:
                os.makedirs(dir_path)

                is_created_successfully = os.path.isdir(dir_path)

                if is_created_successfully:
                    log.info(f"Created directory {dir_path}")
                    return True
            else:
                log.info(f"Dry run: not creating directory {dir_path}")
                return True
        else:
            log.error(f"Directory {dir_path} exists!")
            return False
