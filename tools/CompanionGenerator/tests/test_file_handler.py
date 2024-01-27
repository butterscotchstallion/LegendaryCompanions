from uuid import uuid4

from companiongenerator.file_handler import FileHandler


def test_create_output_dir():
    """
    Tests writing and editing of mod files
    """
    try:
        base_path = "../output/"
        dir_name = str(uuid4())
        output_dir_name = f"{base_path}{dir_name}"
        fhandler = FileHandler(is_dry_run=False)
        success = fhandler.create_output_dir(output_dir_name)
        assert success, "Failed to create directory!"
    except IOError:
        assert False, "Error writing file"
