--[[
CreatureManager - Handles spawning of creatures and related
functionality
]]
local creatureManager = {}

---@diagnostic disable-next-line: redundant-parameter
Ext.Vars.RegisterModVariable(ModuleUUID, 'companions', {})

---@class creatureConfig Handles creatures summoned by integrations
---@field book table
---@field isHostile boolean
---@field spawnedUUID string
---@field originalUUID string
---@field rarity string
local creatureConfig = {
    ['book']         = {},
    ['isHostile']    = false,
    ['originalUUID'] = '',
    ['rarity']       = 'common',
}

---@return string Returns host UUID as a string
local function GetHostGUID()
    return tostring(Osi.GetHostCharacter())
end

---@param tplId string Root Template string
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

---@param spawnedUUID string
local function AddPartyBuffs(spawnedUUID)
    local randomBuff = LC['configUtils'].GetRandomPartyBuff(creatureConfig['book'])
    if randomBuff then
        local buffTarget = GetHostGUID()
        LC['log'].Debug(
            string.format(
                'Casting party buff: %s on host %s',
                randomBuff,
                buffTarget
            )
        )
        Ext.OnNextTick(function ()
            Osi.ApplyStatus(
                buffTarget,
                randomBuff,
                -1,
                1,
                spawnedUUID
            )
        end)
    end
end

---@param spawnedUUID string
local function HandleFriendlySpawn(spawnedUUID)
    LC['log'].Debug('Handling friendly spawn')
    AddPartyBuffs(spawnedUUID)
end

---@param statusName string Name of status
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

---@param entityUUID string UUID string of entity
---@param passives table passives from config
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

    Ext.OnNextTick(function (_)
        for _, passiveName in pairs(passives) do
            if Osi.HasPassive(entityUUID, passiveName) == 1 then
                LC['Debug'](string.format('%s applied successfully', passiveName))
            else
                LC['Critical'](string.format('%s application FAILED', passiveName))
            end
        end
    end)
    ]]
end

--Initializes companions table if necessary and returns Modvars
---@return table Companions or empty table if uninitialized
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
---@param originalUUID string Original UUID from Root Template
---@return string|nil Returns UUID string or nil
local function GetCompanionUUIDByRT(originalUUID)
    local companions = GetCompanionsModVar()
    return companions[originalUUID]
end

---@param book table Integration book from config
local function ApplyUpgradeEffects(book)
    local entityUUID = GetCompanionUUIDByRT(book['upgrade']['entityUUID'])
    local passives   = book['upgrade']['passives'] or {}
    if entityUUID and #passives > 0 then
        ApplyBookPassives(entityUUID, passives)
    end
end

---@param message string Message to show in message box
local function ShowUpgradeMessage(message)
    Osi.OpenMessageBox(GetHostGUID(), message)
end

---@param entityUUID string Original UUID from Root Template
---@param level number Set companion to this level (number)
local function SetCompanionLevel(entityUUID, level)
    if level and entityUUID then
        local entityLevel = Osi.GetLevel(entityUUID)

        if level > entityLevel then
            LC['Debug']('Upgrade setting entity level to ' .. level)
            Osi.SetLevel(entityUUID, level)
        else
            LC['Debug'](
                string.format(
                    'Not setting level because current level is not less than config level: %s <= %s',
                    entityLevel,
                    level
                )
            )
        end
    end
end

---@param book table Integration book
local function OnUpgradeBookCreated(book)
    local upgradeInfo               = book['upgrade']
    local upgradeTargetEntityUUID   = GetCompanionUUIDByRT(upgradeInfo['entityUUID'])
    local upgradeTargetEntityExists = false

    if upgradeTargetEntityUUID then
        upgradeTargetEntityExists = Osi.Exists(upgradeTargetEntityUUID) == 1

        LC['Debug'](string.format('Handling upgrade book %s', book['name']))

        if upgradeTargetEntityExists then
            ShowUpgradeMessage(upgradeInfo['message'])
            ApplyUpgradeEffects(book)
            SetCompanionLevel(upgradeTargetEntityUUID, upgradeInfo['setLevelTo'])
        else
            LC['Debug'](
                string.format('Upgrade target %s does not exist',
                    upgradeTargetEntityUUID)
            )
        end
    end

    if not upgradeTargetEntityExists then
        LC['Critical'](
            string.format('Upgrade target entity %s does not exist!', upgradeTargetEntityUUID)
        )
    end
end

---@param book table Integration book
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
---@param spawnedUUID string
local function ApplySpawnSelfStatus(spawnedUUID)
    local rndStatus = LC['configUtils'].GetRandomSelfStatusFromConfig(creatureConfig['book'])
    if rndStatus then
        LC['log'].Debug(string.format(
            'Applying creature self status %s to %s',
            rndStatus,
            spawnedUUID
        ))
        Osi.ApplyStatus(
            spawnedUUID,
            rndStatus,
            -1,
            1,
            tostring(spawnedUUID)
        )
    end
end

---@param companionUUID string Template string for new companion
---@param originalUUID string Root template UUID
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
---@param spawnedUUID string Creature instance UUID
---@param spawnedRT string Root template string
local function HandleCreatureSpawn(spawnedUUID, spawnedRT)
    LC['Debug']('Handling creature spawn: ' .. spawnedUUID)

    ApplySpawnSelfStatus(spawnedUUID)

    --Nil by default
    if creatureConfig['isHostile'] == true then
        HandleHostileSpawn(spawnedUUID)
    else
        HandleFriendlySpawn(spawnedUUID)
    end

    SetCreatureLevelEqualToHost(spawnedUUID)

    SaveCompanionRecord(spawnedUUID, spawnedRT)
end

--Spawn creature based on book config
---@param book table Book from config
local function SpawnCreatureWithBook(book)
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

        --Set creature info for this scenario
        creatureConfig['book']            = book
        creatureConfig['rarity']          = rarity
        creatureConfig['originalUUID']    = rndSpell['entityUUID']

        --This will be handled in EnteredLevel
        creatureManager['creatureConfig'] = creatureConfig
    else
        --This should not be possible if the integration validation is working
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
LC['creatureManager']                 = creatureManager
