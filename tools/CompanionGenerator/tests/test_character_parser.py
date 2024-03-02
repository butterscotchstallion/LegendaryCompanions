from companiongenerator.character_parser import CharacterParser
from companiongenerator.logger import logger


def test_char_parser():
    parser = CharacterParser()
    entries = parser.get_entry_names_from_text()

    if not parser.is_file_empty:
        assert len(entries) >= 1
    else:
        logger.error("Empty character file?")
