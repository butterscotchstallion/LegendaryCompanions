--[[
Event Handler
]]

--[[
When summoning via spell, we have to listen for this event to get
the GUID of the entity
]]
---@param objectTemplate string
---@param originalUUID string
---@param levelName string
local function OnEnteredLevel(objectTemplate, originalUUID, levelName)
    local creatureConfig = LC['creatureManager']['creatureConfig']
    if creatureConfig then
        local objectUUID = LC['creatureManager'].GetGUIDFromTpl(objectTemplate)

        if objectUUID and creatureConfig['originalUUID'] == originalUUID then
            LC['log'].Debug(string.format('%s entered (%s)!', objectUUID, levelName))
            LC['creatureManager'].HandleCreatureSpawn(tostring(objectUUID), originalUUID)
        end
    end
end

--[[
When a book is created:
1. Check if it's referenced in the config
2. Check if the pages match
3. Return book if everything matches
]]
---@param item1TplId string First combination ingredient
---@param item2TplId string Second combination ingredient
---@param bookTplId string The combined item
local function HandleBookCreated(item1TplId, item2TplId, bookTplId)
    local books = LC['configUtils'].GetBooksWithIntegrationName()
    local book  = LC['configUtils'].GetBookByBookTplId(books, bookTplId)

    if book then
        local pages = {
            item1TplId,
            item2TplId,
        }
        local pagesMatch = LC['configUtils'].IsPageMatch(book, pages)
        if pagesMatch then
            LC['log'].Debug(string.format('Book "%s" created!', book['name']))

            --Handle different book types
            local isUpgradeBook = LC['configUtils'].IsUpgradeBook(book)
            if isUpgradeBook then
                LC['creatureManager'].OnUpgradeBookCreated(book)
            else
                LC['creatureManager'].OnSummonBookCreated(book)
            end
        else
            LC['log'].Debug(
                string.format('%s and %s not found in book %s', item1TplId, item2TplId, book)
            )
        end
    else
        LC['log'].Debug(
            string.format('Book "%s" created but not found in config list', bookTplId)
        )
    end
end

local function PrintStartUpMessages()
    local mod        = Ext.Mod.GetMod(ModuleUUID)
    local version    = mod.Info.ModVersion
    local versionMsg = string.format(
        'LegendaryCompanions v%s.%s.%s',
        version[1],
        version[2],
        version[3]
    )

    LC['Info'](versionMsg)
end

local function PrintIntegrationMessages()
    for _, msg in pairs(LC['integrationLogMessages']['Info']) do
        LC['Info'](msg)
    end
    for _, msg in pairs(LC['integrationLogMessages']['Warn']) do
        LC['Warning'](msg)
    end
    for _, msg in pairs(LC['integrationLogMessages']['Critical']) do
        LC['Critical'](msg)
    end
    for _, msg in pairs(LC['integrationLogMessages']['Debug']) do
        LC['Debug'](msg)
    end

    local configTotals = LC['configUtils'].GetConfigTotals()
    LC['Info'](
        string.format(
            'Integrations: %s/%s configs enabled',
            configTotals['enabledCount'],
            configTotals['totalCount']
        )
    )
end

local function OnSessionLoaded()
    PrintStartUpMessages()
    PrintIntegrationMessages()
end

---@param item1 string First combination item
---@param item2 string Second combination item
---@param item3 string Third combination item
---@param item4 string Fourth combination item
---@param item5 string Fifth combination item
---@param item6 string Sixth combination item
---@param newItem string Created item
local function OnCombined(item1, item2, item3, item4, item5, item6, newItem)
    -- Update me if we add books with more pages
    HandleBookCreated(item1, item2, newItem)
end

--Listeners
Ext.Events.SessionLoaded:Subscribe(OnSessionLoaded)
Ext.Osiris.RegisterListener('Combined', 7, 'after', OnCombined)
Ext.Osiris.RegisterListener('EnteredLevel', 3, 'after', OnEnteredLevel)
