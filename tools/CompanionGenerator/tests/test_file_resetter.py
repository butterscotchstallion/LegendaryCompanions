from pathlib import Path

from companiongenerator.file_resetter import FileResetter
from companiongenerator.file_templates import FileTemplates
from companiongenerator.replica_files import ReplicaFiles


def get_tpl_contents(tpl_filename: str):
    return Path(tpl_filename).read_text()


def test_reset_text_file():
    filename = ReplicaFiles.item_combos
    resetter = FileResetter()
    success = resetter.reset_text_file(filename)

    assert success, "Failed to reset text file"

    fh = Path(filename)
    file_contents = fh.read_text()

    assert len(file_contents) == 0, "Failed to reset text file"


def test_reset_root_template():
    resetter = FileResetter()
    success = resetter.reset_root_template()

    assert success, "Failed to reset RT"

    fh = Path(ReplicaFiles.root_template_file)
    file_contents = fh.read_text()

    assert file_contents == get_tpl_contents(FileTemplates.root_template_file)
