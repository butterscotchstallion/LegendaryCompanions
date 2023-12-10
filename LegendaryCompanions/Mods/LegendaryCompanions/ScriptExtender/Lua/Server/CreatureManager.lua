local CM              = {}
local creatureConfig  = {}
local buffedCreatures = {}

local function GetHostGUID()
    return tostring(Osi.GetHostCharacter())
end

local function GetGUIDFromTpl(tplId)
    return string.sub(tplId, -36)
end

local function SetCreatureHostile(creatureTplId)
    local EVIL_FACTION_ID = 'Evil_NPC_64321d50-d516-b1b2-cfac-2eb773de1ff6'
    Osi.SetFaction(creatureTplId, EVIL_FACTION_ID)
    LC['log'].Info(string.format('Set hostile on %s', creatureTplId))
end

local function SetCreatureLevelEqualToHost(creatureTplId)
    local host = Osi.GetHostCharacter()
    if host then
        local level = Osi.GetLevel(host)
        if level then
            LC['log'].Debug(string.format('Setting %s level to %s', creatureTplId, level))
            Osi.SetLevel(creatureTplId, tonumber(level))
        end
    end
end

local function HandleHostileSpawn(creatureTplId)
    LC['log'].Debug('Handling hostile spawn')
    SetCreatureHostile(creatureTplId)
    -- TODO maybe they buff themselves or debuff player here?
end

-- @return nil
local function AddPartyBuffs()
    LC['log'].Info('Adding buffs to party')
    local host       = tostring(Osi.GetHostCharacter())
    local randomBuff = LC['configUtils'].GetRandomPartyBuff(creatureConfig['book'])

    if randomBuff then
        LC['log'].Debug(
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
    LC['log'].Debug('Handling friendly spawn')

    -- Spells add them as a follower automatically
    if creatureConfig['spawnStrategy'] == 'entityUUIDs' then
        LC['log'].Debug('Adding ' .. creatureTplId .. ' as follower')
        Osi.AddPartyFollower(creatureTplId, Osi.GetHostCharacter())
    end

    AddPartyBuffs()
end

local function CastPortalSpell()
    LC['log'].Debug('Opening a portal!')
    local spells = {
        'LOW_SORCEROUSSUNDRIES_PORTAL_BLUE',
        'LOW_SORCEROUSSUNDRIES_PORTAL_GREEN',
        'LOW_SORCEROUSSUNDRIES_PORTAL_RED',
        'LOW_SORCEROUSSUNDRIES_PORTAL_PURPLE',
    }
    local spell  = spells[math.random(#spells)]
    Osi.ApplyStatus(GetHostGUID(), spell, 1, 1, GetHostGUID())
end

local function ShowSummonMessage(message)
    Osi.OpenMessageBox(GetHostGUID(), message)
end

local function OnBeforeSpawn(book)
    ShowSummonMessage(book['summonMessage'])
    CastPortalSpell()
end

local function ApplySpawnSelfStatus()
    local rndStatus = LC['configUtils'].GetRandomSelfStatusFromConfig(creatureConfig['book'])
    if creatureConfig and rndStatus then
        LC['log'].Debug(string.format(
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
        LC['log'].Debug('Handling creature spawn')

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
        LC['log'].Debug(string.format('Attempting to spawn a %s at %s, %s, %s', creatureTplId, x, y, z))

        -- Give some space if this is a hostile creature
        if isHostile then
            x = x + 10
            y = y + 10
        end

        if numericXPos then
            local createdGUID = Osi.CreateAt(creatureTplId, numericXPos, y, z, 0, 1, '')
            if createdGUID then
                LC['log'].Debug(string.format('Successfully spawned %s [%s]', creatureTplId, createdGUID))

                creatureConfig['spawnedGUID']  = createdGUID
                creatureConfig['handledSpawn'] = false
                creatureConfig['book']         = book
                -- Creature spawn will be handled in OnWentOnStage
            else
                LC['log'].Critical(string.format('Failed to spawn %s', creatureTplId))
            end
        end
    else
        LC['log'].Critical('Invalid template id!')
    end
end

--[[
-- Spawn creature based on book config
-- @param book table
-- @return void
--]]
local function SpawnCreatureUsingStrategy(book)
    local summonSpells = book['summonSpells']

    if summonSpells and #summonSpells > 0 then
        local rndSpell = summonSpells[math.random(#summonSpells)]
        local caster   = tostring(Osi.GetHostCharacter())

        LC['log'].Debug(string.format('Casting summoning spell: %s', rndSpell['name']))

        Osi.UseSpell(caster, rndSpell['name'], caster)

        -- Set creature info for this scenario
        creatureConfig['spawnedGUID']   = rndSpell['entityUUID']
        creatureConfig['handledSpawn']  = false
        creatureConfig['book']          = book
        creatureConfig['spawnStrategy'] = 'spells'

        -- This will be handled in EnteredLevel
        CM['creatureConfig']            = creatureConfig
    else
        LC['log'].Critical('No summoning spells!')
    end
end

local function OnWentOnStage(objectGUID, isOnStageNow)
    if isOnStageNow then
        if creatureConfig and creatureConfig['spawnedGUID'] then
            local alreadyBuffed = buffedCreatures[creatureConfig['spawnedGUID']] == objectGUID
            if objectGUID == creatureConfig['spawnedGUID'] and not alreadyBuffed then
                if creatureConfig and not creatureConfig['handledSpawn'] then
                    LC['log'].Debug(creatureConfig['spawnedGUID'] .. ' is now on stage!')
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
LC['creatureManager']         = CM
