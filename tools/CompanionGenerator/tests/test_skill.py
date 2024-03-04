from companiongenerator.skill import Skill

from tests.template_validity_helper import assert_template_validity


def test_skill_template():
    skill_name = "Target_MistyStep"
    skill = Skill(skill_name)
    tpl = skill.get_tpl_with_replacements()
    assert_template_validity(tpl)
