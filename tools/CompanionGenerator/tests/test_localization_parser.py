from companiongenerator.file_handler import FileHandler


def test_append_localization_entries():
    """Create backup of localization file and append new entries
    Do not allow duplicate entries
    """
    handler = FileHandler()
    loca_file_path = (
        "../replica_mod_directory/Localization/English/LegendaryCompanions.loca.xml"
    )
    backup_created = handler.create_backup_file(loca_file_path)
    assert backup_created, "Failed to create backup file"

    # Test overwriting last backup file
    overwrote_backup_file = handler.create_backup_file(loca_file_path)
    assert overwrote_backup_file, "Failed to overwrite existing backup file"
