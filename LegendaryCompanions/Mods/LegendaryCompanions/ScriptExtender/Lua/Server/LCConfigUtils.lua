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
    if buffs and #buffs > 0 then
        return buffs[math.random(#buffs)]
    end
end

function LCConfigUtils.GetRandomCreatureTplFromConfig(config)
    local tpls = config['entityUUIDs']
    if not tpls or #tpls == 0 then
        MuffinLogger.Warn('Warning: no templates in config!')
    else
        return tpls[math.random(#tpls)]
    end
end

function LCConfigUtils.GetRandomSelfStatusFromConfig(config)
    local statuses = config['selfStatus']
    _D(config)
    if not statuses or #statuses == 0 then
        MuffinLogger.Warn('Warning: no self statuses in config!')
    else
        return statuses[math.random(#statuses)]
    end
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
    local bookInfo = nil
    for intName, _ in pairs(configs) do
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
        -- Get template based on book rarity here
    end
end

function string.starts(String, Start)
    return string.sub(String, 1, string.len(Start)) == Start
end

-- @param books table
-- @param bookTplId string
-- @return book | nil
function LCConfigUtils.GetBookByBookTplId(books, bookTplId)
    for integrationName, _ in pairs(books) do
        for _, book in pairs(books[integrationName]) do
            local isLikelyMatch = string.starts(bookTplId, book['name'])
            if isLikelyMatch then
                return book
            end
        end
    end
end

--[[
-- Check if the pages in the supplied book
-- match all the pages passed in.
-- @param book table
-- @param pages table
--]]
function LCConfigUtils.IsPageMatch(book, pages)
    local bookPages       = book['pages']
    local allPagesPresent = false
    local pageMatches     = 0
    if #bookPages == #pages then
        for _, bookPage in pairs(bookPages) do
            for _, page in pairs(pages) do
                if string.starts(page, bookPage) then
                    pageMatches = pageMatches + 1
                end
            end
        end
        allPagesPresent = pageMatches == #bookPages
    end
    return allPagesPresent
end
