from companiongenerator.root_template import BookRT, CompanionRT, PageRT
from companiongenerator.template_fetcher import TemplateFetcher
import xml.etree.ElementTree as ET

from tests.template_validity_helper import assert_template_validity


def verify_xml_values(template_xml: str, attribute_value_map: dict):
    """
    Parses XML string and iterates children, testing
    values against a provided map
    """
    root = ET.fromstring(template_xml)
    for child in root:
        if "id" in child.attrib:
            attr_id = child.attrib["id"]
            if "value" in child.attrib:
                value = child.attrib["value"]
            else:
                # DisplayName has a handle and not a value
                value = child.attrib["handle"]

            if attr_id in attribute_value_map:
                assert attribute_value_map[attr_id] == value

            # validate UUID
            if "MapKey" in child.attrib:
                assert len(child.attrib["MapKey"]) == 36


def mock_get_book_template_text():
    """
    A subset of the book template
    """
    return """
        <node id="GameObjects"> {{name}}
            <attribute id="Description" type="TranslatedString" handle="{{description}}" version="1" />
            <attribute id="DisplayName" type="TranslatedString" handle="{{displayName}}" version="1" />
            <attribute id="Flag" type="int32" value="0" />
            <attribute id="Icon" type="FixedString" value="{{icon}}" />
            <attribute id="LevelName" type="FixedString" value="" />
            <attribute id="MapKey" type="FixedString" value="{{mapKey}}" />
            <attribute id="Name" type="LSString" value="{{name}}" />
            <attribute id="ParentTemplateId" type="FixedString" value="23f65dff-a1ca-42fb-91ee-4cbb69450336" />
            <attribute id="PhysicsTemplate" type="FixedString" value="74eb44d4-f1a9-c08c-fd8a-4cc98285f2c2" />
            <attribute id="Stats" type="FixedString" value="{{statsName}}" />
            <attribute id="Type" type="FixedString" value="item" />
            <attribute id="VisualTemplate" type="FixedString" value="224e8aa7-8011-e18d-1a4a-ea5f83636769" />
            <children>
                <node id="OnUsePeaceActions">
                    <children>
                        <node id="Action">
                            <attribute id="ActionType" type="int32" value="11" />
                            <children>
                                <node id="Attributes">
                                    <attribute id="Animation" type="FixedString" value="" />
                                    <attribute id="BookId" type="FixedString" value="{{bookId}}" />
                                    <attribute id="Conditions" type="LSString" value="" />
                                </node>
                            </children>
                        </node>
                    </children>
                </node>
            </children>
        </node>
    """


def mock_get_companion_template_text():
    """
    A subset of the companion template
    """
    return """
        <node id="GameObjects">
            <attribute id="Archetype" type="FixedString" value="{{archetypeName}}" />
            <attribute id="DisplayName" type="TranslatedString" handle="{{displayName}}" version="1" />
            <attribute id="Equipment" type="FixedString" value="{{equipmentSetName}}" />
            <attribute id="MapKey" type="FixedString" value="{{mapKey}}" />
            <attribute id="Name" type="LSString" value="{{name}}" />
            <attribute id="Type" type="FixedString" value="character" />
            <attribute id="Stats" type="FixedString" value="{{statsName}}" />
            <attribute id="Title" type="TranslatedString" handle="{{title}}" version="1" />
            <attribute id="ParentTemplateId" type="FixedString" value="{{parentTemplateId}}" />
            <children>
                <node id="Tags">
                    <children>
                        {{tagList}}
                    </children>
                </node>
            </children>
        </node>
    """


