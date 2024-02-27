from uuid import uuid4

from companiongenerator.equipment_set import EquipmentSet, EquipmentSetType
from companiongenerator.equipment_set_aggregator import EquipmentSetAggregator
from companiongenerator.equipment_set_parser import EquipmentSetParser


def test_eqp_parser():
    """
    Tests parsing of equipment file to get names, and
    updating the file
    """
    parser = EquipmentSetParser()
    aggregator = EquipmentSetAggregator()
    eqp_set_name = f"test_equipment_entry_{uuid4()}"
    aggregator.add_entry(
        EquipmentSet(
            equipment_set_name=eqp_set_name, equipment_set_type=EquipmentSetType.CASTER
        )
    )
    success = aggregator.update_equipment_sets()
    assert success, "Failed to update equipment file"

    eqp_set_names: set[str] = parser.get_entry_names_from_text()

    assert (
        eqp_set_name in eqp_set_names
    ), "Failed to add equipment set (name not found in names)"
