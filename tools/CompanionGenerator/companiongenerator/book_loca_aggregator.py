from typing import Literal

from companiongenerator.book_loca_entry import BookLocaEntry


class BookLocaAggregator:
    """
    Handles localization entries for books. This is similar
    to LocalizationAggregator, but specifically handles the
    differences to regular localization entries:
    - Books have unique properties
    - Books have a different file and format
    """

    def __init__(self):
        self.entries: list[BookLocaEntry] = []

    def get_book_with_name(self, book_name: str) -> BookLocaEntry | Literal[False]:
        for entry in self.entries:
            if entry.name == book_name:
                return entry
        return False

    def add_book_and_return_book(self, **kwargs) -> BookLocaEntry:
        existing_book = self.get_book_with_name(kwargs["name"])

        if existing_book is not False:
            return existing_book
        else:
            book = BookLocaEntry(**kwargs)
            self.entries.append(book)
            return book
