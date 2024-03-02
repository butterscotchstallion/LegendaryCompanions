from companiongenerator.character import Character, CharacterName
from companiongenerator.character_parser import CharacterParser
from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.file_handler import FileHandler
from companiongenerator.logger import logger


class CharacterAggregator:
    entries: set[Character | CharacterName] = set()

    def __init__(self):
        self.filename: str = MOD_FILENAMES["character"]

    def add_entry(self, entry: Character | CharacterName):
        self.entries.add(entry)

    def load_entries_from_file(self):
        parser = CharacterParser()
        character_entry_names = parser.get_entry_names_from_text()

        for entry_name in character_entry_names:
            self.add_entry(CharacterName(stats_name=entry_name))

    def get_eligible_entries(self) -> set[Character]:
        return set([entry for entry in self.entries if isinstance(entry, Character)])

    def get_content_text(self) -> str | None:
        eligible_entries = self.get_eligible_entries()

        logger.info(f"CharacterAggregator: {len(eligible_entries)} eligible entries")

        if len(eligible_entries) > 0:
            return "\n\n".join(
                [entry.get_tpl_with_replacements() for entry in eligible_entries]
            )

    def update_character_file(self) -> bool | None:
        if len(self.entries) > 0:
            content_text = self.get_content_text()
            if content_text:
                handler = FileHandler()
                success = handler.append_to_file(self.filename, content_text)
                if success:
                    logger.info("CharacterAggregator: updated character file")
                else:
                    logger.error("CharacterAggregator: error updating character file")
                return success
            else:
                logger.error("CharacterAggregator: no eligible entries")
        else:
            logger.error("CharacterAggregator: no entries to write")
