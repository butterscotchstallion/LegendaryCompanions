from typing import Literal
from uuid import uuid4

from companiongenerator.automation_director import AutomationDirector
from companiongenerator.book_loca_entry import BookLocaEntry
from companiongenerator.book_parser import BookParser
from companiongenerator.root_template_aggregator import RootTemplateAggregator
from companiongenerator.template_fetcher import TemplateFetcher

from tests.template_validity_helper import is_valid_handle_uuid


def test_create():
    """
    Tests interactions between the automation director and various
    managers in order to create the necessary structures and files
    """
    director = AutomationDirector(is_dry_run=False)
    created_output_dir = director.create_output_dir_if_not_exists()

    assert created_output_dir, "Failed to create output directory"

    if created_output_dir:
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

        # Create spell
        created_spell_file = director.create_summon_spell(
            display_name="Summon Chip Chocolate",
            description="A powerful summoning scroll",
            spell_name="LC_Summon_Legendary_Muffin",
            integration_name="LegendaryCompanions",
            summon_uuid=director.companion.map_key,
            template_fetcher=TemplateFetcher(),
            root_template_aggregator=RootTemplateAggregator(is_dry_run=False),
            is_dry_run=False,
        )
        assert created_spell_file, "Failed to create spell file"

        ## Page 1 RT
        page_one_stats_name = "LC_Page_1"
        director.add_page_rt(
            name=page_one_stats_name,
            displayName="A tattered page",
            description="Page description",
            statsName=page_one_stats_name,
            localization_aggregator=director.localization_aggregator,
            template_fetcher=TemplateFetcher(),
            root_template_aggregator=RootTemplateAggregator(is_dry_run=False),
        )

        ## Page 2 RT
        page_two_stats_name = "LC_Page_2"
        director.add_page_rt(
            name=page_two_stats_name,
            displayName="A tattered page",
            description="Page 2 description",
            statsName=page_two_stats_name,
            localization_aggregator=director.localization_aggregator,
            template_fetcher=TemplateFetcher(),
            root_template_aggregator=RootTemplateAggregator(is_dry_run=False),
        )

        ## Book RT
        book_stats_name = "LC_Book_of_Testing"
        director.add_book_rt(
            name=book_stats_name,
            displayName="Book of Testing",
            description="A thick leather bound tome",
            bookId=str(uuid4()),
            statsName=book_stats_name,
            localization_aggregator=director.localization_aggregator,
            template_fetcher=TemplateFetcher(),
            root_template_aggregator=RootTemplateAggregator(is_dry_run=False),
        )

        # Write item combos
        created_item_combos = director.create_item_combos(
            combo_name="Book_of_Testing_Combo",
            object_one_name=page_one_stats_name,
            object_two_name=page_two_stats_name,
            combo_result_item_name=book_stats_name,
            template_fetcher=TemplateFetcher(),
        )
        assert created_item_combos, "Failed to create item combos file"

        ## Scroll RT
        director.add_scroll_rt(
            name="LC_Scroll_of_Testing",
            displayName="Scroll of Testing",
            description="Scroll description",
            scrollSpellName="LC_Scroll_of_Testing",
            statsName="LC_Scroll_of_Testing",
            localization_aggregator=director.localization_aggregator,
            template_fetcher=TemplateFetcher(),
            root_template_aggregator=RootTemplateAggregator(is_dry_run=False),
        )

        ## Append to root template using the above RTs
        # TODO: REPLACE ME with replica merged path
        merged_path = f"{director.output_dir_path}/merged.lsf.lsx"
        appended_rt = director.append_root_template(merged_path)
        assert appended_rt, "Failed to append root template"

        # Write book localization file (book contents)
        book_name = f"Book of Testing {uuid4()}"
        book_contents = "This is a book about how much I love testing"
        unknown_description = "This is the unknown description"
        updated_book_children = director.update_book_file(
            name=book_name,
            content=book_contents,
            unknown_description=unknown_description,
        )
        assert (
            updated_book_children is not None
        ), "Failed to update book localization file"

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
                        attrs.attrib["id"] == "UUID"
                        and attrs.attrib["value"] == book_name
                    )
                    if book_match:
                        # Handle values use the attribute "handle" for values!
                        if attrs.attrib["id"] == "Content":
                            assert (
                                attrs.attrib["handle"] == book.content_handle
                            ), "Content handle mismatch"
                        if attrs.attrib["id"] == "UnknownDescription":
                            assert (
                                attrs.attrib["handle"]
                                == book.unknown_description_handle
                            ), "Unknown description mismatch"
                        # Stop here because we do not care about other books.
                        break
