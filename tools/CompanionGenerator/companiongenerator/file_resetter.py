from pathlib import Path

from companiongenerator.file_templates import FileTemplates
from companiongenerator.logger import logger
from companiongenerator.replica_files import ReplicaFiles


class FileResetter:
    """
    Resets various file types to their default state
    using their templates
    """

    def reset_root_template(self) -> bool:
        """Overwrites with merged template

        Args:
            filename (str): Filename of RT
        """
        return self.overwrite_file_with_template(
            ReplicaFiles.root_template_file, FileTemplates.root_template_file
        )

    def reset_combos_file(self) -> bool:
        return self.reset_text_file(ReplicaFiles.item_combos)

    def reset_text_file(self, filename: str) -> bool:
        logger.info(f"Resetting text file: {filename}")
        with open(filename, "w+") as fh:
            return bool(fh.write(""))

    def reset_localization_file(self, filename: str) -> bool:
        return self.overwrite_file_with_template(filename, ReplicaFiles.localization)

    def overwrite_file_with_template(
        self, file_to_overwrite: str, template_filename: str
    ) -> bool:
        """
        Overwrites target file with template contents
        """
        fh = Path(template_filename)
        template_contents = fh.read_text()

        if fh.exists():
            if template_contents:
                fh = Path(file_to_overwrite)
                return bool(fh.write_text(template_contents))
            else:
                logger.error(f"Empty template: {template_filename}")
                return False
        else:
            logger.error(f"Template file does not exist: {template_filename}")
            return False
