from pathlib import Path
from typing import Literal
from uuid import uuid4

from companiongenerator.automation_director import AutomationDirector
from companiongenerator.book_loca_entry import BookLocaEntry
from companiongenerator.book_parser import BookParser
from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.root_template_aggregator import RootTemplateAggregator
from companiongenerator.stats_object import StatsObject
from companiongenerator.stats_parser import StatsParser
from companiongenerator.template_fetcher import TemplateFetcher

from tests.template_validity_helper import is_valid_handle_uuid


def test_create():
    """
    Tests interactions between the automation director and various
    managers in order to create the necessary structures and files
    """
    director = AutomationDirector(is_dry_run=False)

    ## Companion RT
    director.add_companion_rt(
        title="Legendary Muffin",
        name="Chip Chocolate",
        displayName="Display name",
        parentTemplateId=uuid4(),
        equipmentSetName="LC_EQP_Legendary",
        statsName="LC_Legendary_Muffin",
        localization_aggregator=director.localization_aggregator,
        template_fetcher=TemplateFetcher(),
        root_template_aggregator=RootTemplateAggregator(is_dry_run=False),
    )

    # Update spell
    updated_spell_file = director.update_summon_spells(
        display_name="Summon Kobold",
        description="A powerful summoning scroll",
        spell_name="LC_Summon_Legendary_Kobold",
        integration_name="LegendaryCompanions",
        summon_uuid=director.companion.map_key,
        template_fetcher=TemplateFetcher(),
        root_template_aggregator=RootTemplateAggregator(is_dry_run=False),
        is_dry_run=False,
    )
    assert updated_spell_file, "Failed to update spell file"

    # Verify that we didn't add duplicates to the file
    parser = StatsParser()
    handle = Path(MOD_FILENAMES["spell_text_file_summons"])
    spell_text_file_contents = handle.read_text()
    spell_list = parser.get_entry_names_from_text(spell_text_file_contents)
    spells_set: set[str] = set(spell_list)

    assert len(spell_list) == len(spells_set), "Duplicates found in spell file!"

    ## Page 1 RT
    page_one_stats_name = "LC_Page_1"
    page_one_rt_id = director.add_page_rt(
        name=page_one_stats_name,
        displayName="A tattered page",
        description="Page description",
        statsName=page_one_stats_name,
        localization_aggregator=director.localization_aggregator,
        template_fetcher=TemplateFetcher(),
        root_template_aggregator=RootTemplateAggregator(is_dry_run=False),
    )
    # Add page 1 obj file
    page_1_obj = StatsObject(
        stats_name=page_one_stats_name, root_template_id=page_one_rt_id
    )
    director.stats_object_aggregator.add_entry(page_1_obj)

    ## Page 2 RT
    page_two_stats_name = "LC_Page_2"
    page_2_rt_id = director.add_page_rt(
        name=page_two_stats_name,
        displayName="A tattered page",
        description="Page 2 description",
        statsName=page_two_stats_name,
        localization_aggregator=director.localization_aggregator,
        template_fetcher=TemplateFetcher(),
        root_template_aggregator=RootTemplateAggregator(is_dry_run=False),
    )

    # Add page 2 obj file
    page_2_obj = StatsObject(
        stats_name=page_two_stats_name, root_template_id=page_2_rt_id
    )
    director.stats_object_aggregator.add_entry(page_2_obj)

    ## Book RT
    book_stats_name = "LC_Book_of_Testing"
    book_rt_id = director.add_book_rt(
        name=book_stats_name,
        displayName="Book of Testing",
        description="A thick leather bound tome",
        bookId=str(uuid4()),
        statsName=book_stats_name,
        localization_aggregator=director.localization_aggregator,
        template_fetcher=TemplateFetcher(),
        root_template_aggregator=RootTemplateAggregator(is_dry_run=False),
    )

    # Add book object file
    book_obj = StatsObject(stats_name=book_stats_name, root_template_id=book_rt_id)
    director.stats_object_aggregator.add_entry(book_obj)

    # Write item combos
    updated_item_combos = director.update_item_combos(
        combo_name="Book_of_Testing_Combo",
        object_one_name=page_one_stats_name,
        object_two_name=page_two_stats_name,
        combo_result_item_name=book_stats_name,
        template_fetcher=TemplateFetcher(),
    )
    assert updated_item_combos, "Failed to update item combos file"

    ## Scroll RT
    scroll_stats_name = "LC_Scroll_of_Testing"
    scroll_rt_id = director.add_scroll_rt(
        name="LC_Scroll_of_Testing",
        displayName="Scroll of Testing",
        description="Scroll description",
        scrollSpellName="LC_Scroll_of_Testing",
        statsName=scroll_stats_name,
        localization_aggregator=director.localization_aggregator,
        template_fetcher=TemplateFetcher(),
        root_template_aggregator=RootTemplateAggregator(is_dry_run=False),
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
