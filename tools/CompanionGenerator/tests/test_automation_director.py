import xml.etree.ElementTree as ET
from typing import Literal, Required, TypedDict

from companiongenerator.automation_director import AutomationDirector
from companiongenerator.book_loca_entry import BookLocaEntry
from companiongenerator.book_parser import BookParser
from companiongenerator.character_mindflayer import CharacterMindflayer
from companiongenerator.character_parser import CharacterParser
from companiongenerator.constants import ARCH_MELEE_SMART_TPL_ID
from companiongenerator.equipment_set import EquipmentSet, EquipmentSetType
from companiongenerator.equipment_set_parser import EquipmentSetParser
from companiongenerator.item_combo import ItemCombo
from companiongenerator.item_combo_parser import ItemComboParser
from companiongenerator.localization_parser import LocalizationParser
from companiongenerator.logger import logger
from companiongenerator.root_template import CompanionRT
from companiongenerator.spell import Spell, SpellName, SummonSpell
from companiongenerator.spell_parser import SpellParser
from companiongenerator.stats_object_parser import StatsObjectParser

from tests.template_validity_helper import is_valid_handle_uuid, is_valid_uuid


def test_create():
    """
    Tests interactions between the automation director and various
    managers in order to create the necessary structures and files
    """
    director = AutomationDirector()
    unique_suffix = director.start_automation()

    eqp_set_name = "LC_EQP_Legendary"
    parent_template_id = ARCH_MELEE_SMART_TPL_ID
    companion_name_attr = f"LC_Legendary_Muffin_{unique_suffix}"
    rt_display_name = "Chip Chocolate"
    companion = CompanionRT(
        title="Legendary Muffin",
        name=companion_name_attr,
        displayName=rt_display_name,
        parentTemplateId=parent_template_id,
        equipmentSetName=eqp_set_name,
        statsName=companion_name_attr,
        root_template_aggregator=director.rt_aggregator,
        localization_aggregator=director.localization_aggregator,
    )
    # Add character entry
    character = CharacterMindflayer(stats_name=companion_name_attr)
    director.add_character_entry(character)

    # Add equipment set
    equipment_set = EquipmentSet(
        equipment_set_name=eqp_set_name,
        equipment_set_type=EquipmentSetType.MELEE_PLATE,
    )
    companion_map_key = director.add_companion_with_equipment(companion, equipment_set)

    assert is_valid_uuid(companion_map_key), "Invalid companion map key"

    # Add spells
    summon_spell_name = f"LC_Summon_Legendary_Muffin_{unique_suffix}"
    summon_spell = SummonSpell(
        display_name="Summon Muffin",
        description="A powerful summoning scroll",
        spell_name=summon_spell_name,
        summon_uuid=companion_map_key,
        localization_aggregator=director.localization_aggregator,
    )
    director.spell_aggregator.add_entry(summon_spell)

    summon_kobold_spell_name = f"LC_Summon_Legendary_Kobold_{unique_suffix}"
    summon_kobold = SummonSpell(
        display_name="Summon Kobold",
        description="A powerful summoning scroll",
        spell_name=summon_kobold_spell_name,
        summon_uuid=companion_map_key,
        localization_aggregator=director.localization_aggregator,
    )
    director.spell_aggregator.add_entry(summon_kobold)

    num_found_entries: int = 0
    for entry in director.spell_aggregator.entries:
        if num_found_entries < 2 and entry.spell_name in [
            summon_spell_name,
            summon_kobold_spell_name,
        ]:
            num_found_entries = num_found_entries + 1

        if num_found_entries > 2:
            break
    assert num_found_entries >= 2, "Failed to add summon spells to aggregator"

    """
    Book Pages
    """
    ## Summon Page 1
    summon_page_one_stats_name = f"LC_Summon_Page_1_{unique_suffix}"
    summon_page_one_rt_id = director.add_page(
        name=summon_page_one_stats_name,
        display_name="Summon page 1",
        description="Summon page description",
        stats_name=summon_page_one_stats_name,
    )
    assert is_valid_uuid(summon_page_one_rt_id), "Failed to add summon page one"

    ## Summon Page 2
    summon_page_two_stats_name = f"LC_Summon_Page_2_{unique_suffix}"
    summon_page_two_rt_id = director.add_page(
        name=summon_page_two_stats_name,
        display_name="Summon page 2",
        description="Summon page 2 description",
        stats_name=summon_page_two_stats_name,
    )
    assert is_valid_uuid(summon_page_two_rt_id), "Failed to add summon page two"

    ## Summon Book
    summon_book_stats_name = f"LC_Summon_Book_of_Testing_{unique_suffix}"
    summon_book_rt_id = director.add_book(
        name=summon_book_stats_name,
        display_name=f"Book of Testing {unique_suffix}",
        description="A thick leather bound tome",
        stats_name=summon_book_stats_name,
        book_id=f"Summon_Book_ID_{unique_suffix}",
    )
    assert is_valid_uuid(summon_book_rt_id), "Failed to add summon book"

    """
    Upgrade pages, book, scroll
    """
    ## Upgrade Page 1
    upgrade_page_one_stats_name = f"LC_Upgrade_Page_1_{unique_suffix}"
    upgrade_page_one_rt_id = director.add_page(
        name=upgrade_page_one_stats_name,
        display_name="Upgrade page 1",
        description="Upgrade page description",
        stats_name=upgrade_page_one_stats_name,
    )
    assert is_valid_uuid(upgrade_page_one_rt_id), "Failed to add upgrade page one"

    ## Upgrade Page 2
    upgrade_page_two_stats_name = f"LC_Upgrade_Page_2_{unique_suffix}"
    upgrade_page_two_rt_id = director.add_page(
        name=upgrade_page_one_stats_name,
        display_name="Upgrade page 2",
        description="Upgrade page description",
        stats_name=upgrade_page_two_stats_name,
    )
    assert is_valid_uuid(upgrade_page_two_rt_id), "Failed to add upgrade page two"

    ## Upgrade book
    upgrade_book_stats_name = f"LC_Upgrade_Book_of_Testing_{unique_suffix}"
    upgrade_book_rt_id = director.add_book(
        name=upgrade_book_stats_name,
        display_name=f"Book of Upgrade {unique_suffix}",
        description="A thick leather bound tome",
        stats_name=upgrade_book_stats_name,
        book_id=f"Upgrade_Book_ID_{unique_suffix}",
    )
    assert is_valid_uuid(upgrade_book_rt_id), "Failed to add upgrade book"

    ####################################################################
    ################### END PAGES & BOOKS ##############################
    ####################################################################

    """
    Combos
    """
    # Summon book combo
    summon_combo_name = f"Book_of_Summoning_Combo_{unique_suffix}"
    summon_combo = ItemCombo(
        combo_name=summon_combo_name,
        object_one_name=summon_page_one_stats_name,
        object_two_name=summon_page_two_stats_name,
        combo_result_item_name=summon_book_stats_name,
    )
    director.add_combo(summon_combo)

    # Upgrade book combo
    upgrade_combo_name = f"Book_of_Upgrade_Combo_{unique_suffix}"
    upgrade_combo = ItemCombo(
        combo_name=upgrade_combo_name,
        object_one_name=upgrade_page_one_stats_name,
        object_two_name=upgrade_page_two_stats_name,
        combo_result_item_name=upgrade_book_stats_name,
    )
    director.add_combo(upgrade_combo)

    assert (
        len(director.combo_aggregator.entries) >= 2
    ), "Failed to add summon and upgrade combos"

    """
    Summon/Upgrade Scrolls

    There should be one summon scroll and associated spell for
    each companion.
    """
    ## Summon scroll
    summon_scroll_stats_name = f"LC_Scroll_of_Summoning_{unique_suffix}"
    summon_scroll_rt_id = director.add_scroll(
        name=summon_scroll_stats_name,
        display_name="Summon Scroll of Testing",
        description="Summons a companion",
        # This must match the summon spell above!
        spell_name=summon_spell_name,
        stats_name=summon_scroll_stats_name,
    )
    assert is_valid_uuid(summon_scroll_rt_id), "Failed to verify scroll RT id"

    """
    Upgrade scroll
    We only need one of these because the same upgrade scroll can be used
    on any companion. Might change this later.
    """
    upgrade_scroll_rt_name = "LC_Scroll_Upgrade_Companion"
    upgrade_scroll_stats_name = "OBJ_LC_Scroll_Upgrade_Companion"
    upgrade_spell_name = "LC_Upgrade_Companion"
    upgrade_scroll_rt_id = director.add_scroll(
        name=upgrade_scroll_rt_name,
        display_name="Upgrade Scroll of Revelations",
        description="A glowing scroll, charged with chaotic energy",
        spell_name=upgrade_spell_name,
        stats_name=upgrade_scroll_stats_name,
    )
    assert is_valid_uuid(upgrade_scroll_rt_id), "Invalid upgrade scroll RT id"

    ####################################################################
    ############## END OBJECT ENTRIES/BEGIN UPDATES ####################
    ####################################################################

    # Update and verify character
    updated_char = director.update_characters()
    assert updated_char, "Failed to update character file"

    # Update stats file
    updated_stats = director.stats_object_aggregator.update_stats_file()
    assert updated_stats, "Failed to update object entries"

    ## Update root template
    updated_root_template = director.append_root_template()
    assert updated_root_template, "Failed to append root template"

    # Update combo file
    updated_combo_file = director.update_item_combos()
    assert updated_combo_file, "Failed to update upgrade item combos file"

    # Update spells
    updated_spells = director.update_spells()
    assert updated_spells, "Failed to update spells"

    ####################################################################
    ################ END UPDATES/BEGIN VERIFICATION ####################
    ####################################################################

    """
    Verify links between different parts of the process.
    1.  [✓] Companion RT -> equipment entry
    2.  [✓] Pages RTs -> object entry RT
    3.  [✓] Book RTs -> object entry RT
    4.  [✓] Scroll RT -> object entry RT
    5.  [✓] Scroll RT summon spell -> spell file
    6.  [✓] Companion RT DisplayName handle -> localization file [test_localization]
    7.  [✓] Companion RT Title handle -> localization file [test_localization]
    8.  [✓] Scroll RT DisplayName -> localization file [test_localization]
    9.  [✓] Page 1 RT DisplayName -> localization file [test_localization]
    10. [✓] Page 1 RT Description -> localization file [test_localization]
    11. [✓] Page 2 RT DisplayName -> localization file [test_localization]
    12. [✓] Page 2 RT DisplayName -> localization file [test_localization]
    13. [✓] Page 1 name -> combo file
    14. [✓] Page 2 name -> combo file
    15. [✓] Book name -> combo file
    16. [✓] Companion RT -> spell file summon UUID
    """
    verify_character(director)
    verify_books(director)
    verify_localization(director)
    verify_equipment_set(director)

    # Map of stats_name -> root template id
    objects_to_verify: dict[str, str] = {
        # Summon
        summon_page_one_stats_name: summon_page_one_rt_id,
        summon_page_two_stats_name: summon_page_two_rt_id,
        summon_book_stats_name: summon_book_rt_id,
        summon_scroll_stats_name: summon_scroll_rt_id,
        # Upgrade
        upgrade_page_one_stats_name: upgrade_page_one_rt_id,
        upgrade_page_two_stats_name: upgrade_page_two_rt_id,
        upgrade_book_stats_name: upgrade_book_rt_id,
        # There is only one upgrade scroll so this won't match
        # upgrade_scroll_stats_name: upgrade_scroll_rt_id,
    }

    verify_stats_objects(objects_to_verify)
    verify_spells(director)
    verify_combos_file(set([summon_combo_name, upgrade_combo_name]))


