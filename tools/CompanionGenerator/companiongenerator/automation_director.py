import xml.etree.ElementTree as ET
from pathlib import Path
from time import time
from typing import Required, TypedDict, Unpack
from uuid import uuid4

from companiongenerator.book_loca_aggregator import BookLocaAggregator
from companiongenerator.book_parser import BookParser
from companiongenerator.character import Character
from companiongenerator.character_aggregator import CharacterAggregator
from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.equipment_set import EquipmentSet
from companiongenerator.equipment_set_aggregator import EquipmentSetAggregator
from companiongenerator.file_handler import FileHandler
from companiongenerator.item_combo import ItemCombo
from companiongenerator.item_combo_aggregator import ItemComboAggregator
from companiongenerator.localization_aggregator import LocalizationAggregator
from companiongenerator.localization_parser import LocalizationParser
from companiongenerator.log_message import CriticalErrorMessage
from companiongenerator.log_message_aggregator import LogMessageAggregator
from companiongenerator.logger import logger
from companiongenerator.root_template import (
    BookRT,
    BookRTKeywords,
    CompanionRT,
    ItemRTKeywords,
    PageRT,
    ScrollRT,
    ScrollRTKeywords,
)
from companiongenerator.root_template_aggregator import RootTemplateAggregator
from companiongenerator.spell_aggregator import SpellAggregator
from companiongenerator.stats_object import StatsObject
from companiongenerator.stats_object_aggregator import StatsObjectAggregator


class StatsKeywords(TypedDict):
    name: Required[str]
    display_name: Required[str]
    description: Required[str]
    stats_name: Required[str]


class SpellStatsKeywords(StatsKeywords):
    spell_name: Required[str]


class BookKeywords(StatsKeywords):
    book_id: Required[str]


