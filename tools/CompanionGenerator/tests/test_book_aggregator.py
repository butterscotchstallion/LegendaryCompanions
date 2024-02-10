from companiongenerator.book_loca_aggregator import BookLocaAggregator
from companiongenerator.localization_aggregator import LocalizationAggregator

from tests.template_validity_helper import is_valid_handle_uuid


def test_add_book():
    """Tests adding books, getting books, returning handles"""
    content = "Book contents"
    unknown_description = "A dusty old tome"
    book_name = "Book of Muffins"

    book_loca_aggregator = BookLocaAggregator()
    entry = book_loca_aggregator.add_book_and_return_book(
        name=book_name,
        content=content,
        unknown_description=unknown_description,
        localization_aggregator=LocalizationAggregator(),
    )

    assert entry.name == book_name
    assert entry.content == content
    assert entry.unknown_description == unknown_description
    assert len(book_loca_aggregator.entries) == 1, "Failed to add book loca entry"
    assert is_valid_handle_uuid(entry.content_handle)
    assert is_valid_handle_uuid(entry.unknown_description_handle)
