LCConfigUtils = {
    ['config'] = {
        ['integrations'] = {
            GITHZERAI_CONFIG,
        },
        -- Party buffs
        ['friendlySpawnBuffParty'] = true,
        -- Spawn buffs
        ['friendlySpawnBuffSelf'] = true,
        ['hostileSpawnBuffSelf'] = false,
    }
}

-- @param rarity 'common' | 'rare' | 'legendary'
-- @return table | nil
function LCConfigUtils.GetRandomCreatureByRarity(rarity)
    local enabledConfigs = LCConfigUtils.GetEnabledConfigs()
    local randomCreature = nil
    if #enabledConfigs > 0 then
        local randomConfig = enabledConfigs[math.random(#enabledConfigs)]
        local rarityConfig = randomConfig[rarity]
        if rarityConfig ~= nil then
            local creatureUUIDs = rarityConfig['entityUUIDs']
            randomCreature = rarityConfig[math.random(#creatureUUIDs)]
            return randomCreature
        else
            MuffinLogger.critical(string.format('Invalid rarity: %s', rarity))
        end
    else
        MuffinLogger.warn('No enabled configs!')
    end
    return randomCreature
end

-- @return table
function LCConfigUtils.GetEnabledConfigs()
    local enabledConfigs = {}
    local integrationConfigs = LCConfigUtils['config']['integrations']
    for _, intConfig in pairs(integrationConfigs) do
        _D(intConfig)
        if intConfig['enabled'] then
            table.insert(enabledConfigs)
        end
    end
    return enabledConfigs
end
