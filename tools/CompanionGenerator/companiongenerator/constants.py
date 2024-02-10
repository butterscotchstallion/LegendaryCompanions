"""Mod file paths"""
BASE_PATH = "../replica_mod_directory"
PUBLIC_PATH = f"{BASE_PATH}/Public/LegendaryCompanions"
MOD_PATH = f"{BASE_PATH}/Mods/LegendaryCompanions"
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
}
