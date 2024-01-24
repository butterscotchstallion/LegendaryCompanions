from companiongenerator.localization_manager import (
    LocalizationManager,
)
from companiongenerator.template_fetcher import TemplateFetcher

from tests.template_validity_helper import is_handle_uuid


def test_add_entry():
    loca_mgr = LocalizationManager()
    new_handle = loca_mgr.add_entry_and_return_handle(
        text="Shake that brass!",
        comment="Test comment",
        template_fetcher=TemplateFetcher(),
    )

    assert is_handle_uuid(
        new_handle
    ), "add_entry_and_return_handle returned a non-handle!"

    # TODO: test retrieval of entries here
