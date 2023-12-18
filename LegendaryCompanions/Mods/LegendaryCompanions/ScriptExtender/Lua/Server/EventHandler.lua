--[[
Event Handler
]]

--[[
When summoning via spell, we have to listen for this event to get
the GUID of the entity
]]
---@param object string
---@param objectRT string
---@param levelName string
local function OnEnteredLevel(object, objectRT, levelName)
    local creatureConfig = LC['creatureManager']['creatureConfig']
    local objectGUID     = LC['creatureManager'].GetGUIDFromTpl(object)
    if creatureConfig then
        if creatureConfig['spawnedGUID'] == objectRT then
            LC['log'].Debug(string.format('%s entered (%s)!', objectRT, levelName))
            LC['creatureManager']['creatureConfig']['spawnedGUID'] = objectGUID
            LC['creatureManager'].HandleCreatureSpawn()
        end
    end
end

--[[
When a book is created:
1. Check if it's referenced in the config
2. Check if the pages match
3. Return book if everything matches
]]
---@param item1TplId string
---@param item2TplId string
---@param bookTplId string
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
            LC['log'].Debug(string.format('Book "%s" has been created!', book['name']))

            --Handle different book types
            local isUpgradeBook = LC['configUtils'].IsUpgradeBook(book)
            if isUpgradeBook then
                LC['creatureManager'].OnUpgradeBookCreated(book)
            else
                LC['creatureManager'].OnSummonBookCreated(book)
            end
        else
            LC['log'].Debug(string.format('%s and %s not found in pages', item1TplId, item2TplId))
        end
    else
        LC['log'].Debug(string.format('Book "%s" created but not found in config list', bookTplId))
    end
end

---@param object string
local function OnTurnEnded(object)
    --LC['log'].Debug('Turn ended: ' .. object)
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

---@param item1 string
---@param item2 string
---@param item3 string
---@param item4 string
---@param item5 string
---@param item6 string
---@param newItem string
local function OnCombined(item1, item2, item3, item4, item5, item6, newItem)
    -- Update me if we add books with more pages
    HandleBookCreated(item1, item2, newItem)
end

---@param object GUIDSTRING
---@param status string
---@param causee GUIDSTRING
---@param storyActionID integer
local function OnStatusApplied(object, status, causee, storyActionID)
    LC['Debug'](string.format(
        'Status "%s" applied to object %s',
        status,
        object
    ))
end

Ext.Events.SessionLoaded:Subscribe(OnSessionLoaded)
--Ext.Osiris.RegisterListener('StatusApplied', 4, 'after', OnStatusApplied)
Ext.Osiris.RegisterListener('Combined', 7, 'after', OnCombined)
Ext.Osiris.RegisterListener('EnteredLevel', 3, 'after', OnEnteredLevel)
Ext.Osiris.RegisterListener('TurnEnded', 1, 'after', OnTurnEnded)
--TODO: add death handler that removes creatures and from buff table
