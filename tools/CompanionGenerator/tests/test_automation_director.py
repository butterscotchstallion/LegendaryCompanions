from uuid import uuid4

from companiongenerator.automation_director import AutomationDirector
from companiongenerator.localization_manager import LocalizationManager
from companiongenerator.template_fetcher import TemplateFetcher


def test_create():
    director = AutomationDirector(is_dry_run=False)
    created_output_dir = director.create_output_dir_if_not_exists()

    assert created_output_dir, "Failed to create output directory"

    if created_output_dir:
        created_spell_file = director.create_summon_spell(
            display_name="Summon Chip Chocolate",
            description="A powerful summoning scroll",
            spell_name="LC_Summon_Legendary_Muffin",
            integration_name="LegendaryCompanions",
            summon_uuid=str(uuid4()),
            template_fetcher=TemplateFetcher(),
            localization_manager=LocalizationManager(),
            is_dry_run=False,
        )
        assert created_spell_file, "Failed to create spell file"
