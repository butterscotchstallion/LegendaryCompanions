from uuid import uuid4

from companiongenerator.stats_object import StatsObject
from companiongenerator.stats_object_aggregator import StatsObjectAggregator


def test_stats_obj_aggregator():
    stats_obj_aggregator = StatsObjectAggregator()
    book = StatsObject(stats_name="LC_book_of_testing", root_template_id=str(uuid4()))
    stats_obj_aggregator.add_entry(book)
    assert len(stats_obj_aggregator.entries) == 1

    # Attempt to add duplicate object and make sure it isn't actually added
    stats_obj_aggregator.add_entry(book)
    assert len(stats_obj_aggregator.entries) == 1
