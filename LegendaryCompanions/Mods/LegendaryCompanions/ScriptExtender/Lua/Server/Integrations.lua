--[[
-- Possible refactor idea to make this harder to break:
-- Add methods for introducing new integrations that check
-- whether this name exists or other duplicate/invalid data.
-- These methods could also throw errors upon encountering
-- unexpected values. Although we should catch this in code
-- review, an automated validation system would be superior.
--]]
local GTY_LEGENDARY_UUID = '4973f064-fe29-4857-89fb-a18af7a5d02a'
local GTY_RARE_UUID      = 'bbcf8a7b-5630-4ddf-be17-b361d2289218'
local GTY_COMMON_UUID    = 'abc73768-6f98-423d-9bf2-7748e1f93b0e'
local RARITY_COMMON      = 'common'
local RARITY_RARE        = 'rare'
local RARITY_LEGENDARY   = 'legendary'
LC['rarities']           = { RARITY_COMMON, RARITY_RARE, RARITY_LEGENDARY }
LC['integrations']       = {
    ['Githzerai'] = {
        ['books'] = {
            {
                ['rarity']          = 'common',
                ['entityUUIDs']     = {
                    GTY_LEGENDARY_UUID,
                },
                ['name']            = 'BOOK_LC_Githzerai_Combined_Tome_3',
                ['pages']           = {
                    'BOOK_LC_Githzerai_TornPage_01',
                    'BOOK_LC_Githzerai_TornPage_02'
                },
                ['buffPartySpells'] = {
                    'Target_Bless_3_AI',
                },
                ['selfStatus']      = {
                    'WARMAGIC_GITHYANKI',
                }
            }
        },
        [RARITY_COMMON] = {
            ['entityUUIDs']     = {
                GTY_COMMON_UUID,
            },
            ['buffPartySpells'] = {
                'Target_PLA_Githyanki_Rally',
            },
            ['selfStatus']      = {
                'WARMAGIC_GITHYANKI',
            }
        },
        [RARITY_RARE] = {
            ['entityUUIDs']     = {
                GTY_RARE_UUID,
            },
            ['buffPartySpells'] = {
                'Target_PLA_Githyanki_Rally',
            },
            ['selfStatus']      = {
                'WARMAGIC_GITHYANKI',
            }
        },
        [RARITY_LEGENDARY] = {
            ['entityUUIDs']     = {
                GTY_LEGENDARY_UUID,
            },
            ['buffPartySpells'] = {
                'Target_PLA_Githyanki_Rally',
            },
            ['selfStatus']      = {
                'WARMAGIC_GITHYANKI',
            }
        }
    }
}
