from dataclasses import dataclass

TEMPLATE_DIR = "companiongenerator/templates"


@dataclass(frozen=True)
class FileTemplates:
    item_combos_file = f"{TEMPLATE_DIR}/ItemCombos.txt"
    book_loca_entry = f"{TEMPLATE_DIR}/book_loca_entry.xml"
    book_loca_file = f"{TEMPLATE_DIR}/book_loca_file.xml"
    character_mindflayer = f"{TEMPLATE_DIR}/character_mindflayer.txt"
    eqp_caster_file = f"{TEMPLATE_DIR}/eqp_caster.txt"
    eqp_melee_plate = f"{TEMPLATE_DIR}/eqp_melee_plate.txt"
    loca_file = f"{TEMPLATE_DIR}/loca_file.xml"
    loca_entry = f"{TEMPLATE_DIR}/localization_entry.xml"
    root_template_file = f"{TEMPLATE_DIR}/merged.lsx"
    object_book = f"{TEMPLATE_DIR}/object_book.txt"
    rt_companion_entry = f"{TEMPLATE_DIR}/rt_companion.xml"
    rt_object_book = f"{TEMPLATE_DIR}/rt_object_book.xml"
    rt_object_page = f"{TEMPLATE_DIR}/rt_object_page.xml"
    rt_object_scroll = f"{TEMPLATE_DIR}/rt_object_scroll.xml"
    skill_entry = f"{TEMPLATE_DIR}/skill.xml"
    summon_spell = f"{TEMPLATE_DIR}/summon_spell.txt"
