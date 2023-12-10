--[[
-- Possible refactor idea to make this harder to break:
-- Add methods for introducing new integrations that check
-- whether this name exists or other duplicate/invalid data.
-- These methods could also throw errors upon encountering
-- unexpected values. Although we should catch this in code
-- review, an automated validation system would be superior.
--]]
local RARITY_COMMON         = 'common'
local RARITY_RARE           = 'rare'
local RARITY_LEGENDARY      = 'legendary'
local DEFAULT_SUMMON_MESAGE = 'The book glows with power and opens a portal!'

-- Gith'zerai
LC['integrationManager'].addIntegration({
    ['name']  = 'FollowersOfZerthimon',
    -- A list of lore books
    ['books'] = {
        {
            -- Name of this book item from the root template
            ['name']            = 'BOOK_LC_Githzerai_Combined_Tome_3',
            -- Names of the pages that when combined create the above book
            ['pages']           = {
                'BOOK_LC_Githzerai_TornPage_01',
                'BOOK_LC_Githzerai_TornPage_02',
            },
            -- This message appears as a message box to inform the user what is going on
            ['summonMessage']   = DEFAULT_SUMMON_MESAGE,
            -- Upon combination of the pages, one of these summoning spells will be cast randomly
            -- to summon your companion
            ['summonSpells']    = {
                {
                    -- Name of the summoning spell in LC_Summons.txt
                    ['name']       = 'LC_Summon_Githzerai_Legendary',
                    -- This should match the UUID of the character
                    ['entityUUID'] = '4973f064-fe29-4857-89fb-a18af7a5d02a',
                    -- This determines the power level and lifetime of the summoned
                    -- companion
                    ['rarity']     = RARITY_LEGENDARY,
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
})

-- RSO
LC['integrationManager'].addIntegration({
    ['name']  = 'RS_Slim_Outfit_Series',
    -- A list of lore books
    ['books'] = {
        {
            -- Name of this book item from the root template
            ['name']            = 'BOOK_LC_RSO_Combined_Tome',
            -- Names of the pages that when combined create the above book
            ['pages']           = {
                'BOOK_LC_RSO_TornPage_01',
                'BOOK_LC_RSO_TornPage_02',
            },
            -- This message appears as a message box to inform the user what is going on
            ['summonMessage']   = DEFAULT_SUMMON_MESAGE,
            -- Upon combination of the pages, one of these summoning spells will be cast randomly
            -- to summon your companion
            ['summonSpells']    = {
                {
                    -- Name of the summoning spell in LC_Summons.txt
                    ['name']       = 'LC_Summon_RSO_Legendary',
                    -- This should match the UUID of the character
                    ['entityUUID'] = '52db9322-b223-48fd-ac88-e465efa0c736',
                    -- This determines the power level and lifetime of the summoned
                    -- companion
                    ['rarity']     = RARITY_LEGENDARY,
                },
            },
            -- When your companion is summoned, it will cast one of these spells on the party
            ['buffPartySpells'] = {
                'LC_Target_Longstrider_AOE',
            },
            -- When your companion is summoned, one of these statuses will be applied to the companion
            ['selfStatus']      = {

            }
        }
    }
})
