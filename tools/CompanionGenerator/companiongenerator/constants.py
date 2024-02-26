"""Mod file paths"""
MOD_NAME = "LegendaryCompanions"
BASE_PATH = "../replica_mod_directory"
PUBLIC_PATH = f"{BASE_PATH}/Public/{MOD_NAME}"
MOD_PATH = f"{BASE_PATH}/Mods/{MOD_NAME}"
BOOKS_PATH = f"{MOD_PATH}/Localization"
STATS_PATH = f"{PUBLIC_PATH}/Stats/Generated"
TAGS_PATH = f"{PUBLIC_PATH}/Tags"
STATS_DATA_PATH = f"{STATS_PATH}/Data"
XML_TEMPLATES = "./companiongenerator/templates"

MOD_FILENAMES: dict[str, str] = {
    # replica_mod_directory\Public\LegendaryCompanions\RootTemplates\merged.lsf.lsx
    "root_template_merged": f"{PUBLIC_PATH}/RootTemplates/merged.lsf.lsx",
    "localization": f"{BASE_PATH}/Localization/English/LegendaryCompanions.loca.xml",
    "stats": STATS_PATH,
    "stats_data": STATS_DATA_PATH,
    "tags": TAGS_PATH,
    "books": f"{BOOKS_PATH}/LegendaryCompanions.lsf.lsx",
    "book_template_file": f"{XML_TEMPLATES}/book_loca_file.xml",
    "spell_text_file_summons": f"{STATS_DATA_PATH}/LC_Summons.txt",
    "item_combos": f"{STATS_PATH}/ItemCombos.txt",
    "books_object_file": f"{STATS_DATA_PATH}/LC_Books.txt",
    "equipment": f"{STATS_PATH}/Equipment.txt",
}

ARCH_MELEE_SMART = "melee_smart"
ARCH_MELEE_SMART_TPL_ID = "39c7c3a9-8393-4df9-9bbf-6d52aa7f34db"
