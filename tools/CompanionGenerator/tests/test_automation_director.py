from pathlib import Path
from typing import Literal
from uuid import uuid4

from companiongenerator.automation_director import AutomationDirector
from companiongenerator.book_loca_entry import BookLocaEntry
from companiongenerator.book_parser import BookParser
from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.equipment_set import EquipmentSetType
from companiongenerator.root_template_aggregator import RootTemplateAggregator
from companiongenerator.stats_object import StatsObject
from companiongenerator.stats_parser import ParserType, StatsParser

from tests.template_validity_helper import is_valid_handle_uuid


def test_create():
    """
    Tests interactions between the automation director and various
    managers in order to create the necessary structures and files
    """
    director = AutomationDirector()
    unique_suffix = str(uuid4())[0:6]

    ## Companion RT
    eqp_set_name = "LC_EQP_Legendary"
    # TODO: change this to something real. Maybe an enumeration
    parent_template_id = uuid4()
    # Name attribute, not display name
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
        root_template_aggregator=RootTemplateAggregator(),
    )

    # Update equipment file
    updated_equipment = director.update_equipment(
        equipment_set_name=eqp_set_name, equipment_set_type=EquipmentSetType.MELEE_PLATE
    )

    assert updated_equipment, "Failed to update equipment"

    # Update spell
    summon_spell_name = f"LC_Summon_Legendary_Kobold_{unique_suffix}"
    updated_spell_file = director.update_summon_spells(
        display_name="Summon Kobold",
        description="A powerful summoning scroll",
        spell_name=summon_spell_name,
        integration_name="LegendaryCompanions",
        summon_uuid=companion_map_key,
        root_template_aggregator=RootTemplateAggregator(),
    )
    assert updated_spell_file, "Failed to update spell file"

    # Verify that we didn't add duplicates to the file
    parser = StatsParser(
        filename=MOD_FILENAMES["spell_text_file_summons"], parser_type=ParserType.SPELL
    )
    handle = Path(MOD_FILENAMES["spell_text_file_summons"])
    spell_text_file_contents = handle.read_text()
    spell_list = parser.get_entry_names_from_text(spell_text_file_contents)
    spells_set: set[str] = set(spell_list)

    assert len(spell_list) == len(spells_set), "Duplicates found in spell file!"

    ## Page 1 RT
    page_one_stats_name = f"LC_Page_1_{unique_suffix}"
    page_one_rt_id = director.add_page_rt(
        name=page_one_stats_name,
        displayName="A tattered page",
        description="Page description",
        statsName=page_one_stats_name,
        localization_aggregator=director.localization_aggregator,
        root_template_aggregator=RootTemplateAggregator(),
    )
    # Add page 1 obj file
    page_1_obj = StatsObject(
        stats_name=page_one_stats_name, root_template_id=page_one_rt_id
    )
    director.stats_object_aggregator.add_entry(page_1_obj)

    ## Page 2 RT
    page_two_stats_name = f"LC_Page_2_{unique_suffix}"
    page_2_rt_id = director.add_page_rt(
        name=page_two_stats_name,
        displayName="A tattered page",
        description="Page 2 description",
        statsName=page_two_stats_name,
        localization_aggregator=director.localization_aggregator,
        root_template_aggregator=RootTemplateAggregator(),
    )

    # Add page 2 obj file
    page_2_obj = StatsObject(
        stats_name=page_two_stats_name, root_template_id=page_2_rt_id
    )
    director.stats_object_aggregator.add_entry(page_2_obj)

    ## Book RT
    book_stats_name = f"LC_Book_of_Testing_{unique_suffix}"
    book_rt_id = director.add_book_rt(
        name=book_stats_name,
        displayName="Book of Testing",
        description="A thick leather bound tome",
        bookId=str(uuid4()),
        statsName=book_stats_name,
        localization_aggregator=director.localization_aggregator,
        root_template_aggregator=RootTemplateAggregator(),
    )

    # Add book object file
    book_obj = StatsObject(stats_name=book_stats_name, root_template_id=book_rt_id)
    director.stats_object_aggregator.add_entry(book_obj)

    # Write item combos
    combo_name = f"Book_of_Testing_Combo_{unique_suffix}"
    updated_item_combos = director.update_item_combos(
        combo_name=combo_name,
        object_one_name=page_one_stats_name,
        object_two_name=page_two_stats_name,
        combo_result_item_name=book_stats_name,
    )
    assert updated_item_combos, "Failed to update item combos file"

    ## Scroll RT
    scroll_stats_name = f"LC_Scroll_of_Testing_{unique_suffix}"
    scroll_rt_id = director.add_scroll_rt(
        name=scroll_stats_name,
        displayName="Scroll of Testing",
        description="Scroll description",
        scrollSpellName=scroll_stats_name,
        statsName=scroll_stats_name,
        localization_aggregator=director.localization_aggregator,
        root_template_aggregator=RootTemplateAggregator(),
    )
    # Add scroll object file
    scroll_obj = StatsObject(
        stats_name=scroll_stats_name, root_template_id=scroll_rt_id
    )
    director.stats_object_aggregator.add_entry(scroll_obj)

    ####################################################################
    ################### END OBJECT ENTRIES #############################
    ####################################################################

    wrote_obj_entries = director.stats_object_aggregator.append_entries()
    assert wrote_obj_entries, "Failed to append entries"

    ## Append to root template using the above RTs
    appended_rt = director.append_root_template()
    assert appended_rt, "Failed to append root template"

    # Write book localization file (book contents)
    book_name = "Book of Testing"
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


def verify_links():
    """
    Verify links between different parts of the process.
    1. Companion RT -> equipment entry
    2. Pages RTs -> object entry RT
    3. Books RTs -> object entry RT
    4. Scroll RT -> object entry RT
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
    pass
