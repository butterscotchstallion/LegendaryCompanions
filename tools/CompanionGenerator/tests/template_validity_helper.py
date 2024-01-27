import xml.etree.ElementTree as ET
from uuid import UUID


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
                    assert is_valid_handle_uuid(value), "not a handle!"

            if attr_id in attribute_value_map:
                assert (
                    attribute_value_map[attr_id] == value
                ), f"Value mismatch in XML: '{value}' != '{attribute_value_map[attr_id]}'"

            # validate UUID
            if "MapKey" in child.attrib:
                assert is_valid_uuid(child.attrib["MapKey"]), "not a UUID!"


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


def is_valid_handle_uuid(input: str) -> bool:
    """
    This isn't really comprehensive but it's good enough
    """
    return len(input) == 37 and input[0] == "h" and "-" not in input


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.

     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

     Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """

    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test
