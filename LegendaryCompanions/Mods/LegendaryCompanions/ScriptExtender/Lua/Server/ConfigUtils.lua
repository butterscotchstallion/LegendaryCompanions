--[[
ConfigUtils

Handle operations involving the integration config
]]
local configUtils = {}

---@param config table
---@return table
function configUtils.GetPartyBuffsFromConfig(config)
    return config['buffPartySpells']
end

---@param config table
---@return string|nil
function configUtils.GetRandomPartyBuff(config)
    local buffs = configUtils.GetPartyBuffsFromConfig(config)
    if buffs and #buffs > 0 then
        return buffs[math.random(1, #buffs)]
    end
    return nil
end

---@param config table
---@return string|nil
function configUtils.GetRandomSelfStatusFromConfig(config)
    local statuses = config['selfStatus']
    if not statuses or #statuses == 0 then
        LC['log'].Debug('Warning: no self statuses in config!')
        return nil
    else
        return statuses[math.random(1, #statuses)]
    end
end

--[[
Get configs, optionally all. This is a flat
table of configs (which are also tables).
]]
---@param options? table
---@return table
function configUtils.GetConfigs(options)
    local opts        = options or {}
    local enabledOnly = not opts['enabledOnly']
    local enabled     = {}
    for _, integration in pairs(LC['integrations']) do
        if enabledOnly and integration['enabled'] then
            table.insert(enabled, integration)
        end
    end
    return enabled
end

---@param name string
---@return string|nil
function configUtils.getConfigByName(name)
    local configs = configUtils.GetConfigs()
    for _, cfg in pairs(configs) do
        if cfg['name'] == name then
            return cfg
        end
    end
end

---@return number
function configUtils.GetTotalConfigs()
    local total = 0
    for _ in pairs(LC['integrations']) do
        total = total + 1
    end
    return total
end

---@return table
function configUtils.GetConfigTotals()
    return {
        ['enabledCount'] = #configUtils.GetConfigs(),
        ['totalCount']   = LC['integrationLogMessages']['totalIntegrations'],
    }
end

---@return table books
function configUtils.GetBooksWithIntegrationName()
    local configs = configUtils.GetConfigs()
    local books   = {}
    for _, config in pairs(configs) do
        books[config['name']] = config['books']
    end
    return books
end

---@param input string
---@param startPosition number
local function IsLikelyMatch(input, startPosition)
    return string.sub(input, 1, string.len(startPosition)) == startPosition
end

---@param books table
---@param bookTplId string
---@return table|nil
function configUtils.GetBookByBookTplId(books, bookTplId)
    for integrationName, _ in pairs(books) do
        for _, book in pairs(books[integrationName]) do
            local isLikelyMatch = IsLikelyMatch(bookTplId, book['name'])
            if isLikelyMatch then
                -- Used to get other templates based on rarity
                book['integrationName'] = integrationName
                return book
            end
        end
    end
end

--Returns true if this is an upgrade book
---@param book table
---@return boolean
function configUtils.IsUpgradeBook(book)
    return type(book['upgrade']) == 'table'
end

--Check if the pages in the supplied book
--match all the pages passed in.
---@param book table
---@param pages table
function configUtils.IsPageMatch(book, pages)
    local bookPages       = book['pages']
    local allPagesPresent = false
    local pageMatches     = 0
    if #bookPages == #pages then
        for _, bookPage in pairs(bookPages) do
            for _, page in pairs(pages) do
                if IsLikelyMatch(page, bookPage) then
                    pageMatches = pageMatches + 1
                end
            end
        end
        allPagesPresent = pageMatches == #bookPages
    end

    return allPagesPresent
end

LC['configUtils'] = configUtils
