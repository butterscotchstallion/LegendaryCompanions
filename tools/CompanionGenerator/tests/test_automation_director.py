from uuid import uuid4

from companiongenerator.automation_director import AutomationDirector
from companiongenerator.root_template_aggregator import RootTemplateAggregator
from companiongenerator.template_fetcher import TemplateFetcher


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
            bookId=uuid4(),
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
        merged_path = f"{director.output_dir_path}/merged.lsf.lsx"
        appended_rt = director.append_root_template(merged_path)
        assert appended_rt, "Failed to append root template"

        # Write book localization file (book contents)
        book_name = "Book of Testing"
        book_contents = "This is a book about how much I love testing"
        unknown_description = "This is the unknown description"
        created_book_loca_file = director.create_book_localization_file(
            name=book_name,
            content=book_contents,
            unknownDescription=unknown_description,
            template_fetcher=TemplateFetcher(),
            localization_aggregator=director.localization_aggregator,
        )
        assert created_book_loca_file, "Failed to create book localization file"
        assert director.localization_aggregator.entry_with_text_exists(book_contents)
        assert director.localization_aggregator.entry_with_handle_exists(
            director.book_content_handle
        )
        assert director.localization_aggregator.entry_with_handle_exists(
            director.book_description_handle
        )

        # Write localization
        created_loca_file = director.create_localization_file()
        assert created_loca_file, "Failed to create localization file"
