--[[
-- Possible refactor idea to make this harder to break:
-- Add methods for introducing new integrations that check
-- whether this name exists or other duplicate/invalid data.
-- These methods could also throw errors upon encountering
-- unexpected values. Although we should catch this in code
-- review, an automated validation system would be superior.
--]]
local GTY_LEGENDARY_UUID    = '4973f064-fe29-4857-89fb-a18af7a5d02a'
local GTY_RARE_UUID         = 'bbcf8a7b-5630-4ddf-be17-b361d2289218'
local GTY_COMMON_UUID       = 'abc73768-6f98-423d-9bf2-7748e1f93b0e'
local DEFAULT_SUMMON_MESAGE = 'The book glows with power and opens a portal!'
LC['integrations']          = {}

LC['integrations'].insert({
    -- This is the name of your mod
    ['Githzerai'] = {
        -- A list of lore books
        ['books'] = {
            {
                -- Name of this book item from the root template
                ['name']            = 'BOOK_LC_Githzerai_Combined_Tome_3',
                -- Names of the pages that when combined create the above book
                ['pages']           = {
                    'BOOK_LC_Githzerai_TornPage_01',
                    'BOOK_LC_Githzerai_TornPage_02'
                },
                -- This message appears as a message box to inform the user what is going on
                ['summonMessage']   = DEFAULT_SUMMON_MESAGE,
                -- Upon combination of the pages, one of these summoning spells will be cast to summon your companion
                ['summonSpells']    = {
                    {
                        ['name']       = 'LC_Summon_Githzerai_Legendary',
                        ['entityUUID'] = GTY_LEGENDARY_UUID
                    },
                },
                -- When your companion is summoned, it will cast one of these spells on the party
                ['buffPartySpells'] = {
                    'Target_Bless_3_AI',
                },
                -- When your companion is summoned, one of these statuses will be applied to the companion
                ['selfStatus']      = {
                    'WARMAGIC_GITHYANKI',
                }
            }
        }
    }
})
