--[[
Integrations

Adds integrations via IntegrationManager and
validates each added configuration

]]
local rarityCommon         = 'common'
local rarityRare           = 'rare'
local rarityLegendary      = 'legendary'
local defaultSummonMessage = 'The book glows with power and opens a portal!'

-- Gith'zerai
LC['integrationManager'].AddIntegration({
    -- This should be the name of your mod
    ['name']    = 'FollowersOfZerthimon',
    --This will be set to false if validation fails
    ['enabled'] = true,
    -- A list of lore books
    ['books']   = {
        {
            -- Name of this book item from the root template
            ['name']            = 'BOOK_LC_Githzerai_Combined_Tome_3',
            -- Names of the pages that when combined create the above book
            ['pages']           = {
                'BOOK_LC_Githzerai_TornPage_01',
                'BOOK_LC_Githzerai_TornPage_02',
            },
            -- This message appears as a message box to inform the user what is going on
            ['summonMessage']   = defaultSummonMessage,
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
                    ['rarity']     = rarityLegendary,
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
        },
    }
})

-- RSO
LC['integrationManager'].AddIntegration({
    ['name']    = 'RS_Slim_Outfit_Series',
    --This will be set to false if validation fails
    ['enabled'] = false,
    -- A list of lore books
    ['books']   = {
        {
            -- Name of this book item from the root template
            ['name']            = 'BOOK_LC_RSO_Combined_Tome',
            -- Names of the pages that when combined create the above book
            ['pages']           = {
                'BOOK_LC_RSO_TornPage_01',
                'BOOK_LC_RSO_TornPage_02',
            },
            -- This message appears as a message box to inform the user what is going on
            ['summonMessage']   = defaultSummonMessage,
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
                    ['rarity']     = rarityLegendary,
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

-- Muffin
local muffinLegendaryUUID = '82ffc8c7-644c-40a8-b4b7-2d73b1a1049b'
LC['integrationManager'].AddIntegration({
    ['name']    = 'LC_Muffin_Integration',
    --This will be set to false if validation fails
    ['enabled'] = true,
    -- A list of lore books
    ['books']   = {
        {
            -- Name of this book item from the root template
            ['name']            = 'BOOK_LC_Muffin_Combined_Tome',
            -- Names of the pages that when combined create the above book
            ['pages']           = {
                'BOOK_LC_Muffin_TornPage_01',
                'BOOK_LC_Muffin_TornPage_02',
            },
            -- This message appears as a message box to inform the user what is going on
            ['summonMessage']   = defaultSummonMessage,
            -- Upon combination of the pages, one of these summoning spells will be cast randomly
            -- to summon your companion
            ['summonSpells']    = {
                {
                    -- Name of the summoning spell in LC_Summons.txt
                    ['name']       = 'LC_Summon_Muffin_Legendary',
                    -- This should match the UUID of the character
                    ['entityUUID'] = muffinLegendaryUUID,
                    -- This determines the power level and lifetime of the summoned
                    -- companion
                    ['rarity']     = rarityLegendary,
                },
            },
            -- When your companion is summoned, it will cast one of these spells on the party
            ['buffPartySpells'] = {
                'LC_Target_FalseLife_AOE',
            },
            -- When your companion is summoned, one of these statuses will be applied to the companion
            ['selfStatus']      = {
                'UND_GLUT_ENRAGE'
            }
        },
        --Upgrade book
        {
            -- Name of this book item from the root template
            ['name']    = 'BOOK_LC_Muffin_Combined_Upgrade_Tome',
            -- Names of the pages that when combined create the above book
            ['pages']   = {
                'BOOK_LC_Muffin_Upgrade_TornPage_01',
                'BOOK_LC_Muffin_Upgrade_TornPage_02',
            },
            --If this field is here, this is an upgrade book
            ['upgrade'] = {
                --This should match the UUID of the character
                ['entityUUID'] = muffinLegendaryUUID,
                ['message']    = 'Your companion has been upgraded!',
                ['setLevelTo'] = 5,
                ['passives']   = {
                    'DangerSense',
                    'FastMovement',
                    'FiendishBlessing',
                }
            },
        }
    }
})

--Do not change below.

-- Invalid config for testing errors
LC['integrationManager'].AddIntegration({
    ['name']    = 'LC_Debug_Integration',
    --This will be set to false if validation fails
    ['enabled'] = true,
    -- A list of lore books
    ['books']   = {
        {
            -- Name of this book item from the root template
            ['name']            = 'LC_Book_of_Debugging',
            -- Names of the pages that when combined create the above book
            ['pages']           = {

            },
            -- Upon combination of the pages, one of these summoning spells will be cast randomly
            -- to summon your companion
            ['summonSpells']    = {

            },
            -- When your companion is summoned, it will cast one of these spells on the party
            ['buffPartySpells'] = {

            },
            -- When your companion is summoned, one of these statuses will be applied to the companion
            ['selfStatus']      = {

            }
        }
    }
})
