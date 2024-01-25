import re
import xml.etree.ElementTree as ET


def verify_xml_values(template_xml: str, attribute_value_map: dict) -> None:
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
                if "handle" in child.attrib:
                    value = child.attrib["handle"]
                    # Make sure this is actually a handle and not a value
                    assert is_handle_uuid(value), "not a handle!"

            if attr_id in attribute_value_map:
                assert (
                    attribute_value_map[attr_id] == value
                ), f"Value mismatch in XML: '{value}' != '{attribute_value_map[attr_id]}'"

            # validate UUID
            if "MapKey" in child.attrib:
                assert is_uuid_v4(child.attrib["MapKey"]), "not a UUID!"


def contains_template_symbols(template: str) -> bool:
    return "{{" in template or "}}" in template


def assert_template_validity(template: str):
    """
    Basic template replacement validity check
    """

    assert len(template) > 0
    tpl_lines = template.splitlines()

    for line in tpl_lines:
        if contains_template_symbols(line):
            assert False, f"Line '{line.strip()}' contains template symbol"


def is_uuid_v4(input: str) -> bool:
    """
    Matches uuidv4 strings
    """
    pattern = re.compile(
        "/^[0-9A-F]{8}-[0-9A-F]{4}-[4][0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$/i"
    )
    return pattern.match(pattern)


def is_handle_uuid(input: str) -> bool:
    """
    This isn't really comprehensive but it's good enough
    """
    return len(input) == 37 and input[0] == "h" and "-" not in input