def test_generate_companion_rt(mocker):
    fetcher = TemplateFetcher()
    mocker.patch.object(
        fetcher, "get_template_text", return_value=mock_get_companion_template_text()
    )
    display_name = "Chip Chocolate"
    description = "Legendary Muffin"
    stats_name = "LC_Legendary_Muffin"
    parent_template_id = "1234"
    equipment_set_name = "LC_EQP_Legendary_Muffin"
    companion_rt = CompanionRT(
        name=stats_name,
        displayName=display_name,
        statsName=stats_name,
        parentTemplateId=parent_template_id,
        template_fetcher=fetcher,
        equipmentSetName=equipment_set_name,
        title=description,
    )
    attribute_value_map = {
        "DisplayName": display_name,
        "Description": description,
        "Stats": stats_name,
        "ParentTemplateId": parent_template_id,
        "Name": stats_name,
        "EquipmentSetName": equipment_set_name,
        "Title": description,
    }
    xml_with_replacements = companion_rt.get_tpl_with_replacements()

    assert_template_validity(xml_with_replacements)
    verify_xml_values(xml_with_replacements, attribute_value_map)


def mock_get_page_template_text():
    """
    A subset of the book page template
    """
    return """
        <node id="GameObjects"> {{name}}
            <attribute id="Description" type="TranslatedString" handle="{{description}}" version="1" />
            <attribute id="DisplayName" type="TranslatedString" handle="{{displayName}}" version="1" />
            <attribute id="Icon" type="FixedString" value="{{icon}}" />
            <attribute id="LevelName" type="FixedString" value="" />
            <attribute id="MapKey" type="FixedString" value="{{mapKey}}" />
            <attribute id="Name" type="LSString" value="{{name}}" />
            <attribute id="ParentTemplateId" type="FixedString" value="c9e45e5a-f089-480b-ab3a-7f5f76dccc3b" />
            <attribute id="PhysicsTemplate" type="FixedString" value="f0d3d875-69c8-e61d-7339-5606a22f8ed2" />
            <attribute id="Stats" type="FixedString" value="{{statsName}}" />
            <attribute id="Type" type="FixedString" value="item" />
            <attribute id="VisualTemplate" type="FixedString" value="d9dc6f6d-a431-2200-5a3b-36f04573e7d5" />
        </node>
    """


def test_generate_page_xml(mocker):
    """
    Tests generation of book pages
    """
    fetcher = TemplateFetcher()
    mocker.patch.object(
        fetcher, "get_template_text", return_value=mock_get_page_template_text()
    )
    display_name = "Page 1"
    description = "A tattered page"
    stats_name = "OBJ_LC_Page_1"
    icon_name = "book_icon_name"
    companion_rt = PageRT(
        displayName=display_name,
        description=description,
        statsName=stats_name,
        name=stats_name,
        icon=icon_name,
        template_fetcher=fetcher,
    )
    attribute_value_map = {
        "DisplayName": display_name,
        "Description": description,
        "Stats": stats_name,
        "Name": stats_name,
        "Icon": icon_name,
    }
    xml_with_replacements = companion_rt.get_tpl_with_replacements()

    assert_template_validity(xml_with_replacements)
    verify_xml_values(xml_with_replacements, attribute_value_map)


def test_generate_book_xml(mocker):
    """
    Tests generation of books
    """
    fetcher = TemplateFetcher()
    mocker.patch.object(
        fetcher, "get_template_text", return_value=mock_get_book_template_text()
    )
    display_name = "The Legend of Chip Chocolate"
    description = "A legendary muffin wizard"
    stats_name = "OBJ_LC_BOOK_1"
    icon_name = "Item_BOOK_GEN_Book_C"
    book_id = "LC_BOOK_Legendary_Muffin"
    companion_rt = BookRT(
        displayName=display_name,
        description=description,
        statsName=stats_name,
        name=stats_name,
        icon=icon_name,
        bookId=book_id,
        template_fetcher=fetcher,
    )
    attribute_value_map = {
        "DisplayName": display_name,
        "Description": description,
        "Stats": stats_name,
        "Name": stats_name,
        "Icon": icon_name,
    }
    xml_with_replacements = companion_rt.get_tpl_with_replacements()

    assert_template_validity(xml_with_replacements)
    verify_xml_values(xml_with_replacements, attribute_value_map)
