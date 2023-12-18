--[[
CreatureManager - Handles spawning of creatures and related
functionality
]]
local creatureManager = {}
---@class creatureConfig Handles creatures summoned by integrations
---@field book table
---@field handledSpawn boolean
---@field isHostile boolean
---@field spawnedGUID string
---@field rarity string
local creatureConfig  = {
    ['book']         = {},
    ['handledSpawn'] = false,
    ['isHostile']    = false,
    ['spawnedGUID']  = '',
    ['rarity']       = 'common',
}
local buffedCreatures = {}

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

---@param creatureTplId string
local function SetCreatureLevelEqualToHost(creatureTplId)
    local host = GetHostGUID()
    if host then
        local level = Osi.GetLevel(host)
        if level then
            LC['log'].Debug(string.format('Setting %s level to %s', creatureTplId, level))
            Osi.SetLevel(creatureTplId, tonumber(level))
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
                '%s is casting party buff: %s on %s',
                creatureConfig['spawnedGUID'],
                randomBuff,
                host
            )
        )
        Osi.UseSpell(creatureConfig['spawnedGUID'], randomBuff, host)
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
        Osi.AddPassive(entityUUID, passiveName)

        local success = Osi.HasPassive(entityUUID, passiveName)

        if success == 1 then
            LC['Debug'](string.format('%s applied successfully', passiveName))
        else
            LC['Critical'](string.format('%s application FAILED', passiveName))
        end
    end
end

---@param book table
local function ApplyUpgradeEffects(book)
    local entityUUID       = book['upgrade']['entityUUID']
    local passives         = book['upgrade']['passives']
    local statusEffectName = 'GHOST_FX_RED'

    --TODO: maybe add effects to book config
    LC['Debug'](string.format(
        'Applying upgrade status effect %s to %s',
        statusEffectName,
        entityUUID
    ))
    Osi.ApplyStatus(entityUUID, statusEffectName, 1, 1, entityUUID)

    ApplyBookPassives(entityUUID, passives)
end

---@param book table
local function OnUpgradeBookCreated(book)
    local upgradeTargetEntityUUID   = book['upgrade']['entityUUID']
    local upgradeTargetEntityExists = Osi.Exists(upgradeTargetEntityUUID) == 1

    LC['Debug'](string.format('Handling upgrade book %s', book['name']))

    if upgradeTargetEntityExists then
        ApplyUpgradeEffects(book)
    else
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
            creatureConfig['spawnedGUID']
        ))
        Osi.ApplyStatus(creatureConfig['spawnedGUID'], rndStatus, -1, 1, tostring(creatureConfig['spawnedGUID']))
    end
end

--Gets all tags for a given entityUUID
---@param entityUUID string
---@return table
local function GetTags(entityUUID)
    local entity = Osi.GetEntity(entityUUID)
    local tags   = {}

    if entity then
        ---@diagnostic disable-next-line: undefined-field
        local components = entity.GetAllComponents()
        _D(components)
    else
        LC['Critical']('Could not get entity for ' .. entityUUID)
    end

    return tags
end

local function HandleCreatureSpawn()
    LC['log'].Debug('Handling creature spawn')

    buffedCreatures[creatureConfig['spawnedGUID']] = 1

    ApplySpawnSelfStatus()

    if creatureConfig['isHostile'] == true then
        HandleHostileSpawn(creatureConfig['spawnedGUID'])
    else
        HandleFriendlySpawn()
    end

    SetCreatureLevelEqualToHost(creatureConfig['spawnedGUID'])

    creatureConfig['handledSpawn'] = true
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
        ---@type string
        creatureConfig['spawnedGUID']     = tostring(rndSpell['entityUUID'])
        creatureConfig['handledSpawn']    = false
        creatureConfig['book']            = book
        creatureConfig['rarity']          = rarity

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
creatureManager.GetTags               = GetTags
LC['creatureManager']                 = creatureManager