def verify_character(director: AutomationDirector):
    char_parser = CharacterParser()
    char_entry_names = char_parser.get_entry_names_from_text()
    assert director.companion.name in char_entry_names


def verify_books(director: AutomationDirector):
    # Write book localization file (book contents)
    book_name = f"Book_of_Localization_Testing_{director.unique_suffix}"
    book_contents = "This is a book about how much I love testing"
    unknown_description = "This is the unknown description"
    updated_book_children_el = director.update_book_file(
        name=book_name,
        content=book_contents,
        unknown_description=unknown_description,
    )
    assert (
        updated_book_children_el is not None
    ), "Failed to update book localization file"

    book: BookLocaEntry | Literal[False] = (
        director.book_loca_aggregator.get_book_with_name(book_name)
    )
    assert isinstance(book, BookLocaEntry), f"No book found with name {book_name}"
    assert is_valid_handle_uuid(book.content_handle)
    assert is_valid_handle_uuid(book.unknown_description_handle)

    verify_book_xml(book, updated_book_children_el)


def verify_localization(director: AutomationDirector):
    parser = LocalizationParser()
    updated_content_list = director.update_localization(parser)
    assert updated_content_list is not None, "Failed to update localization"


def verify_book_xml(book: BookLocaEntry, updated_book_children: ET.Element):
    """
    Verify book XML
    """
    parser = BookParser()
    all_book_attrs = parser.get_attrs_from_children(updated_book_children)
    assert all_book_attrs, "Failed to get book attrs"

    """
    Verify the above values match the XML
    NOTE: the books here can be books that existed before
    we added our book, so we identify the book with our
    UUID and stop there. Comparing to other books would
    result in a test failure, as those are different books.
    """
    if all_book_attrs is not None:
        for book_attrs in all_book_attrs:
            for attrs in book_attrs:
                book_match = (
                    attrs.attrib["id"] == "UUID" and attrs.attrib["value"] == book.name
                )
                if book_match:
                    # Handle values use the attribute "handle" for values!
                    if attrs.attrib["id"] == "Content":
                        assert (
                            attrs.attrib["handle"] == book.content_handle
                        ), "Content handle mismatch"
                    if attrs.attrib["id"] == "UnknownDescription":
                        assert (
                            attrs.attrib["handle"] == book.unknown_description_handle
                        ), "Unknown description mismatch"
                    # Stop here because we do not care about other books.
                    break


