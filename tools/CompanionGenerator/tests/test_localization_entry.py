import xml.etree.ElementTree as ET

from companiongenerator.localization_entry import LocalizationEntry

from tests.template_validity_helper import (
    assert_template_validity,
    is_valid_handle_uuid,
)


def test_loca_entry():
    """
    Tests the generation of a localization entry
    """
    loca_value = "Testing localization innit"
    comment = "Test localization comment"
    loca = LocalizationEntry(text=loca_value, comment=comment)
    xml_with_replacements = loca.get_tpl_with_replacements()

    assert_template_validity(xml_with_replacements)
    tag = ET.fromstring(xml_with_replacements)
    xml_lines = xml_with_replacements.splitlines()

    assert tag.text == loca_value, "Localization text mismatch"
    assert is_valid_handle_uuid(tag.attrib["contentuid"]), "Not a handle!"
    assert comment in xml_lines[0], "Missing comment"
