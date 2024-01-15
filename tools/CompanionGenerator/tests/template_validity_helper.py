def assert_template_validity(template: str):
    """
    Basic template replacement validity check
    """
    assert len(template) > 0
    assert "{{" not in template
