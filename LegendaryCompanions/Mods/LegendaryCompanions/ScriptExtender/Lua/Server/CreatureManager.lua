--[[
CreatureManager - Handles spawning of creatures and related
functionality
]]
---@diagnostic disable-next-line: redundant-parameter
Ext.Vars.RegisterModVariable(ModuleUUID, 'companions', {})

local creatureManager = {}
---@class creatureConfig Handles creatures summoned by integrations
---@field book table
---@field isHostile boolean
---@field spawnedUUID string
---@field originalUUID string
---@field rarity string
local creatureConfig  = {
    ['book']         = {},
    ['isHostile']    = false,
    ['originalUUID'] = '',
    ['spawnedUUID']  = '',
    ['rarity']       = 'common',
}
local buffedCreatures = {}

---@param spawnedUUID string
local function SetSpawnedUUID(spawnedUUID)
    creatureConfig['spawnedUUID'] = spawnedUUID
end

---@return string
local function GetHostGUID()
    return tostring(Osi.GetHostCharacter())
end

---@param tplId string
local function GetGUIDFromTpl(tplId)
    return string.sub(tplId, -36)
end

---@param creatureTplId string
local function SetCreatureHostile(creatureTplId)
    local evilFactionId = 'Evil_NPC_64321d50-d516-b1b2-cfac-2eb773de1ff6'
    Osi.SetFaction(creatureTplId, evilFactionId)
    LC['log'].Info(string.format('Set hostile on %s', creatureTplId))
end

---@param creatureUUID string
local function SetCreatureLevelEqualToHost(creatureUUID)
    local host = GetHostGUID()
    if host then
        local level = Osi.GetLevel(host)
        if level then
            Ext.OnNextTick(function ()
                LC['log'].Debug(string.format('Setting %s level to %s', creatureUUID, level))
                Osi.SetLevel(creatureUUID, tonumber(level))
            end)
        end
    end
end

---@param creatureTplId string
local function HandleHostileSpawn(creatureTplId)
    LC['log'].Debug('Handling hostile spawn')
    SetCreatureHostile(creatureTplId)
    -- TODO maybe they buff themselves or debuff player here?
end

local function AddPartyBuffs()
    local host       = GetHostGUID()
    local randomBuff = LC['configUtils'].GetRandomPartyBuff(creatureConfig['book'])

    LC['log'].Info('Adding buffs to party')

    if randomBuff then
        LC['log'].Debug(
            string.format(
                '%s is casting party buff: %s on host %s',
                creatureConfig['spawnedUUID'],
                randomBuff,
                creatureConfig['spawnedUUID']
            )
        )
        Osi.UseSpell(creatureConfig['spawnedUUID'], randomBuff, creatureConfig['spawnedUUID'])
    end
end

local function HandleFriendlySpawn()
    LC['log'].Debug('Handling friendly spawn')

    AddPartyBuffs()
end

---@param statusName string
local function ApplyStatusToHost(statusName)
    Osi.ApplyStatus(GetHostGUID(), statusName, 1, 1, GetHostGUID())
end

