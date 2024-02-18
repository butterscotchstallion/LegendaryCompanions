from companiongenerator.equipment_parser import EquipmentParser
from companiongenerator.equipment_set import EquipmentSet, EquipmentSetType


def test_eqp_parser():
    """
    Tests parsing of equipment file to get names, and
    updating the file
    """
    parser = EquipmentParser()
    eqp_set_name = "test_equipment_entry"
    eqp_set = EquipmentSet(
        name=eqp_set_name, equipment_set_type=EquipmentSetType.CASTER
    )
    eqp_set_text = eqp_set.get_tpl_with_replacements()
    success = parser.add_entry(eqp_set_name, eqp_set_text)

    assert success, "Failed to update equipment file"

    eqp_set_names = parser.get_entry_names_from_text()

    assert (
        eqp_set_name in eqp_set_names
    ), "Failed to add equipment set (name not found in names)"
