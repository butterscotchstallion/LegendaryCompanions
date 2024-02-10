from companiongenerator.book_loca_entry import BookLocaEntry
from companiongenerator.localization_aggregator import LocalizationAggregator

from tests.template_validity_helper import assert_template_validity, verify_xml_values


def test_book_loca_entry():
    """
    Tests the entry in the localization file for books
    """
    content = "Book contents"
    unknown_description = "A dusty old tome"
    book_name = "Book of Muffins"
    book_loca_entry = BookLocaEntry(
        content=content,
        unknown_description=unknown_description,
        name=book_name,
        localization_aggregator=LocalizationAggregator(),
    )
    attribute_value_map = {
        "Content": book_loca_entry.content_handle,
        "UnknownDescription": book_loca_entry.unknown_description_handle,
        "Name": book_name,
    }
    xml_with_replacements = book_loca_entry.get_tpl_with_replacements()

    assert_template_validity(xml_with_replacements)
    verify_xml_values(xml_with_replacements, attribute_value_map)
