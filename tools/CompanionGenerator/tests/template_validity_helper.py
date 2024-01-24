import re


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
