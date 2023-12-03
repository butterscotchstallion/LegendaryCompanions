--[[
-- Legendary Companions
--]]
local EVIL_FACTION_ID = 'Evil_NPC_64321d50-d516-b1b2-cfac-2eb773de1ff6'
local creatureBuffSpells = {
    --'Target_Bless_3_AI',
    --'EC_Target_Enlarge_AOE',
    --'EC_Target_Haste_AOE',
    'EC_Target_Longstrider_AOE'
}
local creatureConfig = nil
local buffedCreatures = {}
local function GetGUIDFromTpl(tpl_id)
    return string.sub(tpl_id, -36)
end

local function SetCreatureHostile(creatureTplId)
    Osi.SetFaction(creatureTplId, EVIL_FACTION_ID)
    MuffinLogger.Info(string.format('Set hostile on %s', creatureTplId))
end

local function SetCreatureLevelEqualToHost(creatureTplId)
    local host = Osi.GetHostCharacter()
    if host then
        local level = Osi.GetLevel(host)
        if level then
            Osi.SetLevel(creatureTplId, tonumber(level))
        end
    end
end

local function HandleFriendlySpawn(creatureTplId)
    Osi.AddPartyFollower(creatureTplId, Osi.GetHostCharacter())
end

local function HandleHostileSpawn(creatureTplId)
    SetCreatureHostile(creatureTplId)
    -- TODO maybe they buff themselves or debuff player here
end

local function AddBuffsToCreature(creatureTplId)
    local rndSpellName = creatureBuffSpells[math.random(#creatureBuffSpells)]
    if rndSpellName then
        Osi.UseSpell(creatureTplId, rndSpellName, creatureTplId)
        MuffinLogger.Info(string.format('Queued spell %s with target %s', rndSpellName, creatureTplId))
    end
end

-- @return nil
local function AddPartyBuffs()
    MuffinLogger.Info('Adding buffs to party')
    local partyMemberTpl = GetGUIDFromTpl(Osi.GetHostCharacter())
    local randomBuff = LCConfigUtils.GetRandomPartyBuff(creatureConfig)
    if creatureConfig and randomBuff then
        Osi.UseSpell(creatureConfig['spawnedGUID'], randomBuff, partyMemberTpl)
        MuffinLogger.Debug(string.format('Queued creature buff: %s', randomBuff))
    end
end

local function ApplySpawnSelfStatus()
    local rndStatus = LCConfigUtils.GetRandomSelfStatusFromConfig(creatureConfig)
    if creatureConfig and rndStatus then
        MuffinLogger.Debug(string.format('Applying creature self status %s to %s', rndStatus,
            creatureConfig['spawnedGUID']))
        Osi.RemoveStatus(creatureConfig['spawnedGUID'], rndStatus)
        Osi.ApplyStatus(creatureConfig['spawnedGUID'], rndStatus, -1, 1, tostring(creatureConfig['spawnedGUID']))
    end
end

local function HandleCreatureSpawn()
    if creatureConfig then
        local creatureTplId = creatureConfig['spawnedGUID']
        local isFriend = true
        -- Creature statuses
        ApplySpawnSelfStatus()
        buffedCreatures[creatureConfig['spawnedGUID']] = 1

        -- Handle hostility
        if isFriend then
            HandleFriendlySpawn(creatureTplId)
        else
            HandleHostileSpawn(creatureTplId)
        end

        -- Set creature level and buffs
        SetCreatureLevelEqualToHost(creatureTplId)

        -- Party buffs
        if isFriend then
            AddPartyBuffs()
        end

        creatureConfig['handledSpawn'] = true
    end
end

local function SpawnCreature()
    creatureConfig = LCConfigUtils.GetRandomCommonConfig()
    if creatureConfig and creatureConfig['spawnedGUID'] then
        local randomCreatureTpl = LCConfigUtils.GetRandomCreatureTplFromConfig(creatureConfig)

        if randomCreatureTpl then
            local x, y, z = Osi.GetPosition(tostring(Osi.GetHostCharacter()))
            local numericXPos = tonumber(x)
            local isFriendly = math.random(0, 1) == 1
            MuffinLogger.Info(string.format('Attempting to spawn a %s at %s, %s, %s', randomCreatureTpl, x, y, z))

            -- Give some space if this is a hostile creature
            if not isFriendly then
                x = x + 10
                y = y + 10
            end

            if numericXPos then
                local createdGUID = Osi.CreateAt(randomCreatureTpl, numericXPos, y, z, 0, 1, '')
                if createdGUID then
                    MuffinLogger.Debug('Successful spawn')
                    creatureConfig['spawnedTpl'] = randomCreatureTpl
                    creatureConfig['spawnedGUID'] = createdGUID
                    creatureConfig['handledSpawn'] = false
                    -- Creature spawn will be handled in OnWentOnStage
                else
                    MuffinLogger.Critical(string.format('Failed to spawn %s', randomCreatureTpl))
                end
            end
        end
    end
end

local function OnItemOpened(itemTemplateId)
    MuffinLogger.Info(string.format('Opened item %s', itemTemplateId))
    SpawnCreature()
end

local function OnWentOnStage(objectGUID, isOnStageNow)
    if isOnStageNow then
        if creatureConfig and creatureConfig['spawnedGUID'] then
            local alreadyBuffed = buffedCreatures[creatureConfig['spawnedGUID']] == objectGUID
            if objectGUID == creatureConfig['spawnedGUID'] and not alreadyBuffed then
                -- TODO copy this status into EC mod
                -- TODO make this only apply to friendlies
                if creatureConfig and not creatureConfig['handledSpawn'] then
                    HandleCreatureSpawn()
                end
            end
        end
    end
end

-- item1, item2, item3, item4, item5, character, newItem
local function OnCombined(item1, item2, _, _, _, _, newItem)
    MuffinLogger.Debug(item1)
    MuffinLogger.Debug(item2)

    LC['BookEventHandler'].HandleBookCreated(item1, item2, newItem)
end

Ext.Osiris.RegisterListener('WentOnStage', 2, 'after', OnWentOnStage)
-- Ext.Osiris.RegisterListener('Opened', 1, 'after', OnItemOpened)
Ext.Osiris.RegisterListener('Combined', 7, 'after', OnCombined)

-- TODO add death handler that removes creatures and from buff table