--Opens portal when a companion is summoned
local function CastPortalSpell()
    local spells = {
        'LOW_SORCEROUSSUNDRIES_PORTAL_BLUE',
        'LOW_SORCEROUSSUNDRIES_PORTAL_GREEN',
        'LOW_SORCEROUSSUNDRIES_PORTAL_RED',
        'LOW_SORCEROUSSUNDRIES_PORTAL_PURPLE',
    }
    local spell  = spells[math.random(#spells)]

    LC['log'].Debug(string.format('Opening a portal: %s!', spell))

    ApplyStatusToHost(spell)
end

---@param message string
local function ShowSummonMessage(message)
    if message then
        Osi.OpenMessageBox(GetHostGUID(), message)
    end
end

---@param entityUUID string
---@param passives table
local function ApplyBookPassives(entityUUID, passives)
    for _, passiveName in pairs(passives) do
        LC['Debug'](string.format(
            'Applying passive "%s" to %s',
            passiveName,
            entityUUID
        ))
        --[[
        Must use OnNextTick here or subsequent application
        of passives will not work!
        ]]
        Ext.OnNextTick(function ()
            Osi.AddPassive(entityUUID, passiveName)
        end)
    end

    --[[
    Failure to apply passive error is not 100% reliable:
    After first loading a save the application fails, but all
    subsequent applications are successfully. Also, despite the error
    application of the passive still works.
    ]]
    Ext.OnNextTick(function (_)
        for _, passiveName in pairs(passives) do
            if Osi.HasPassive(entityUUID, passiveName) == 1 then
                LC['Debug'](string.format('%s applied successfully', passiveName))
            else
                LC['Critical'](string.format('%s application FAILED', passiveName))
            end
        end
    end)
end

--Initializes and saves all summon info
--@return table
local function InitializeCompanionsTableAndReturnModVars()
    local modVars = Ext.Vars.GetModVariables(ModuleUUID)
    if not modVars then
        LC['Debug']('Initializing companions table')
        modVars['companions'] = {}
    end
    return modVars
end

--Get persistent companions mod var
---@return table
local function GetCompanionsModVar()
    local modVars = InitializeCompanionsTableAndReturnModVars()
    return modVars['companions']
end

--Finds companion UUID in ModVars using original UUID
---@param originalUUID string
---@return string|nil
local function GetCompanionUUIDByRT(originalUUID)
    local companions = GetCompanionsModVar()

    return companions[originalUUID]
end

---@param book table
local function ApplyUpgradeEffects(book)
    local entityUUID       = GetCompanionUUIDByRT(book['upgrade']['entityUUID'])
    local passives         = book['upgrade']['passives']
    local statusEffectName = 'GHOST_FX_RED'

    if entityUUID then
        --TODO: maybe add effects to book config
        LC['Debug'](string.format(
            'Applying upgrade status effect %s to %s',
            statusEffectName,
            entityUUID
        ))
        Osi.ApplyStatus(entityUUID, statusEffectName, 1, 1, entityUUID)

        ApplyBookPassives(entityUUID, passives)
    end
end

---@param book table
local function OnUpgradeBookCreated(book)
    local upgradeTargetEntityUUID   = GetCompanionUUIDByRT(book['upgrade']['entityUUID'])
    local upgradeTargetEntityExists = false

    if upgradeTargetEntityUUID then
        upgradeTargetEntityExists = Osi.Exists(upgradeTargetEntityUUID) == 1

        LC['Debug'](string.format('Handling upgrade book %s', book['name']))

        if upgradeTargetEntityExists then
            ApplyUpgradeEffects(book)
        end
    end

    if not upgradeTargetEntityExists then
        LC['Critical'](
            string.format('Upgrade target entity %s does not exist!', upgradeTargetEntityUUID)
        )
    end
end

---@param book table
local function OnSummonBookCreated(book)
    LC['Debug'](string.format('Handling summon book %s', book['name']))
    LC['creatureManager'].OnBeforeSpawn(book)
    LC['creatureManager'].SpawnCreatureWithBook(book)
end

---@param book table
local function OnBeforeSpawn(book)
    CastPortalSpell()
    --ShowSummonMessage(book['summonMessage'])
end

--Applies self status buff from config, if any
local function ApplySpawnSelfStatus()
    local rndStatus = LC['configUtils'].GetRandomSelfStatusFromConfig(creatureConfig['book'])
    if creatureConfig and rndStatus then
        LC['log'].Debug(string.format(
            'Applying creature self status %s to %s',
            rndStatus,
            creatureConfig['spawnedUUID']
        ))
        Osi.ApplyStatus(
            creatureConfig['spawnedUUID'],
            rndStatus,
            -1,
            1,
            tostring(creatureConfig['spawnedUUID'])
        )
    end
end

---@param companionUUID string Template string for new companion
---@param originalUUID string
--Remembers what summons we have
local function SaveCompanionRecord(companionUUID, originalUUID)
    local modVars              = InitializeCompanionsTableAndReturnModVars()
    local companionMap         = modVars['companions']
    companionMap[originalUUID] = companionUUID
    modVars['companions']      = companionMap
    LC['Debug'](
        string.format('Saved companion record: %s -> %s', originalUUID, companionUUID)
    )
end

--Handles creature spawn, passing along object info from the event handler
---@param object string
---@param objectRT string
local function HandleCreatureSpawn(object, objectRT)
    LC['Debug']('Handling creature spawn: ' .. object)

    buffedCreatures[creatureConfig['spawnedUUID']] = 1

    ApplySpawnSelfStatus()

    if creatureConfig['isHostile'] == true then
        HandleHostileSpawn(creatureConfig['spawnedUUID'])
    else
        HandleFriendlySpawn()
    end

    SetCreatureLevelEqualToHost(creatureConfig['spawnedUUID'])

    SaveCompanionRecord(object, objectRT)
end

--Spawn creature based on book config
---@param book table
local function SpawnCreatureWithBook(book)
    ---@type table
    local summonSpells = book['summonSpells']

    if summonSpells and #summonSpells > 0 then
        local rndSpell = summonSpells[math.random(#summonSpells)]
        local caster   = GetHostGUID()
        local rarity   = rndSpell['rarity'] or 'common'

        LC['log'].Debug(string.format(
            'Casting summoning spell: %s [%s]',
            rndSpell['name'],
            rndSpell['entityUUID']
        ))

        Osi.UseSpell(caster, rndSpell['name'], caster)

        -- Set creature info for this scenario
        creatureConfig['book']            = book
        creatureConfig['rarity']          = rarity
        creatureConfig['originalUUID']    = rndSpell['entityUUID']

        -- This will be handled in EnteredLevel
        creatureManager['creatureConfig'] = creatureConfig
    else
        LC['log'].Critical('No summoning spells!')
    end
end

---@return table|nil
local function GetCreatureConfig()

end

---@param config table
local function SetCreatureConfig(config)

end

--External
creatureManager.SpawnCreatureWithBook = SpawnCreatureWithBook
creatureManager.HandleCreatureSpawn   = HandleCreatureSpawn
creatureManager.GetGUIDFromTpl        = GetGUIDFromTpl
creatureManager.OnBeforeSpawn         = OnBeforeSpawn
creatureManager.OnUpgradeBookCreated  = OnUpgradeBookCreated
creatureManager.OnSummonBookCreated   = OnSummonBookCreated
creatureManager.SetSpawnedUUID        = SetSpawnedUUID
LC['creatureManager']                 = creatureManager
