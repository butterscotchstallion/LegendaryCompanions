local GTY_LEGENDARY_UUID = '4973f064-fe29-4857-89fb-a18af7a5d02a'
local GTY_RARE_UUID      = 'bbcf8a7b-5630-4ddf-be17-b361d2289218'
local GTY_COMMON_UUID    = 'abc73768-6f98-423d-9bf2-7748e1f93b0e'

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
        ['common'] = {
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
        ['rare'] = {
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
        ['legendary'] = {
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
