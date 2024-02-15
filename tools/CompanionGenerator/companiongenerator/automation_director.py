import datetime
import os
from pathlib import Path
from uuid import uuid4

from companiongenerator.book_loca_aggregator import BookLocaAggregator
from companiongenerator.book_parser import BookParser
from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.file_handler import FileHandler
from companiongenerator.item_combo import ItemCombo
from companiongenerator.item_combos_parser import ItemCombosParser
from companiongenerator.localization_aggregator import LocalizationAggregator
from companiongenerator.logger import logger
from companiongenerator.root_template import BookRT, CompanionRT, PageRT, ScrollRT
from companiongenerator.root_template_aggregator import RootTemplateAggregator
from companiongenerator.spell import SummonSpell
from companiongenerator.stats_parser import StatsParser


class AutomationDirector:
    """
    Handles writing and editing of mod files by getting entries
    from managers
    """

    base_dir = "../output"
    is_dry_run: bool = True
    output_dir_path: str | None = None
    localization_aggregator: LocalizationAggregator
    book_loca_aggregator: BookLocaAggregator
    rt_aggregator: RootTemplateAggregator
    integration_name: str = ""
    default_localization_filename: str = "English"

    def __init__(self, **kwargs):
        if "is_dry_run" in kwargs:
            self.is_dry_run = kwargs["is_dry_run"]
        if "integration_name" in kwargs:
            self.integration_name = kwargs["integration_name"]

        self.rt_aggregator = RootTemplateAggregator(is_dry_run=self.is_dry_run)
        self.localization_aggregator = LocalizationAggregator(
            is_dry_run=self.is_dry_run
        )
        self.book_loca_aggregator = BookLocaAggregator()
        self.file_handler = FileHandler(is_dry_run=self.is_dry_run)
        logger.info("=================================================")
        logger.info("Initializing new automation run!")
        logger.info("=================================================")

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
        ahorita = datetime.datetime.now()
        shortened_uuid = str(uuid4())[0:7]
        dir_name = f"{ahorita.strftime('%Y-%m-%d_%I-%M-%S')}_{shortened_uuid}"
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

    def update_summon_spells(self, **kwargs):
        """
        Updates spell file and appends new spell
        """
        filename = MOD_FILENAMES["spell_text_file_summons"]
        handler = FileHandler()
        backup_created = handler.create_backup_file(filename)

        if backup_created:
            summon_spell = SummonSpell(
                **kwargs, localization_manager=self.localization_aggregator
            )

            generated_spell_text = summon_spell.get_tpl_with_replacements()

            # Open spell file and append new spell if it doesn't exist
            try:
                # Open file for reading and writing, creating if not exists
                with open(filename, "a+") as handle:
                    parser = StatsParser()
                    # Since we started at the end of the file, we have to seek to the beginning
                    # to get the file contents
                    handle.seek(0)
                    spell_text = handle.read()

                    spell_name_exists = parser.spell_name_exists_in_spell_text(
                        summon_spell.spell_name, spell_text
                    )
                    # Not really a big deal if it exists. We just bail out here
                    if spell_name_exists:
                        logger.info(
                            f"Spell name {summon_spell.spell_name} exists! Skipping"
                        )
                        return True
                    else:
                        # New spell: create backup before proceeding
                        handler = FileHandler()
                        backup_created = handler.create_backup_file(filename)

                        if backup_created:
                            # Seek to end before appending
                            handle.seek(os.SEEK_END)
                            # Append to existing file
                            spell_with_new_line = f"{os.linesep}{generated_spell_text}"
                            success = handle.write(spell_with_new_line)

                            if success:
                                logger.info(
                                    f'Appended spell "{summon_spell.spell_name}" to spell file'
                                )
                            else:
                                logger.error("Failed to append to spell file")

                            return success
                        else:
                            logger.error(f"Failed to create backup of {filename}")
                            return False
            except IOError as err:
                logger.error(f"Error opening summon spell file: {err}")
                return False

    def update_book_file(self, **kwargs):
        """
        Updates book file
        1. Add new book to book loca aggregator
        2. Create book file if not existing
        3. Create backup of file
        4. Obtain modified XML tree of book structure with new books
        5. Write new XML tree to file
        """
        book_filename = MOD_FILENAMES["books"]
        book = self.book_loca_aggregator.add_book_and_return_book(
            localization_aggregator=self.localization_aggregator,
            **kwargs,
        )

        self.book_content_handle = book.content_handle

        create_ok = self.file_handler.create_template_if_not_exists(
            book_filename, MOD_FILENAMES["book_template_file"]
        )

        if create_ok:
            parser = BookParser()
            books = parser.update_book_file(
                book_filename, self.book_loca_aggregator.entries
            )

            if books is not None:
                backup_created = self.file_handler.create_backup_file(book_filename)
                if backup_created:
                    parser.write_tree()
                    logger.info(
                        f"Wrote updated book file: {Path(parser.filename).stem}"
                    )
                    return books
                else:
                    logger.error("Failed to create backup file!")
        else:
            logger.error("Failed to create book template")

    def update_item_combos(self, **kwargs):
        """
        Updates item combos file. Returns True if file update
        succeeds or the combo exists already
        """
        item_combo = ItemCombo(**kwargs)
        item_combo_tpl = item_combo.get_tpl_with_replacements()

        with open(MOD_FILENAMES["item_combos"], "a+") as handle:
            handle.seek(0)
            item_combo_contents = handle.read()
            combo_exists = False

            if len(item_combo_contents) > 0:
                parser = ItemCombosParser()
                combo_exists = parser.combo_name_exists(
                    item_combo.combo_name, item_combo_contents
                )
            if not combo_exists:
                handler = FileHandler()
                created_backup = handler.create_backup_file(
                    MOD_FILENAMES["item_combos"]
                )
                if created_backup:
                    logger.info(f"Backup created for {MOD_FILENAMES["item_combos"]}")
                    handle.seek(os.SEEK_END)
                    combo_text = f"{os.linesep}{item_combo_tpl}"
                    logger.info(f"Added item combo {item_combo.combo_name} to file")
                    return handle.write(combo_text)
                else:
                    logger.error(
                        f"Failed to create backup of {MOD_FILENAMES["item_combos"]}"
                    )
                    return False
            else:
                logger.info(f"Item combo {item_combo.combo_name} exists")
                return True

    def append_root_template(self, file_path: str) -> bool | None:
        """
        Appends to existing root template using
        RootTemplateAggregator.
        """
        return self.rt_aggregator.append_root_template(file_path)

    def add_companion_rt(self, **kwargs):
        rt = CompanionRT(**kwargs)
        self.companion = rt
        tpl = rt.get_tpl_with_replacements()
        self.rt_aggregator.add_entry(tpl, rt.get_comment(), rt.name)

    def add_page_rt(self, **kwargs):
        rt = PageRT(**kwargs)
        tpl = rt.get_tpl_with_replacements()
        self.rt_aggregator.add_entry(tpl, rt.get_comment(), rt.name)

    def add_book_rt(self, **kwargs):
        rt = BookRT(**kwargs)
        tpl = rt.get_tpl_with_replacements()
        self.rt_aggregator.add_entry(tpl, rt.get_comment(), rt.name)

    def add_scroll_rt(self, **kwargs):
        rt = ScrollRT(**kwargs)
        tpl = rt.get_tpl_with_replacements()
        self.rt_aggregator.add_entry(tpl, rt.get_comment(), rt.name)
