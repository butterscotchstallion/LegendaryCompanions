local configUtils = {}

--@param config table
--@return table
function configUtils.GetPartyBuffsFromConfig(config)
    return config['buffPartySpells']
end

--@param config table
--@return string
function configUtils.GetRandomPartyBuff(config)
    local buffs = configUtils.GetPartyBuffsFromConfig(config)
    if buffs and #buffs > 0 then
        return buffs[math.random(#buffs)]
    end
end

--@param config table
--@return string
function configUtils.GetRandomSelfStatusFromConfig(config)
    local statuses = config['selfStatus']
    if not statuses or #statuses == 0 then
        LC['log'].Warn('Warning: no self statuses in config!')
    else
        return statuses[math.random(#statuses)]
    end
end

--@return table
function configUtils.GetConfigs()
    return LC['integrations']
end

-- @return table
function configUtils.GetBooksWithIntegrationName()
    local configs  = configUtils.GetConfigs()
    local books    = {}
    local bookInfo = nil
    for _, config in pairs(configs) do
        local intName  = config['name']
        books[intName] = config['books']
    end
    return books
end

function string.Starts(string, start)
    return string.sub(string, 1, string.len(start)) == start
end

--@param books table
--@param bookTplId string
--@return book | void
function configUtils.GetBookByBookTplId(books, bookTplId)
    for integrationName, _ in pairs(books) do
        for _, book in pairs(books[integrationName]) do
            local isLikelyMatch = string.Starts(bookTplId, book['name'])
            if isLikelyMatch then
                -- Used to get other templates based on rarity
                book['integrationName'] = integrationName
                return book
            end
        end
    end
end

--[[
-- Check if the pages in the supplied book
-- match all the pages passed in.
--@param book table
--@param pages table
--]]
function configUtils.IsPageMatch(book, pages)
    local bookPages       = book['pages']
    local allPagesPresent = false
    local pageMatches     = 0
    if #bookPages == #pages then
        for _, bookPage in pairs(bookPages) do
            for _, page in pairs(pages) do
                if string.Starts(page, bookPage) then
                    pageMatches = pageMatches + 1
                end
            end
        end
        allPagesPresent = pageMatches == #bookPages
    end
    return allPagesPresent
end

LC['configUtils'] = configUtils
