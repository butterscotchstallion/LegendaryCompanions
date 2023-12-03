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

function LCConfigUtils.GetPartyBuffsFromConfig(config)
    return config['buffPartySpells']
end

function LCConfigUtils.GetRandomPartyBuff(config)
    local buffs = LCConfigUtils.GetPartyBuffsFromConfig(config)
    return buffs[math.random(#buffs)]
end

function LCConfigUtils.GetRandomCreatureTplFromConfig(config)
    local tpls = config['entityUUIDs']
    if #tpls == 0 then
        MuffinLogger.Warn('Warning: no templates in config!')
    end
    return tpls[math.random(#tpls)]
end

function LCConfigUtils.GetRandomSelfStatusFromConfig(config)
    local statuses = config['selfStatus']
    if #statuses == 0 then
        MuffinLogger.Warn('Warning: no self statuses in config!')
    end
    return statuses[math.random(#statuses)]
end

-- @param rarity 'common' | 'rare' | 'legendary'
-- @return string
function LCConfigUtils.GetRandomConfigByRarity(rarity)
    local enabledConfigs = LCConfigUtils.GetEnabledConfigs()
    local randomCreature = nil
    if #enabledConfigs > 0 then
        local randomConfig = enabledConfigs[math.random(#enabledConfigs)]
        if randomConfig then
            return randomConfig[rarity]
        end
    else
        MuffinLogger.Warn('No enabled configs!')
    end
    return randomCreature
end

function LCConfigUtils.GetRandomCommonConfig()
    return LCConfigUtils.GetRandomConfigByRarity('common')
end

function LCConfigUtils.GetRandomRareConfig()
    return LCConfigUtils.GetRandomConfigByRarity('rare')
end

function LCConfigUtils.GetRandomLegendaryConfig()
    return LCConfigUtils.GetRandomConfigByRarity('legendary')
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