class AutomationDirector:
    """
    Handles writing and editing of mod files by getting entries
    from managers
    """

    localization_aggregator: LocalizationAggregator
    book_loca_aggregator: BookLocaAggregator
    rt_aggregator: RootTemplateAggregator
    stats_object_aggregator: StatsObjectAggregator
    combo_aggregator: ItemComboAggregator
    spell_aggregator: SpellAggregator
    equipment_set_aggregator: EquipmentSetAggregator
    character_aggregator: CharacterAggregator
    log_message_aggregator: LogMessageAggregator
    default_localization_filename: str = "English"
    companion: CompanionRT
    start_time: float
    end_time: float

    def __init__(self):
        self.rt_aggregator = RootTemplateAggregator()
        self.localization_aggregator = LocalizationAggregator()
        self.book_loca_aggregator = BookLocaAggregator()
        self.stats_object_aggregator = StatsObjectAggregator()
        self.combo_aggregator = ItemComboAggregator()
        self.spell_aggregator = SpellAggregator()
        self.equipment_set_aggregator = EquipmentSetAggregator()
        self.character_aggregator = CharacterAggregator()
        self.log_message_aggregator = LogMessageAggregator()
        self.file_handler = FileHandler()
        self.unique_suffix = str(uuid4())[0:6]

    def start_automation(self) -> str:
        """
        Shows start up message and loads entries from existing files.

        Returns the unique string associated with this run.
        """
        logger.info("=================================================")
        logger.info(f"Initializing new automation run! [{self.unique_suffix}]")
        logger.info("=================================================")

        automation_start = time()

        self.localization_aggregator.load_localization_entries_from_file()
        self.combo_aggregator.load_entries_from_file()
        self.spell_aggregator.load_entries_from_file()
        self.equipment_set_aggregator.load_entries_from_file()
        self.character_aggregator.load_entries_from_file()

        logger.info(
            f"Loaded entries from file in {str(round(time() - automation_start, 2))} seconds"
        )

        return self.unique_suffix

    def can_update(self) -> bool:
        """
        We should not update unless there are no critical errors
        """
        return not self.log_message_aggregator.has_critical_errata()

    def add_combo(self, combo: ItemCombo):
        """
        Adds combos to aggregator
        """
        self.combo_aggregator.add_entry(combo)

    def add_companion_with_equipment(
        self, companionRT: CompanionRT, equipment_set: EquipmentSet
    ) -> str:
        """
        - Adds a new companion with equipment set
        - Used to verify equipment set in test
        - Need to refactor this if we ever add the ability to add
        more than one companion in a run
        """
        self.companion = companionRT

        # Add companion
        tpl = self.companion.get_tpl_with_replacements()
        logger.info(
            f"Adding RT entry: {self.companion.display_name} [{self.companion.map_key}]"
        )
        self.rt_aggregator.add_entry(
            tpl, self.companion.get_comment(), self.companion.name
        )

        # Add equipment set
        self.equipment_set_aggregator.add_entry(equipment_set)

        return self.companion.map_key

    def add_character_entry(self, character: Character):
        self.character_aggregator.add_entry(character)

    def update_characters(self) -> bool | None:
        success = self.character_aggregator.update_character_file()
        if not success:
            self.log_message_aggregator.log(
                CriticalErrorMessage(
                    message="Error updating character file", module_name=str(__class__)
                )
            )
        return success

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
        success = False
        if self.can_update():
            success = self.equipment_set_aggregator.update_equipment_sets()
            if not success:
                self.log_message_aggregator.log(
                    CriticalErrorMessage(
                        message="Error updating equipment set",
                        module_name=str(__class__),
                    )
                )
        return success

    def update_spells(self) -> bool | None:
        """
        Updates spell file and appends new spell
        """
        success = False
        if self.can_update():
            success = self.spell_aggregator.update_spells()
            if not success:
                self.log_message_aggregator.log(
                    CriticalErrorMessage(
                        message="Error updating spells", module_name=str(__class__)
                    )
                )
        return success

    def update_localization(self, parser: LocalizationParser) -> bool:
        """
        Update localization file with all entries
        from localization aggregator
        """
        loca_file = MOD_FILENAMES["localization"]
        entries = self.localization_aggregator.entries
        num_entries = len(entries)
        success = False
        if self.can_update():
            if num_entries:
                backup_created = self.file_handler.create_backup_file(loca_file)
                if backup_created:
                    updated_content_list = parser.append_entries(loca_file, entries)
                    if updated_content_list is not None:
                        parser.write_tree()
                        success = True
            else:
                logger.error("No localization entries!")

            if not success:
                self.log_message_aggregator.log(
                    CriticalErrorMessage(
                        message="Error updating localization",
                        module_name=str(__class__),
                    )
                )
        return success

    def update_book_file(self, **kwargs) -> ET.Element | None:
        """
        Updates book file
        1. Add new book to book loca aggregator
        2. Create book file if not existing
        3. Create backup of file
        4. Obtain modified XML tree of book structure with new books
        5. Write new XML tree to file
        """
        success = False
        if self.can_update():
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
                        success = True
                        return books

            if not success:
                self.log_message_aggregator.log(
                    CriticalErrorMessage(
                        message="Error updating book file", module_name=str(__class__)
                    )
                )

    def update_item_combos(self):
        """
        Updates item combos file. Returns True if file update
        succeeds or the combo exists already
        """
        success = False
        if self.can_update():
            success = self.combo_aggregator.update_item_combos()
            if not success:
                self.log_message_aggregator.log(
                    CriticalErrorMessage(
                        message="Error updating item combos", module_name=str(__class__)
                    )
                )
        return success

    def update_root_template(self) -> bool | None:
        """
        Appends to existing root template using
        RootTemplateAggregator.
        """
        success = False
        if self.can_update():
            backup_created = self.file_handler.create_backup_file(
                MOD_FILENAMES["root_template_merged"]
            )
            if backup_created:
                success = self.rt_aggregator.append_root_template()

            if not success:
                self.log_message_aggregator.log(
                    CriticalErrorMessage(
                        message="Error updating root template",
                        module_name=str(__class__),
                    )
                )
        return success

    def add_page_rt(self, **kwargs: Unpack[ItemRTKeywords]) -> str:
        rt = PageRT(**kwargs)
        tpl = rt.get_tpl_with_replacements()
        self.rt_aggregator.add_entry(tpl, rt.get_comment(), rt.name)
        return rt.map_key

    def add_book_rt(self, **kwargs: Unpack[BookRTKeywords]) -> str:
        rt = BookRT(**kwargs)
        # Used to verify links in test
        self.book_rt = rt
        tpl = rt.get_tpl_with_replacements()
        self.rt_aggregator.add_entry(tpl, rt.get_comment(), rt.name)
        return rt.map_key

    def add_scroll_rt(self, **kwargs: Unpack[ScrollRTKeywords]) -> str:
        rt = ScrollRT(**kwargs)
        tpl = rt.get_tpl_with_replacements()
        self.rt_aggregator.add_entry(tpl, rt.get_comment(), rt.name)
        return rt.map_key
