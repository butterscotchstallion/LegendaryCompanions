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
        # Create spell
        created_spell_file = director.create_summon_spell(
            display_name="Summon Chip Chocolate",
            description="A powerful summoning scroll",
            spell_name="LC_Summon_Legendary_Muffin",
            integration_name="LegendaryCompanions",
            summon_uuid=str(uuid4()),
            template_fetcher=TemplateFetcher(),
            is_dry_run=False,
        )
        assert created_spell_file, "Failed to create spell file"

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

        # Write item combos
        created_item_combos = director.create_item_combos(
            combo_name="Test combo",
            object_one_name="Object one",
            object_two_name="Object two name",
            combo_result_item_name="Combo result",
            template_fetcher=TemplateFetcher(),
        )
        assert created_item_combos, "Failed to create item combos file"

        # Write root templates
