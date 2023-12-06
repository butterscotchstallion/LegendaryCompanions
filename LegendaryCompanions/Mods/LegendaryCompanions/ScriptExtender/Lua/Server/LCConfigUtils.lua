LCConfigUtils = {
    ['config'] = {
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
    local configs = LCConfigUtils.GetConfigs()
    local randomCreature = nil
    if #configs > 0 then
        local randomConfig = configs[math.random(#configs)]
        if randomConfig then
            return randomConfig[rarity]
        end
    else
        MuffinLogger.Warn('No configs!')
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
function LCConfigUtils.GetConfigs()
    return LC['integrations']
end

-- @return table
function LCConfigUtils.GetBooksWithIntegrationName()
    local configs = LCConfigUtils.GetConfigs()
    local books = {}
    local integrationName = nil
    local bookInfo = nil
    for intName, _ in pairs(configs) do
        integrationName = intName
        bookInfo = configs[intName]['books']
        books[intName] = bookInfo
    end
    return books
end

-- @param bookInfo table
function LCConfigUtils.GetTemplateByBookInfo(bookInfo)
    local templates = bookInfo['entityUUIDs']
    if #templates > 0 then
        return templates[math.random(#templates)]
    else
        MuffinLogger.Debug('No templates found for book')
    end
end

function LCConfigUtils.GetBookByTplName(tplName)
    local books = LCConfigUtils.GetBooksWithIntegrationName()
    if books then
        for _, intName in pairs(books) do
            for _, book in pairs(books[intName]) do
                if book['name'] == tplName then
                    return book
                end
            end
        end
    end
end
