--[[
CreatureManager - Handles spawning of creatures and related
functionality
]]
local creatureManager = {
    ['companionCache']         = nil,
    ['isExpectingSummonBook']  = nil,
    ['isExpectingUpgradeBook'] = nil,
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
local function AddPartyBuffs(spawnedUUID, book)
    local randomBuff = LC['configUtils'].GetRandomPartyBuff(book)
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
local function HandleFriendlySpawn(spawnedUUID, book)
    LC['log'].Debug('Handling friendly actions')
    AddPartyBuffs(spawnedUUID, book)
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

---@param entityUUID string UUID string of entity
---@param passives table passives from config
local function ApplyBookPassives(entityUUID, passives)
    for _, passiveName in pairs(passives) do
        LC['Debug'](string.format(
            'Upgrade: Applying passive "%s" to %s',
            passiveName,
            entityUUID
        ))
        Ext.OnNextTick(function ()
            Osi.AddPassive(entityUUID, passiveName)
        end)
    end
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
            LC['Debug']('Upgrade: setting entity level to ' .. level)
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

---@param entityUUID string Integration book from config
---@param book table Book with upgrade info
local function ApplyUpgradeEffects(entityUUID, book)
    local upgradeInfo = book['upgrade']
    local passives = book['upgrade']['passives']

    ShowUpgradeMessage(upgradeInfo['message'])
    SetCompanionLevel(entityUUID, upgradeInfo['setLevelTo'])

    if entityUUID and #passives > 0 then
        ApplyBookPassives(entityUUID, passives)
    end
end

local function OnBeforeSpawn()
    CastPortalSpell()
end

--Applies self status buff from config, if any
---@param spawnedUUID string
---@param book table
local function ApplySpawnSelfStatus(spawnedUUID, book)
    local rndStatus = LC['configUtils'].GetRandomSelfStatusFromConfig(book)
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

--Handles creature spawn, passing along object info from the event handler
---@param spawnedUUID string Creature instance UUID
---@param book table Book with the summoning spell
local function HandleCreatureSpawn(spawnedUUID, book)
    LC['Debug']('Handling creature spawn: ' .. spawnedUUID)

    ApplySpawnSelfStatus(spawnedUUID, book)

    --Nil by default
    if book['isHostile'] == true then
        HandleHostileSpawn(spawnedUUID)
    else
        HandleFriendlySpawn(spawnedUUID, book)
    end

    SetCreatureLevelEqualToHost(spawnedUUID)
end

---@return table
local function GetPlayerSummons()
    return Osi.DB_PlayerSummons:Get(nil)
end

---@param tagUUID string
---@param tags table
---@return boolean
local function IsTagInTags(tagUUID, tags)
    for _, uuid in pairs(tags) do
        if uuid == tagUUID then
            return true
        end
    end
    return false
end

--TODO: Maybe refactor to be more efficient
---@return table
local function GetLCSummons()
    local summons       = GetPlayerSummons()
    local taggedSummons = {}
    if summons then
        for _, summon in pairs(summons) do
            local tplName      = summon[1]
            local entity       = Ext.Entity.Get(tplName)
            local summonUUID   = entity.Uuid.EntityUuid
            local tagComponent = entity:GetComponent('Tag')
            local tags         = tagComponent['Tags']
            local isLCSummon   = IsTagInTags('6d6d37a2-95be-4841-b97f-c59e2b4a8f49', tags)
            if isLCSummon then
                table.insert(taggedSummons, summonUUID)
            end
        end
    end
    return taggedSummons
end

--[[
1. Check if player has any summons with LC tag
2. Get first one
3. Get originalUUID from summon somehow
4. Apply upgrade effects using info
]]
---@param book table
local function HandleUpgradeCompanionSpell(book)
    local companions = GetLCSummons()
    if companions and #companions > 0 then
        for _, summonUUID in pairs(companions) do
            ApplyUpgradeEffects(
                summonUUID,
                book
            )
        end
    end
end

---@param book table
local function HandleSummonCompanionSpell(book)
    LC['Debug']('Handling summon: ' .. book['name'])
    OnBeforeSpawn()
end

--External
creatureManager.HandleCreatureSpawn         = HandleCreatureSpawn
creatureManager.GetGUIDFromTpl              = GetGUIDFromTpl
creatureManager.GetHostGUID                 = GetHostGUID
creatureManager.HandleUpgradeCompanionSpell = HandleUpgradeCompanionSpell
creatureManager.HandleSummonCompanionSpell  = HandleSummonCompanionSpell
LC['creatureManager']                       = creatureManager
