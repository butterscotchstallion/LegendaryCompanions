from uuid import uuid4

from companiongenerator.stats_object import StatsObject

from tests.template_validity_helper import assert_template_validity


def test_stats_object():
    stats_obj = StatsObject(
        stats_name="LC_object_book_of_testing", root_template_id=str(uuid4())
    )
    stats_obj_text = stats_obj.get_tpl_with_replacements()
    assert_template_validity(stats_obj_text)
