"""Mod file paths"""
BASE_PATH = "../replica_mod_directory"
PUBLIC_PATH = f"{BASE_PATH}/Public/LegendaryCompanions"
STATS_PATH = f"{PUBLIC_PATH}/Stats/Generated"
TAGS_PATH = f"{PUBLIC_PATH}/Tags"
STATS_DATA_PATH = f"{STATS_PATH}/Data"

MOD_FILENAMES: dict = {
    # replica_mod_directory\Public\LegendaryCompanions\RootTemplates\merged.lsf.lsx
    "root_template_merged": f"{PUBLIC_PATH}/RootTemplates/merged.lsf.lsx",
    "localization": f"{BASE_PATH}/Localization/English/LegendaryCompanions.loca.xml",
    "stats": STATS_PATH,
    "stats_data": STATS_DATA_PATH,
    "tags": TAGS_PATH,
}
