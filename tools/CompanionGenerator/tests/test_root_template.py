from companiongenerator.root_template import CompanionRT
from companiongenerator.template_fetcher import TemplateFetcher
import xml.etree.ElementTree as ET


def mock_get_companion_template_text():
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
    companion_rt = CompanionRT(
        displayName=display_name,
        description=description,
        statsName=stats_name,
        parentTemplateId=parent_template_id,
        template_fetcher=fetcher,
    )
    attribute_value_map = {
        "DisplayName": display_name,
        "Description": description,
        "Stats": stats_name,
        "ParentTemplateId": parent_template_id,
    }
    rt_xml = companion_rt.get_template_text()
    assert len(rt_xml) > 0
    root = ET.fromstring(rt_xml)
    for child in root:
        if "id" in child.attrib:
            attr_id = child.attrib["id"]
            if "value" in child.attrib:
                value = child.attrib["value"]
            else:
                # DisplayName has a handle and not a value
                value = child.attrib["handle"]

            if id in attribute_value_map:
                assert attribute_value_map[attr_id] == value
