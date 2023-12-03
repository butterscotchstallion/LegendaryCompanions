--[[
-- Legendary Companions
--]]
local EVIL_FACTION_ID = 'Evil_NPC_64321d50-d516-b1b2-cfac-2eb773de1ff6'
local creatures = {}
local creatureBuffSpells = {
    --'Target_Bless_3_AI',
    --'EC_Target_Enlarge_AOE',
    --'EC_Target_Haste_AOE',
    'EC_Target_Longstrider_AOE'
}
local function IsFriend()
    return math.random(0, 1) == 1
end
local lastSpawnedCreature = ''
local lastSpawnedCreatureInfo = nil
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

--[[
-- Creatures that are spawned can't cast spells immediately;
-- we have to wait for them to be on stage. We queue up a spell
-- here in anticipation of the event handler
--]]
local function AddBuffsToCreature(creatureTplId)
    local rndSpellName = creatureBuffSpells[math.random(#creatureBuffSpells)]
    if rndSpellName then
        --spawned_creature_spell_queue[rndSpellName] = creatureTplId
        Osi.UseSpell(creatureTplId, rndSpellName, creatureTplId)
        MuffinLogger.Info(string.format('Queued spell %s with target %s', rndSpellName, creatureTplId))
    end
end

-- @param partyMemberTpl string
-- @return nil
local function AddPartyBuffs(partyMemberTpl)
    if lastSpawnedCreature and lastSpawnedCreatureInfo then
        if #lastSpawnedCreatureInfo['buff_party_spells'] > 0 then
            local spells = lastSpawnedCreatureInfo['buff_party_spells']
            local rnd_party_buff = spells[math.random(#spells)]
            --spawned_creature_spell_queue[rnd_party_buff] = partyMemberTpl
            Osi.UseSpell(lastSpawnedCreature, rnd_party_buff, partyMemberTpl)
            MuffinLogger.Debug(string.format('Queued creature buff: %s', rnd_party_buff))
        else
            AddBuffsToCreature(partyMemberTpl)
        end
    end
end

-- Remove is here to prevent stacking on multiple
-- of the same creature
local function ApplyGeneralCreatureStatus()
    Osi.RemoveStatus(lastSpawnedCreature, 'EC_AUTOMATED')
    Osi.ApplyStatus(lastSpawnedCreature, 'EC_AUTOMATED', -1, 1, lastSpawnedCreature)
end

local function ApplySpawnSelfStatus()
    if lastSpawnedCreatureInfo and lastSpawnedCreatureInfo['selfStatus'] then
        local statuses = lastSpawnedCreatureInfo['selfStatus']
        if #statuses > 0 then
            local rndStatus = statuses[math.random(#statuses)]
            MuffinLogger.Debug(string.format('Applying creature self status %s to %s', rndStatus, lastSpawnedCreature))
            Osi.RemoveStatus(lastSpawnedCreature, rndStatus)
            Osi.ApplyStatus(lastSpawnedCreature, rndStatus, -1, 1, lastSpawnedCreature)
        end
    end
end

local function HandleCreatureSpawn()
    if lastSpawnedCreatureInfo then
        local creatureTplId = lastSpawnedCreatureInfo['spawnedGUID']

        -- Creature statuses
        ApplyGeneralCreatureStatus()
        if lastSpawnedCreatureInfo['selfStatus'] then
            ApplySpawnSelfStatus()
        end
        buffedCreatures[lastSpawnedCreature] = 1

        -- Handle spells

        -- Handle hostility
        --[[
        if is_friend then
            handle_friendly_spawn(creatureTplId)
        --else
            handle_hostile_spawn(creatureTplId)
        --end
        ]]
        HandleFriendlySpawn(creatureTplId)
        --handle_hostile_spawn(creatureTplId)

        -- Set creature level and buffs
        SetCreatureLevelEqualToHost(creatureTplId)
        -- AddBuffsToCreature(creatureTplId)

        -- Party buffs
        --if is_friend and config['friendly_spawn_buff_party'] then
        MuffinLogger.Info('Adding buffs to party')
        local partyMemberTpl = GetGUIDFromTpl(Osi.GetHostCharacter())
        AddPartyBuffs(partyMemberTpl)
        --end

        lastSpawnedCreatureInfo['handledSpawn'] = true
    end
end

local function SpawnCreature()
    lastSpawnedCreatureInfo = LCConfigUtils.GetRandomCreatureByRarity('common')
    if lastSpawnedCreatureInfo then
        local templates = lastSpawnedCreatureInfo['templateIds']
        local summonSpell = lastSpawnedCreatureInfo['summonSpell']

        if #templates > 0 then
            local rndCreatureTplId = templates[math.random(#templates)]
            local x, y, z = Osi.GetPosition(tostring(Osi.GetHostCharacter()))
            local numericXPos = tonumber(x)
            local isFriendly = IsFriend()
            MuffinLogger.Info(string.format('Spawning a %s at %s, %s, %s', rndCreatureTplId, x, y, z))

            -- Give some space if this is a hostile creature
            if not isFriendly then
                x = x + 10
                y = y + 10
            end

            if numericXPos ~= nil then
                local createdGUID = Osi.CreateAt(rndCreatureTplId, numericXPos, y, z, 0, 1, '')
                if createdGUID ~= nil then
                    MuffinLogger.Debug('Successful spawn')
                    lastSpawnedCreature = tostring(createdGUID)
                    lastSpawnedCreatureInfo['spawnedGUID'] = lastSpawnedCreature
                    lastSpawnedCreatureInfo['handledSpawn'] = false
                else
                    MuffinLogger.Critical(string.format('Failed to spawn %s', rndCreatureTplId))
                end
            end
        else
            if summonSpell then
                MuffinLogger.Debug(string.format('Casting summoning spell: %s', summonSpell))
                local hostChar = tostring(Osi.GetHostCharacter())
                Osi.UseSpell(hostChar, summonSpell, hostChar)
                lastSpawnedCreatureInfo['spawnedGUID'] = nil
                lastSpawnedCreatureInfo['handledSpawn'] = false
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
        if lastSpawnedCreature then
            local alreadyBuffed = buffedCreatures[lastSpawnedCreature] == objectGUID
            if objectGUID == lastSpawnedCreature and not alreadyBuffed then
                -- TODO copy this status into EC mod
                -- TODO make this only apply to friendlies
                if lastSpawnedCreatureInfo and not lastSpawnedCreatureInfo['handledSpawn'] then
                    HandleCreatureSpawn()
                end
            end
        end
    end
end

local function OnTemplateAddedTo(objectTemplate, object2, inventoryHolder, addType)
    MuffinLogger.Critical(string.format('Added item %s to %s', objectTemplate, inventoryHolder))
end

local function OnBookRead(character, bookName)
    MuffinLogger.Debug('BOOK READ!!')
    MuffinLogger.Debug(bookName)
end

Ext.Osiris.RegisterListener('WentOnStage', 2, 'after', OnWentOnStage)
Ext.Osiris.RegisterListener('Opened', 1, 'after', OnItemOpened)
Ext.Osiris.RegisterListener('TemplateAddedTo', 4, 'after', OnTemplateAddedTo)
Ext.Osiris.RegisterListener('OpenCustomBookUI', 2, 'after', OnBookRead)
-- TODO add death handler that removes creatures and from buff table
