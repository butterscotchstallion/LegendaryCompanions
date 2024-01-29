from uuid import uuid4

from companiongenerator.automation_director import AutomationDirector
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
        # Write root templates
        ## Companion RT
        created_companion_rt = director.create_companion_rt(
            title="Legendary Muffin",
            name="Chip Chocolate",
            displayName="Display name",
            parentTemplateId=uuid4(),
            equipmentSetName="LC_EQP_Legendary",
            statsName="LC_Legendary_Muffin",
            localization_manager=director.loca_mgr,
            template_fetcher=TemplateFetcher(),
        )
        assert created_companion_rt, "Failed to create companion RT"

        # Create spell
        created_spell_file = director.create_summon_spell(
            display_name="Summon Chip Chocolate",
            description="A powerful summoning scroll",
            spell_name="LC_Summon_Legendary_Muffin",
            integration_name="LegendaryCompanions",
            summon_uuid=director.companion.map_key,
            template_fetcher=TemplateFetcher(),
            is_dry_run=False,
        )
        assert created_spell_file, "Failed to create spell file"

        ## Page 1 RT
        page_one_stats_name = "LC_Page_1"
        created_page_one_rt = director.create_page_rt(
            name=page_one_stats_name,
            displayName="A tattered page",
            description="Page description",
            statsName=page_one_stats_name,
            localization_manager=director.loca_mgr,
            template_fetcher=TemplateFetcher(),
        )
        assert created_page_one_rt, "Failed to create page one RT"

        ## Page 2 RT
        page_two_stats_name = "LC_Page_2"
        created_page_two_rt = director.create_page_rt(
            name=page_two_stats_name,
            displayName="A tattered page",
            description="Page 2 description",
            statsName=page_two_stats_name,
            localization_manager=director.loca_mgr,
            template_fetcher=TemplateFetcher(),
        )
        assert created_page_two_rt, "Failed to create page two RT"

        ## Book RT
        book_stats_name = "LC_Book_of_Testing"
        created_book_rt = director.create_book_rt(
            name=book_stats_name,
            displayName="Book of Testing",
            description="A thick leather bound tome",
            bookId=uuid4(),
            statsName=book_stats_name,
            localization_manager=director.loca_mgr,
            template_fetcher=TemplateFetcher(),
        )
        assert created_book_rt, "Failed to create book RT"

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
        created_scroll_rt = director.create_scroll_rt(
            name="LC_Scroll_of_Testing",
            displayName="Scroll of Testing",
            description="Scroll description",
            scrollSpellName="LC_Scroll_of_Testing",
            statsName="LC_Scroll_of_Testing",
            localization_manager=director.loca_mgr,
            template_fetcher=TemplateFetcher(),
        )
        assert created_scroll_rt, "Failed to create scroll RT"

        # Write localization
        created_loca_file = director.create_localization_file()
        assert created_loca_file, "Failed to create localization file"

        # Write book localization file (book contents)
        created_book_loca_file = director.create_book_localization_file(
            name="Book of Testing",
            content="This is a book about how much I love testing",
            unknownDescription="This is the unknown description",
            template_fetcher=TemplateFetcher(),
        )
        assert created_book_loca_file, "Failed to create book localization file"
