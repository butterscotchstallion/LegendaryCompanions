import os
from uuid import uuid4

from companiongenerator.book_loca_entry import BookLocaEntry
from companiongenerator.file_handler import FileHandler
from companiongenerator.item_combo import ItemCombo
from companiongenerator.localization_manager import LocalizationManager
from companiongenerator.logger import logger
from companiongenerator.root_template import CompanionRT
from companiongenerator.spell import SummonSpell


class AutomationDirector:
    """
    Handles writing and editing of mod files by getting entries
    from managers
    """

    base_dir = "../output"
    is_dry_run: bool = True
    output_dir_path: str | None = None
    loca_mgr: LocalizationManager
    integration_name: str = ""
    default_localization_filename: str = "English"

    def __init__(self, **kwargs):
        if "is_dry_run" in kwargs:
            self.is_dry_run = kwargs["is_dry_run"]
        if "integration_name" in kwargs:
            self.integration_name = kwargs["integration_name"]

        self.loca_mgr = LocalizationManager(is_dry_run=self.is_dry_run)
        self.file_handler = FileHandler(is_dry_run=self.is_dry_run)

    def create_output_dir_if_not_exists(self):
        if not self.output_dir_path:
            output_dir_path = self._create_output_dir()

            if output_dir_path:
                self.output_dir_path = output_dir_path
                return output_dir_path

    def _create_output_dir(self):
        """
        Creates output directory where mod files will be created
        """
        dir_name = uuid4()
        dir_path = f"{self.base_dir}/{dir_name}"
        if not os.path.exists(dir_path) and not os.path.isdir(dir_path):
            if not self.is_dry_run:
                os.makedirs(dir_path)

                is_created_successfully = os.path.isdir(dir_path)

                if is_created_successfully:
                    logger.info(f"Created directory {dir_path}")
                    return dir_path
                else:
                    logger.error(f"Failed to create directory: {dir_path}")
            else:
                logger.info(f"Dry run: not creating directory {dir_path}")
                return dir_path
        else:
            logger.error(f"Directory {dir_path} exists!")
            return False

    def create_summon_spell(self, **kwargs):
        """
        Create spell based on supplied info
        """
        summon_spell = SummonSpell(**kwargs, localization_manager=self.loca_mgr)

        if summon_spell:
            generated_spell_text = summon_spell.get_tpl_with_replacements()

            if generated_spell_text:
                file_path = f"{self.output_dir_path}/{summon_spell.spell_name}.txt"

                if not os.path.exists(file_path) and not os.path.isfile(file_path):
                    is_write_successful = self.file_handler.write_list_to_file(
                        file_path, generated_spell_text.splitlines()
                    )
                    if is_write_successful:
                        logger.info(f"Wrote spell file: {file_path}")
                    else:
                        logger.error(f"Error writing file: {file_path}")

                    return is_write_successful
                else:
                    logger.error(f"File exists: {file_path}")

    def create_localization_file(self):
        """
        Creates main localization file (not the books)
        """
        filename = self.integration_name or self.default_localization_filename
        file_path = f"{self.output_dir_path}/{filename}.loca.xml"
        return self.loca_mgr.write_entries(file_path)

    def create_book_localization_file(self, **kwargs):
        """
        Creates localization file (the books)
        """
        book_loca_entry = BookLocaEntry(localization_manager=self.loca_mgr, **kwargs)
        book_entry_xml = book_loca_entry.get_tpl_with_replacements()
        file_path = f"{self.output_dir_path}/Books.lsf.lsx"
        return self.file_handler.write_string_to_file(file_path, book_entry_xml)

    def create_item_combos(self, **kwargs):
        """
        Creates item combos file
        """
        item_combos = ItemCombo(**kwargs)
        item_combo_tpl = item_combos.get_tpl_with_replacements()
        file_path = f"{self.output_dir_path}/{item_combos.filename}"
        return self.file_handler.write_string_to_file(file_path, item_combo_tpl)

    def create_companion_rt(self, **kwargs):
        companion_rt = CompanionRT(**kwargs)
        companion_tpl = companion_rt.get_tpl_with_replacements()
        file_path = f"{self.output_dir_path}/companion_rt.lsf.lsx"
        return self.file_handler.write_string_to_file(file_path, companion_tpl)
