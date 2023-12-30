--[[
ConfigUtils

Handle operations involving the integration config
]]
local configUtils = {
    ['bookTypes'] = {
        ['SUMMON_COMPANION']  = 'SUMMON_COMPANION',
        ['PARTY_BUFFS']       = 'PARTY_BUFFS',
        ['COMPANION_UPGRADE'] = 'COMPANION_UPGRADE',
    }
}

---@return string
function configUtils.GetBookTypeByName(name)
    return configUtils['bookTypes'][name]
end

---@return string
function configUtils.GetPartyBuffBookType()
    return configUtils.GetBookTypeByName(configUtils['bookTypes']['PARTY_BUFFS'])
end

---@return string
function configUtils.GetCompanionUpgradeBookType()
    return configUtils.GetBookTypeByName(configUtils['bookTypes']['COMPANION_UPGRADE'])
end

---@return string
function configUtils.GetSummonBookType()
    return configUtils.GetBookTypeByName(configUtils['bookTypes']['SUMMON_COMPANION'])
end

-- Get books from config
---@param configs table
---@return table
local function GetBooksFromConfigs(configs)
    local books = {}
    for _, config in pairs(configs) do
        if config['books'] then
            for _, book in pairs(config['books']) do
                table.insert(books, book)
            end
        end
    end
    return books
end

--Return summon type books
---@param books table
---@return table
local function GetSummonBooksFromBooks(books)
    local summonBooks = {}
    for _, book in pairs(books) do
        if configUtils.IsSummonBook(book) then
            table.insert(summonBooks, book)
        end
    end
    return summonBooks
end

--Return upgrade type books
---@param books table
---@return table
local function GetUpgradeBooksFromBooks(books)
    local upgradeBooks = {}
    for _, book in pairs(books) do
        if configUtils.IsUpgradeBook(book) then
            table.insert(upgradeBooks, book)
        end
    end
    return upgradeBooks
end

---@return table
local function GetBooks()
    local configs = configUtils.GetConfigs()
    return GetBooksFromConfigs(configs)
end

---@param scrollUUID string
---@return boolean|nil
function configUtils.GetUpgradeBookByScrollUUID(scrollUUID)
    local books        = GetBooks()
    local upgradeBooks = GetUpgradeBooksFromBooks(books)

    if upgradeBooks and #upgradeBooks > 0 then
        for _, book in pairs(upgradeBooks) do
            if configUtils.GetScrollFromBook(book) == scrollUUID then
                return book
            end
        end
    end
end

---@return table entityUUIDBookMap
function configUtils.GetSummonEntityUUIDBookMap()
    local books         = GetBooks()
    local summonBooks   = GetSummonBooksFromBooks(books)
    local entityUUIDMap = {}
    for _, book in pairs(summonBooks) do
        local spells = book['summonSpells']
        for _, spell in pairs(spells) do
            local entityUUID = spell['entityUUID']
            entityUUIDMap[entityUUID] = book
        end
    end
    return entityUUIDMap
end

---@param book table
---@return string|nil
function configUtils.GetBookType(book)
    return book['type']
end

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
function configUtils.GetConfigByName(name)
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

--Filters table of books by their type
---@param bookType string SUMMON_COMPANION, PARTY_BUFFS, COMPANION_UPGRADE
---@param books table books|nil
function configUtils.GetBookByBookType(bookType, books)
    for _, book in pairs(books) do
        if book['type'] == bookType then
            return book
        end
    end
end

---@param books table
---@return table|nil
function configUtils.GetSummonBookByName(books)
    return configUtils.GetBookByBookType(configUtils.GetSummonBookType(), books)
end

---@param book table
function configUtils.GetSummonScrollFromBook(book)
    local scrollName = book['summonScrollUUID']

    LC['Debug'](string.format('Found summon scroll: %s', scrollName))

    return scrollName
end

---@param book table
function configUtils.GetScrollFromBook(book)
    if configUtils.IsSummonBook(book) then
        return configUtils.GetSummonScrollFromBook(book)
    elseif configUtils.IsUpgradeBook(book) then
        return configUtils.GetUpgradeScrollFromBook(book)
    else
        LC['Critical']('Unknown book type: ' .. book['type'])
    end
end

---@param book table
function configUtils.GetUpgradeScrollFromBook(book)
    local scrollName = book['upgradeScrollUUID']

    LC['Debug'](string.format('Found upgrade scroll: %s', scrollName))

    return scrollName
end

function configUtils.AddScrollToInventory(scrollName)
    Osi.TemplateAddTo(
        scrollName,
        LC['creatureManager'].GetHostGUID(),
        1,
        1
    )
end

--Returns true if this is an upgrade book
---@param book table
---@return boolean
function configUtils.IsUpgradeBook(book)
    return book['type'] == configUtils.GetCompanionUpgradeBookType()
end

--Returns true if this is a party buffs book
---@param book table
---@return boolean
function configUtils.IsPartyBuffsBook(book)
    return book['type'] == configUtils.GetPartyBuffBookType()
end

--Returns true if this is a summon book
---@param book table
---@return boolean
function configUtils.IsSummonBook(book)
    return book['type'] == configUtils.GetSummonBookType()
end

--[[
Check if the pages in the supplied book
match all the pages passed in.
]]
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

--Check if book is named according to convention
---@param bookName string
---@return boolean
function configUtils.IsLCBook(bookName)
    return string.find(bookName, '^BOOK_LC_') ~= nil
end

--Check if this is the upgrade spell
---@param spellName string
---@return table|nil
function configUtils.GetUpgradeBookByScrollSpellName(spellName)
    local books        = GetBooks()
    local upgradeBooks = GetUpgradeBooksFromBooks(books)
    if upgradeBooks and #upgradeBooks > 0 then
        for _, book in pairs(upgradeBooks) do
            if book['upgradeScrollSpellName'] == spellName then
                return book
            end
        end
    end
end

LC['configUtils'] = configUtils