def verify_stats_objects(objects_to_verify: dict[str, str]):
    """ """
    # Verify page RT map key in object file
    stats_object_parser = StatsObjectParser()

    # Entry info for all objects
    object_entry_info: dict[str, dict] = stats_object_parser.get_entry_info_from_text()

    # Verify each object
    for stats_name in objects_to_verify:
        assert (
            stats_name in object_entry_info
        ), f"Failed to find entry name {stats_name}"
        assert (
            objects_to_verify[stats_name]
            == object_entry_info[stats_name]["root_template_id"]
        ), f"Root template id mismatch for {stats_name}"


def verify_equipment_set(director: AutomationDirector):
    # Verify companion RT equipment set is in equipment file
    equipment_parser = EquipmentSetParser()
    equipment_set_names = equipment_parser.get_entry_names_from_text()
    assert (
        director.companion.equipment_set_name in equipment_set_names
    ), "Failed to verify equipment set in file"


class VerifySpellsKeywords(TypedDict):
    spell_names_to_verify: Required[set[str]]
    companion_map_key: Required[str]


def verify_spells(director: AutomationDirector):
    """
    Verify each spell made it into the file
    1. [✓] Companion summon spell with
    2. [✓] Check companion RT id in the summon spell
    3. [✓] Scroll for upgrade spell (just need to check that the spell used
    in the spell is there)
    """
    spell_parser = SpellParser()
    companion_map_key: str = director.companion.map_key
    spell_entries: set[Spell | SpellName] = director.spell_aggregator.entries

    spell_entry_info: dict[str, dict] = spell_parser.get_entry_info_from_text()

    # Verify each spell name
    for spell in spell_entries:
        assert (
            spell.spell_name in spell_entry_info
        ), f"Failed to verify spell: {spell.spell_name}"

        if isinstance(spell, SummonSpell):
            assert (
                spell_entry_info[spell.spell_name]["summon_uuid"] == companion_map_key
            )


def verify_combos_file(combo_names: set[str]) -> None:
    """
    Verifies that all pages and books made it
    into the combo file
    """
    parser = ItemComboParser()
    combo_info = parser.get_combo_entries_from_file_contents()

    # The template has "_1" at the end of every combo result
    combo_names_with_suffix = set([combo_name + "_1" for combo_name in combo_names])

    # Checking issubset here because there could be existing combos
    is_combo_name_subset = combo_names.issubset(combo_info["combo_names"])
    is_combo_result_name_subset = combo_names_with_suffix.issubset(
        combo_info["combo_result_names"]
    )

    if not is_combo_name_subset:
        logger.debug("[+] Printing combo names difference")
        logger.debug(combo_names.difference(combo_info["combo_names"]))

    if not is_combo_result_name_subset:
        logger.debug("[+] Printing combo result names difference")
        logger.debug(combo_info["combo_result_names"])
        logger.debug(
            combo_names_with_suffix.difference(combo_info["combo_result_names"])
        )

    assert is_combo_name_subset, "[!] Combo name mismatch"
    assert is_combo_result_name_subset, "[!] Combo name result mismatch"
