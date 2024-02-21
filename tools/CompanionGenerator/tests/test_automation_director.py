from typing import Literal
from uuid import uuid4

from companiongenerator.automation_director import AutomationDirector
from companiongenerator.book_loca_entry import BookLocaEntry
from companiongenerator.book_parser import BookParser
from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.equipment_parser import EquipmentParser
from companiongenerator.equipment_set import EquipmentSetType
from companiongenerator.localization_parser import LocalizationParser
from companiongenerator.stats_parser import ParserType, StatsParser

from tests.template_validity_helper import is_valid_handle_uuid, is_valid_uuid


def test_create():
    """
    Tests interactions between the automation director and various
    managers in order to create the necessary structures and files
    """
    director = AutomationDirector()
    unique_suffix = director.unique_suffix

    ## Companion RT
    eqp_set_name = "LC_EQP_Legendary"
    # TODO: change this to something real. Maybe an enumeration
    parent_template_id = str(uuid4())
    companion_name_attr = f"LC_Legendary_Muffin_{unique_suffix}"
    rt_display_name = "Chip Chocolate"
    companion_map_key = director.add_companion_rt(
        title="Legendary Muffin",
        name=companion_name_attr,
        displayName=rt_display_name,
        parentTemplateId=parent_template_id,
        equipmentSetName=eqp_set_name,
        statsName=companion_name_attr,
        localization_aggregator=director.localization_aggregator,
    )
    # Update equipment file
    updated_equipment = director.update_equipment(
        equipment_set_name=eqp_set_name, equipment_set_type=EquipmentSetType.MELEE_PLATE
    )
    assert updated_equipment, "Failed to update equipment"

    # Update spells
    summon_spell_name = f"LC_Summon_Legendary_Kobold_{unique_suffix}"
    updated_spell_file = director.update_summon_spells(
        display_name="Summon Kobold",
        description="A powerful summoning scroll",
        spell_name=summon_spell_name,
        integration_name="LegendaryCompanions",
        summon_uuid=companion_map_key,
    )
    assert updated_spell_file, "Failed to update spell file"

    # Verify that we didn't add duplicates to the file
    parser = StatsParser(
        filename=MOD_FILENAMES["spell_text_file_summons"], parser_type=ParserType.SPELL
    )
    spell_list = parser.get_entry_names_from_text()
    spells_set: set[str] = set(spell_list)

    assert len(spell_list) == len(spells_set), "Duplicates found in spell file!"

    """
    Book Pages
    """
    ## Summon Page 1
    summon_page_one_stats_name = f"LC_Page_1_{unique_suffix}"
    summon_page_one_rt_id = director.add_page(
        name=summon_page_one_stats_name,
        display_name="Summon page 1",
        description="Summon page description",
        stats_name=summon_page_one_stats_name,
    )
    assert is_valid_uuid(summon_page_one_rt_id), "Failed to add summon page one"

    ## Summon Page 2
    summon_page_two_stats_name = f"LC_Page_2_{unique_suffix}"
    summon_page_two_rt_id = director.add_page(
        name=summon_page_two_stats_name,
        display_name="Summon page 2",
        description="Summon page 2 description",
        stats_name=summon_page_two_stats_name,
    )
    assert is_valid_uuid(summon_page_two_rt_id), "Failed to add summon page two"

    ## Summon Book
    summon_book_stats_name = f"LC_Book_of_Testing_{unique_suffix}"
    summon_book_rt_id = director.add_book(
        name=summon_book_stats_name,
        display_name=f"Book of Testing {unique_suffix}",
        description="A thick leather bound tome",
        stats_name=summon_book_stats_name,
        book_id=unique_suffix,
    )
    assert is_valid_uuid(summon_book_rt_id), "Failed to add summon book"

    """
    Upgrade pages, book, scroll
    """

    # TODO: Upgrade page 1

    # TODO: Upgrade page 2

    # TODO: Upgrade book

    # Upgrade scroll
    upgrade_scroll_rt_name = "LC_Scroll_Upgrade_Companion"
    upgrade_scroll_stats_name = "OBJ_LC_Scroll_Upgrade_Companion"
    upgrade_spell_name = "LC_Upgrade_Companion"
    upgrade_scroll_rt_id = director.add_scroll(
        name=upgrade_scroll_rt_name,
        display_name="Scroll of Revelations",
        description="A glowing scroll, charged with chaotic energy",
        spell_name=upgrade_spell_name,
        stats_name=upgrade_scroll_stats_name,
    )
    assert is_valid_uuid(upgrade_scroll_rt_id), "Invalid upgrade scroll RT id"

    """
    End pages/books
    """

    """
    Combos
    """

    # Summon book combo
    combo_name = f"Book_of_Summoning_Combo_{unique_suffix}"
    updated_item_combos = director.update_item_combos(
        combo_name=combo_name,
        object_one_name=summon_page_one_stats_name,
        object_two_name=summon_page_two_stats_name,
        combo_result_item_name=summon_book_stats_name,
    )
    assert updated_item_combos, "Failed to update item combos file"

    # TODO: Upgrade book combo

    """
    Summon/Upgrade Scrolls
    """
    ## Summon scroll
    summon_scroll_stats_name = f"LC_Scroll_of_Summoning_{unique_suffix}"
    summon_scroll_rt_id = director.add_scroll(
        name=summon_scroll_stats_name,
        display_name="Scroll of Testing",
        description="Scroll description",
        # This must match the summon spell above!
        spell_name=summon_spell_name,
        stats_name=summon_scroll_stats_name,
    )
    assert is_valid_uuid(summon_scroll_rt_id), "Failed to verify scroll RT id"

    ####################################################################
    ################### END OBJECT ENTRIES #############################
    ####################################################################

    wrote_obj_entries = director.stats_object_aggregator.append_entries()
    assert wrote_obj_entries, "Failed to append entries"

    ## Append to root template using the above RTs
    appended_rt = director.append_root_template()
    assert appended_rt, "Failed to append root template"

    # Write book localization file (book contents)
    book_name = f"Book_of_Testing_{unique_suffix}"
    book_contents = "This is a book about how much I love testing"
    unknown_description = "This is the unknown description"
    updated_book_children = director.update_book_file(
        name=book_name,
        content=book_contents,
        unknown_description=unknown_description,
    )
    assert updated_book_children is not None, "Failed to update book localization file"

    ## TODO: move all this stuff into a dedicated verify function?
    book: BookLocaEntry | Literal[
        False
    ] = director.book_loca_aggregator.get_book_with_name(book_name)

    assert book is not False, "Returned False from get_book_with_name"
    assert is_valid_handle_uuid(book.content_handle)
    assert is_valid_handle_uuid(book.unknown_description_handle)

    # Verify book XML
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
                    attrs.attrib["id"] == "UUID" and attrs.attrib["value"] == book_name
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
    # Localization
    parser = LocalizationParser()
    updated_content_list = director.update_localization(parser)
    assert updated_content_list is not None, "Failed to update localization"

    """
    Verify links between different parts of the process.
    1. [✓] Companion RT -> equipment entry
    2. [✓] Pages RTs -> object entry RT
    3. [✓] Book RTs -> object entry RT
    4. [✓] Scroll RT -> object entry RT
    5. Scroll RT summon spell -> spell file
    6. Companion RT DisplayName handle -> localization file
    7. Companion RT Title handle -> localization file
    8. Scroll RT DisplayName -> localization file
    # NOTE: Maybe reuse page descriptions here?
    9. Page 1 RT DisplayName -> localization file
    10. Page 1 RT Description -> localization file
    11. Page 2 RT DisplayName -> localization file
    12. Page 2 RT DisplayName -> localization file
    13. Page 1 name -> combo file
    14. Page 2 name -> combo file
    15. Book name -> combo file
    16. Companion RT -> spell file summon UUID
    """

    # Verify companion RT equipment set is in equipment file
    equipment_parser = EquipmentParser()
    equipment_set_names = equipment_parser.get_entry_names_from_text()
    assert (
        director.companion.equipment_set_name in equipment_set_names
    ), "Failed to very equipment set in file"

    # Verify page RT map key in object file
    stats_parser = StatsParser(
        filename=MOD_FILENAMES["books_object_file"], parser_type=ParserType.BOOK
    )

    # Entry info for all objects
    object_entry_info: dict[str, dict] = stats_parser.get_entry_info_from_text()

    # Map of stats_name -> root template id
    objects_to_verify = {
        summon_page_one_stats_name: summon_page_one_rt_id,
        summon_page_two_stats_name: summon_page_two_rt_id,
        summon_book_stats_name: summon_book_rt_id,
        summon_scroll_stats_name: summon_scroll_rt_id,
        # TODO: add upgrade book pages, book, scroll
    }
    # Verify each object
    for stats_name in objects_to_verify:
        assert (
            stats_name in object_entry_info
        ), f"Failed to find entry name {stats_name}"
        assert (
            objects_to_verify[stats_name]
            == object_entry_info[stats_name]["root_template_id"]
        ), "Root template id mismatch for page 1"

    """
    Verify each spell made it into the file
    1. [✓] Companion summon spell with
    2. [✓] Check companion RT id in the summon spell
    3. Scroll for upgrade spell (just need to check that the spell used
    in the spell is there)
    """
    spell_parser = StatsParser(
        filename=MOD_FILENAMES["spell_text_file_summons"], parser_type=ParserType.SPELL
    )

    # Verify summon spell
    spell_entry_info = spell_parser.get_entry_info_from_text()

    assert (
        summon_spell_name in spell_entry_info
    ), "Failed to find summon spell in spell entry info"
    summon_entry = spell_entry_info[summon_spell_name]

    assert (
        summon_entry["summon_uuid"] == companion_map_key
    ), "Failed to find companion RT in summon spell"
