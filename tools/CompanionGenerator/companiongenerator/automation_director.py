from pathlib import Path
from typing import TypedDict, Unpack
from uuid import uuid4

from companiongenerator.book_loca_aggregator import BookLocaAggregator
from companiongenerator.book_parser import BookParser
from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.equipment_set_aggregator import EquipmentSetAggregator
from companiongenerator.file_handler import FileHandler
from companiongenerator.item_combo_aggregator import ItemComboAggregator
from companiongenerator.localization_aggregator import LocalizationAggregator
from companiongenerator.localization_parser import LocalizationParser
from companiongenerator.logger import logger
from companiongenerator.root_template import BookRT, CompanionRT, PageRT, ScrollRT
from companiongenerator.root_template_aggregator import RootTemplateAggregator
from companiongenerator.spell_aggregator import SpellAggregator
from companiongenerator.stats_object import StatsObject
from companiongenerator.stats_object_aggregator import StatsObjectAggregator


class StatsKeywords(TypedDict):
    name: str
    display_name: str
    description: str
    stats_name: str


class SpellStatsKeywords(StatsKeywords):
    spell_name: str


class BookKeywords(StatsKeywords):
    book_id: str


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
        self.combo_aggregator = ItemComboAggregator()
        self.spell_aggregator = SpellAggregator()
        self.equipment_set_aggregator = EquipmentSetAggregator()
        self.file_handler = FileHandler()
        self.unique_suffix = str(uuid4())[0:6]

    def start_automation(self):
        """
        Shows start up message and loads entries from existing files
        """
        logger.info("=================================================")
        logger.info(f"Initializing new automation run! [{self.unique_suffix}]")
        logger.info("=================================================")

        self.localization_aggregator.load_localization_entries_from_file()
        self.combo_aggregator.load_entries_from_file()
        self.spell_aggregator.load_entries_from_file()
        self.equipment_set_aggregator.load_entries_from_file()

    def add_scroll(self, **kwargs: Unpack[SpellStatsKeywords]) -> str:
        """
        Handles all the operations necessary to add a new scroll:
        1. Add RT
        2. Add object entry
        3. Add to aggregator
        """
        scroll_rt_id = self.add_scroll_rt(
            name=kwargs["name"],
            displayName=kwargs["display_name"],
            description=kwargs["description"],
            scrollSpellName=kwargs["spell_name"],
            statsName=kwargs["stats_name"],
            localization_aggregator=self.localization_aggregator,
        )
        # Add scroll object file
        scroll_obj = StatsObject(
            stats_name=kwargs["stats_name"], root_template_id=scroll_rt_id
        )
        self.stats_object_aggregator.add_entry(scroll_obj)

        return scroll_rt_id

    def add_page(self, **kwargs: Unpack[StatsKeywords]) -> str:
        """
        Add page
        1. Add RT
        2. Create page object
        3. Add page object to stats_obj_aggregator
        """
        page_rt_id = self.add_page_rt(
            name=kwargs["stats_name"],
            displayName=kwargs["display_name"],
            description=kwargs["description"],
            statsName=kwargs["stats_name"],
            localization_aggregator=self.localization_aggregator,
        )
        page_obj = StatsObject(
            stats_name=kwargs["stats_name"], root_template_id=page_rt_id
        )
        self.stats_object_aggregator.add_entry(page_obj)
        return page_rt_id

    def add_book(self, **kwargs: Unpack[BookKeywords]) -> str:
        """
        Add book
        1. Add RT
        2. Create book object
        3. Add book object to stats_obj_aggregator
        """
        book_rt_id = self.add_book_rt(
            name=kwargs["stats_name"],
            displayName=kwargs["display_name"],
            description=kwargs["description"],
            statsName=kwargs["stats_name"],
            localization_aggregator=self.localization_aggregator,
            book_id=kwargs["book_id"],
        )
        book_obj = StatsObject(
            stats_name=kwargs["stats_name"], root_template_id=book_rt_id
        )
        self.stats_object_aggregator.add_entry(book_obj)
        return book_rt_id

    def update_equipment(self) -> bool:
        """
        Updates equipment file with new set, if it doesn't exist
        """
        return self.equipment_set_aggregator.update_equipment_sets()

    def update_spells(self) -> bool | None:
        """
        Updates spell file and appends new spell
        """
        return self.spell_aggregator.update_spells()

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

    def update_item_combos(self):
        """
        Updates item combos file. Returns True if file update
        succeeds or the combo exists already
        """
        return self.combo_aggregator.update_item_combos()

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
        rt = CompanionRT(**kwargs, root_template_aggregator=self.rt_aggregator)
        self.companion = rt
        tpl = rt.get_tpl_with_replacements()
        logger.info(f"Adding RT entry: {rt.display_name} [{rt.map_key}]")
        self.rt_aggregator.add_entry(tpl, rt.get_comment(), rt.name)
        return rt.map_key

    def add_page_rt(self, **kwargs) -> str:
        rt = PageRT(**kwargs, root_template_aggregator=self.rt_aggregator)
        tpl = rt.get_tpl_with_replacements()
        self.rt_aggregator.add_entry(tpl, rt.get_comment(), rt.name)
        return rt.map_key

    def add_book_rt(self, **kwargs) -> str:
        rt = BookRT(**kwargs, root_template_aggregator=self.rt_aggregator)
        # Used to verify links in test
        self.book_rt = rt
        tpl = rt.get_tpl_with_replacements()
        self.rt_aggregator.add_entry(tpl, rt.get_comment(), rt.name)
        return rt.map_key

    def add_scroll_rt(self, **kwargs) -> str:
        rt = ScrollRT(**kwargs, root_template_aggregator=self.rt_aggregator)
        tpl = rt.get_tpl_with_replacements()
        self.rt_aggregator.add_entry(tpl, rt.get_comment(), rt.name)
        return rt.map_key
