from enum import StrEnum
from typing import TypedDict, Unpack

from companiongenerator.template_replacer_base import TemplateReplacerBase


class EquipmentSetName:
    equipment_set_name: str

    def __init__(self, equipment_set_name: str):
        self.equipment_set_name = equipment_set_name


class EquipmentSetType(StrEnum):
    """
    Matches equipment set type to the corresponding
    template
    """

    MELEE_PLATE = "eqp_caster.txt"
    CASTER = "eqp_caster.txt"


class EquipmentSetKeywords(TypedDict):
    equipment_set_type: EquipmentSetType
    equipment_set_name: str


class EquipmentSet(TemplateReplacerBase):
    """
    Represents an equipment set to add to the equipment
    file
    """

    def __init__(self, **kwargs: Unpack[EquipmentSetKeywords]):
        super().__init__()
        self.equipment_set_name = kwargs["equipment_set_name"]
        self.equipment_set_type = kwargs["equipment_set_type"]
        self.template_filename = self.equipment_set_type
        self.replacements = {"{{equipment_set_name}}": self.equipment_set_name}

    def __repr__(self):
        return self.equipment_set_name
