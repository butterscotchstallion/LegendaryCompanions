import xml.etree.ElementTree as ET

from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.file_handler import FileHandler
from companiongenerator.localization_aggregator import LocalizationAggregator
from companiongenerator.localization_entry import LocalizationEntry
from companiongenerator.localization_parser import LocalizationParser
from companiongenerator.logger import logger
from companiongenerator.template_fetcher import TemplateFetcher
from companiongenerator.xml_utils import get_text_from_entries

from tests.template_validity_helper import is_valid_handle_uuid


def verify_localization_added(
    updated_content_list: list[ET.Element],
    loca_entries: set[LocalizationEntry],
) -> bool:
    """Build updated content text list and compare loca entries"""

    # Build text list from both
    updated_content_texts: list[str] = get_text_from_entries(set(updated_content_list))
    loca_texts = get_text_from_entries(loca_entries)

    # Return true if all of the loca entries added exist in the updated list
    return set(loca_texts).issubset(updated_content_texts)


def test_append_localization_entries():
    """Tests backup, appending, and verification

    1. Backup existing localization file
    2. Test overwriting existing localization file
    3. Verify output by testing that all added localization
    entries exist in the output
    """
    handler = FileHandler()
    backup_created = handler.create_backup_file(MOD_FILENAMES["localization"])
    assert backup_created, "Failed to create backup file"

    logger.info("Testing overwriting of backup file")

    # Test overwriting last backup file
    overwrote_backup_file = handler.create_backup_file(MOD_FILENAMES["localization"])
    assert overwrote_backup_file, "Failed to overwrite existing backup file"

    # Get new nodes and append to file
    loca_aggregator = LocalizationAggregator(template_fetcher=TemplateFetcher())
    loca_text = "Tut tut tut tut tut"
    new_handle = loca_aggregator.add_entry_and_return_handle(
        text=loca_text,
        comment="This is a comment about where this localization is used",
    )
    assert is_valid_handle_uuid(new_handle)
    assert len(loca_aggregator.entries) == 1

    # Parse loca XML and return tree for verification
    parser = LocalizationParser()
    entries = loca_aggregator.entries
    content_list = parser.append_entries(MOD_FILENAMES["localization"], entries)

    assert content_list is not None, "Failed to append to loca entries"

    # Verify updated tree
    content_entries = content_list.findall("content")
    verification_ok = verify_localization_added(content_entries, entries)
    assert verification_ok, "Failed to verify loca entries"

    # Write tree
    parser.write_tree()
