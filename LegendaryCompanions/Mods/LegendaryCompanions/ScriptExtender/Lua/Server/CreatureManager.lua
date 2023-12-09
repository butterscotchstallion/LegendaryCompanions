local CM              = {}
local creatureConfig  = {}
local buffedCreatures = {}

local function GetGUIDFromTpl(tplId)
    return string.sub(tplId, -36)
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
            MuffinLogger.Debug(string.format('Setting %s level to %s', creatureTplId, level))
            Osi.SetLevel(creatureTplId, tonumber(level))
        end
    end
end

local function HandleHostileSpawn(creatureTplId)
    MuffinLogger.Debug('Handling hostile spawn')
    SetCreatureHostile(creatureTplId)
    -- TODO maybe they buff themselves or debuff player here?
end

-- @return nil
local function AddPartyBuffs()
    MuffinLogger.Info('Adding buffs to party')
    local host       = tostring(Osi.GetHostCharacter())
    local randomBuff = LCConfigUtils.GetRandomPartyBuff(creatureConfig['book'])

    if randomBuff then
        MuffinLogger.Debug(
            string.format(
                '%s is casting party buff: %s on %s',
                creatureConfig['spawnedGUID'],
                randomBuff,
                host
            )
        )
        Osi.UseSpell(creatureConfig['spawnedGUID'], randomBuff, host)
    end
end

local function HandleFriendlySpawn(creatureTplId)
    MuffinLogger.Debug('Handling friendly spawn')

    -- Spells add them as a follower automatically
    if creatureConfig['spawnStrategy'] == 'entityUUIDs' then
        MuffinLogger.Debug('Adding ' .. creatureTplId .. ' as follower')
        Osi.AddPartyFollower(creatureTplId, Osi.GetHostCharacter())
    end

    AddPartyBuffs()
end

local function CastPortalSpell(creatureGUID)
    MuffinLogger.Debug('Opening a portal!')
    local host = tostring(Osi.GetHostCharacter())
    Osi.ApplyStatus(host, 'PUZ_CASTEDPORTAL_BLUE', 1, 1, host)
end

local function OnBeforeSpawn(creatureGUID)
    CastPortalSpell(creatureGUID)
end

local function ApplySpawnSelfStatus()
    local rndStatus = LCConfigUtils.GetRandomSelfStatusFromConfig(creatureConfig['book'])
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
        MuffinLogger.Debug('Handling creature spawn')

        buffedCreatures[creatureConfig['spawnedGUID']] = 1

        ApplySpawnSelfStatus()

        if creatureConfig['isHostile'] == true then
            HandleHostileSpawn(creatureConfig['spawnedGUID'])
        else
            HandleFriendlySpawn(creatureConfig['spawnedGUID'])
        end

        SetCreatureLevelEqualToHost(creatureConfig['spawnedGUID'])

        creatureConfig['handledSpawn'] = true
    end
end

-- @param creatureTplId string
-- @param book table
local function SpawnCreatureByTemplateId(creatureTplId, book)
    local x, y, z     = Osi.GetPosition(tostring(Osi.GetHostCharacter()))
    local numericXPos = tonumber(x)
    local isHostile   = false

    if creatureTplId then
        MuffinLogger.Debug(string.format('Attempting to spawn a %s at %s, %s, %s', creatureTplId, x, y, z))

        -- Give some space if this is a hostile creature
        if isHostile then
            x = x + 10
            y = y + 10
        end

        if numericXPos then
            local createdGUID = Osi.CreateAt(creatureTplId, numericXPos, y, z, 0, 1, '')
            if createdGUID then
                MuffinLogger.Debug(string.format('Successfully spawned %s [%s]', creatureTplId, createdGUID))

                creatureConfig['spawnedGUID']  = createdGUID
                creatureConfig['handledSpawn'] = false
                creatureConfig['book']         = book
                -- Creature spawn will be handled in OnWentOnStage
            else
                MuffinLogger.Critical(string.format('Failed to spawn %s', creatureTplId))
            end
        end
    else
        MuffinLogger.Critical('Invalid template id!')
    end
end

--[[
-- Spawn creature based on book config
-- 1. If there are summon spells, use those
-- 2. If there are no spells but there are entity UUIDs, use those
-- 3. If none of the above, get a random template based on book rarity
-- @param strategy string
-- @param book table
-- @return void
--]]
local function SpawnCreatureUsingStrategy(book)
    local strategy     = LCConfigUtils.GetSummoningStrategy(book)
    local summonSpells = book['summonSpells']

    MuffinLogger.Debug(string.format('Spawning creature using strategy: %s', strategy))

    if summonSpells and #summonSpells > 0 then
        local rndSpell = summonSpells[math.random(#summonSpells)]
        local caster   = tostring(Osi.GetHostCharacter())

        MuffinLogger.Debug(string.format('Casting summoning spell: %s', rndSpell['name']))

        Osi.UseSpell(caster, rndSpell['name'], caster)

        -- Set creature info for this scenario
        creatureConfig['spawnedGUID']   = rndSpell['entityUUID']
        creatureConfig['handledSpawn']  = false
        creatureConfig['book']          = book
        creatureConfig['spawnStrategy'] = 'spells'

        -- This will be handled in EnteredLevel
        CM['creatureConfig']            = creatureConfig
    else
        local templates = book['entityUUIDs']
        if not templates or #templates == 0 then
            local configs = LCConfigUtils.GetConfigs()
            local intName = book['integrationName']
            local rarity  = book['rarity']
            if configs and configs[intName] then
                MuffinLogger.Debug(string.format('No templates for book %s; using rarity %s',
                    book['name'],
                    book['rarity']
                ))
                templates = configs[intName][rarity]['entityUUIDs']

                if templates then
                    creatureConfig['spawnStrategy'] = 'entityUUIDs'
                else
                    MuffinLogger.Critical('Failed to get creature UUID by rarity!')
                end
            else
                MuffinLogger.Warn('Invalid book rarity!')
            end
        end

        SpawnCreatureByTemplateId(templates[math.random(#templates)], book)
    end
end

local function OnWentOnStage(objectGUID, isOnStageNow)
    if isOnStageNow then
        if creatureConfig and creatureConfig['spawnedGUID'] then
            local alreadyBuffed = buffedCreatures[creatureConfig['spawnedGUID']] == objectGUID
            if objectGUID == creatureConfig['spawnedGUID'] and not alreadyBuffed then
                if creatureConfig and not creatureConfig['handledSpawn'] then
                    MuffinLogger.Debug(creatureConfig['spawnedGUID'] .. ' is now on stage!')
                    HandleCreatureSpawn()
                end
            end
        end
    end
end

-- External
CM.OnWentOnStage              = OnWentOnStage
CM.SpawnCreatureByTemplateId  = SpawnCreatureByTemplateId
CM.SpawnCreatureUsingStrategy = SpawnCreatureUsingStrategy
CM.HandleCreatureSpawn        = HandleCreatureSpawn
CM.GetGUIDFromTpl             = GetGUIDFromTpl
CM.OnBeforeSpawn              = OnBeforeSpawn
LC['CreatureManager']         = CM
