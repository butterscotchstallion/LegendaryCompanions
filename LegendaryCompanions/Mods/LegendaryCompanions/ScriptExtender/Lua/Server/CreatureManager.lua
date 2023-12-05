local CM                 = {}
local creatureConfig     = nil
local buffedCreatures    = {}
local creatureBuffSpells = {
    --'Target_Bless_3_AI',
    --'EC_Target_Enlarge_AOE',
    --'EC_Target_Haste_AOE',
    'EC_Target_Longstrider_AOE'
}
local LC_COMMON_STATUSES = {
    'UNSUMMON_ABLE',
    'SHADOWCURSE_SUMMON_CHECK',
}

local function GetGUIDFromTpl(tpl_id)
    return string.sub(tpl_id, -36)
end

local function SetCreatureHostile(creatureTplId)
    local EVIL_FACTION_ID = 'Evil_NPC_64321d50-d516-b1b2-cfac-2eb773de1ff6'
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

local function HandleHostileSpawn(creatureTplId)
    SetCreatureHostile(creatureTplId)
    -- TODO maybe they buff themselves or debuff player here?
end

-- @return nil
local function AddPartyBuffs()
    MuffinLogger.Info('Adding buffs to party')
    local partyMemberTpl = GetGUIDFromTpl(Osi.GetHostCharacter())
    local randomBuff = LCConfigUtils.GetRandomPartyBuff(creatureConfig)
    if creatureConfig and randomBuff then
        Osi.UseSpell(creatureConfig['spawnedGUID'], randomBuff, partyMemberTpl)
        MuffinLogger.Debug(string.format('Casting creature buff: %s', randomBuff))
    end
end

local function HandleFriendlySpawn(creatureTplId)
    Osi.AddPartyFollower(creatureTplId, Osi.GetHostCharacter())
    AddPartyBuffs()
end

local function ApplySpawnSelfStatus()
    local rndStatus = LCConfigUtils.GetRandomSelfStatusFromConfig(creatureConfig)
    if creatureConfig and rndStatus then
        MuffinLogger.Debug(string.format(
            'Applying creature self status %s to %s',
            rndStatus,
            creatureConfig['spawnedGUID']
        ))
        Osi.RemoveStatus(creatureConfig['spawnedGUID'], rndStatus)
        Osi.ApplyStatus(creatureConfig['spawnedGUID'], rndStatus, -1, 1, tostring(creatureConfig['spawnedGUID']))
    end
end

local function HandleCreatureSpawn()
    if creatureConfig then
        local isFriend = true
        buffedCreatures[creatureConfig['spawnedGUID']] = 1
        -- Creature statuses
        ApplySpawnSelfStatus()

        -- Handle hostility
        if isFriend then
            HandleFriendlySpawn(creatureConfig['spawnedGUID'])
        else
            HandleHostileSpawn(creatureConfig['spawnedGUID'])
        end

        -- Set creature level and buffs
        SetCreatureLevelEqualToHost(creatureConfig['spawnedGUID'])

        creatureConfig['handledSpawn'] = true
    end
end

local function SpawnCreatureByTemplateId(creatureTplId, isFriendly)
    local x, y, z     = Osi.GetPosition(tostring(Osi.GetHostCharacter()))
    local numericXPos = tonumber(x)
    -- Use config value instead
    MuffinLogger.Info(string.format('Attempting to spawn a %s at %s, %s, %s', creatureTplId, x, y, z))

    -- Give some space if this is a hostile creature
    if not isFriendly then
        x = x + 10
        y = y + 10
    end

    if numericXPos then
        local createdGUID = Osi.CreateAt(creatureTplId, numericXPos, y, z, 0, 1, '')
        if createdGUID then
            MuffinLogger.Debug('Successful spawn')
            creatureConfig['spawnedTpl']   = creatureTplId
            creatureConfig['spawnedGUID']  = createdGUID
            creatureConfig['handledSpawn'] = false
            -- Creature spawn will be handled in OnWentOnStage
        else
            MuffinLogger.Critical(string.format('Failed to spawn %s', creatureTplId))
        end
    end
end

local function SpawnCreatureUsingRandomConfig()
    creatureConfig = LCConfigUtils.GetRandomCommonConfig()
    if creatureConfig and creatureConfig['spawnedGUID'] then
        local randomCreatureTplId = LCConfigUtils.GetRandomCreatureTplFromConfig(creatureConfig)

        if randomCreatureTplId then
            SpawnCreatureByTemplateId(randomCreatureTplId)
        end
    end
end

local function OnWentOnStage(objectGUID, isOnStageNow)
    if isOnStageNow then
        if creatureConfig and creatureConfig['spawnedGUID'] then
            local alreadyBuffed = buffedCreatures[creatureConfig['spawnedGUID']] == objectGUID
            if objectGUID == creatureConfig['spawnedGUID'] and not alreadyBuffed then
                if creatureConfig and not creatureConfig['handledSpawn'] then
                    HandleCreatureSpawn()
                end
            end
        end
    end
end

-- External
CM.OnWentOnStage             = OnWentOnStage
CM.SpawnCreatureByTemplateId = SpawnCreatureByTemplateId
LC['CreatureManager']        = CM
