from companiongenerator.localization_entry import LocalizationEntry
from companiongenerator.template_fetcher import TemplateFetcher
from tests.template_validity_helper import assert_template_validity
import xml.etree.ElementTree as ET


def mock_loca_xml():
    """
    Returns XML for loca
    """
    return """
        <!-- {{comment}} -->
        <content contentuid="{{handle}}" version="1">{{text}}</content>
    """


def test_loca_entry(mocker):
    """
    Tests the generation of a localization entry
    """
    fetcher = TemplateFetcher()
    mocker.patch.object(fetcher, "get_template_text", return_value=mock_loca_xml())
    loca_value = "Testing localization innit"
    comment = "Test localization comment"
    loca = LocalizationEntry(text=loca_value, comment=comment, template_fetcher=fetcher)
    xml_with_replacements = loca.get_tpl_with_replacements()

    assert_template_validity(xml_with_replacements)
    tag = ET.fromstring(xml_with_replacements)
    xml_lines = xml_with_replacements.splitlines()

    assert tag.text == loca_value
    assert len(tag.attrib["contentuid"]) == 37
    assert comment in xml_lines[0]
