import os
from pathlib import Path
from uuid import uuid4

from companiongenerator.book_loca_aggregator import BookLocaAggregator
from companiongenerator.book_parser import BookParser
from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.equipment_parser import EquipmentParser
from companiongenerator.equipment_set import EquipmentSet, EquipmentSetType
from companiongenerator.file_handler import FileHandler
from companiongenerator.item_combo import ItemCombo
from companiongenerator.item_combos_parser import ItemCombosParser
from companiongenerator.localization_aggregator import LocalizationAggregator
from companiongenerator.localization_parser import LocalizationParser
from companiongenerator.logger import logger
from companiongenerator.root_template import BookRT, CompanionRT, PageRT, ScrollRT
from companiongenerator.root_template_aggregator import RootTemplateAggregator
from companiongenerator.spell import SummonSpell
from companiongenerator.stats_object_aggregator import StatsObjectAggregator
from companiongenerator.stats_parser import ParserType, StatsParser


class AutomationDirector:
    """
    Handles writing and editing of mod files by getting entries
    from managers
    """

    base_dir = "../output"
    localization_aggregator: LocalizationAggregator
    book_loca_aggregator: BookLocaAggregator
    rt_aggregator: RootTemplateAggregator
    stats_object_aggregator: StatsObjectAggregator
    integration_name: str = ""
    default_localization_filename: str = "English"

    def __init__(self, **kwargs):
        if "integration_name" in kwargs:
            self.integration_name = kwargs["integration_name"]

        self.rt_aggregator = RootTemplateAggregator()
        self.localization_aggregator = LocalizationAggregator()
        self.book_loca_aggregator = BookLocaAggregator()
        self.stats_object_aggregator = StatsObjectAggregator()
        self.file_handler = FileHandler()
        self.unique_suffix = str(uuid4())[0:6]

        logger.info("=================================================")
        logger.info(f"Initializing new automation run! [{self.unique_suffix}]")
        logger.info("=================================================")

    def update_equipment(
        self, equipment_set_name: str, equipment_set_type: EquipmentSetType
    ):
        """
        Updates equipment file with new set, if it doesn't exist
        """
        parser = EquipmentParser()
        equipment_set = EquipmentSet(
            name=equipment_set_name, equipment_set_type=equipment_set_type
        )
        equipment_text = equipment_set.get_tpl_with_replacements()
        return parser.add_entry(equipment_set_name, equipment_text)

    def update_summon_spells(self, **kwargs):
        """
        Updates spell file and appends new spell
        """
        filename = MOD_FILENAMES["spell_text_file_summons"]
        handler = FileHandler()
        summon_spell = SummonSpell(
            **kwargs, localization_aggregator=self.localization_aggregator
        )

        generated_spell_text = summon_spell.get_tpl_with_replacements()

        # Open spell file and append new spell if it doesn't exist
        try:
            # Open file for reading and writing, creating if not exists
            with open(filename, "a+") as handle:
                parser = StatsParser(filename=filename, parser_type=ParserType.SPELL)
                # Since we started at the end of the file, we have to seek to the beginning
                # to get the file contents
                handle.seek(0)
                spell_text = handle.read()

                spell_name_exists = parser.entry_name_exists_in_text(
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
                                f'Appended spell "{summon_spell.spell_name}" [Summon UUID: {summon_spell.summon_uuid}] to spell file'
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

    def update_localization(self, parser: LocalizationParser) -> bool | None:
        """
        Update localization file with all entries
        from localization aggregator
        """
        loca_file = MOD_FILENAMES["localization"]
        entries = self.localization_aggregator.entries
        num_entries = len(entries)

        if num_entries:
            logger.info(f"There are {num_entries} localization entries aggregated")

            backup_created = self.file_handler.create_backup_file(loca_file)

            if backup_created:
                updated_content_list = parser.append_entries(loca_file, entries)

                if updated_content_list is not None:
                    parser.write_tree()
                    return True
        else:
            logger.error("No localization entries!")

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
                        f"Updated book file: {Path(parser.filename).stem} with book {book.name}"
                    )
                    return books
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

    def append_root_template(self) -> bool | None:
        """
        Appends to existing root template using
        RootTemplateAggregator.
        """
        backup_created = self.file_handler.create_backup_file(
            MOD_FILENAMES["root_template_merged"]
        )
        if backup_created:
            return self.rt_aggregator.append_root_template()

    def add_companion_rt(self, **kwargs) -> str:
        rt = CompanionRT(**kwargs)
        self.companion = rt
        tpl = rt.get_tpl_with_replacements()
        logger.info(f"Adding RT entry: {rt.display_name} [{rt.map_key}]")
        self.rt_aggregator.add_entry(tpl, rt.get_comment(), rt.name)
        return rt.map_key

    def add_page_rt(self, **kwargs) -> str:
        rt = PageRT(**kwargs)
        tpl = rt.get_tpl_with_replacements()
        self.rt_aggregator.add_entry(tpl, rt.get_comment(), rt.name)
        return rt.map_key

    def add_book_rt(self, **kwargs) -> str:
        rt = BookRT(**kwargs)
        tpl = rt.get_tpl_with_replacements()
        self.rt_aggregator.add_entry(tpl, rt.get_comment(), rt.name)
        return rt.map_key

    def add_scroll_rt(self, **kwargs) -> str:
        rt = ScrollRT(**kwargs)
        tpl = rt.get_tpl_with_replacements()
        self.rt_aggregator.add_entry(tpl, rt.get_comment(), rt.name)
        return rt.map_key
