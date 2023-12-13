--[[
-- Legendary Companions - Event Handler
--]]

--[[
-- When summoning via spell, we have to listen for this event to get
-- the GUID of the entity
--]]
local function OnEnteredLevel(object, objectRT, level)
    local creatureConfig = LC['creatureManager']['creatureConfig']
    local objectGUID     = LC['creatureManager'].GetGUIDFromTpl(object)

    if creatureConfig then
        if creatureConfig['spawnedGUID'] == objectRT then
            LC['log'].Debug(string.format('%s (%s) entered level!', objectRT, level))
            LC['creatureManager']['creatureConfig']['spawnedGUID'] = objectGUID
            LC['creatureManager'].HandleCreatureSpawn()
        end
    end
end

--[[
-- When a book is created:
------------------------------------------------
-- 1. Check if it's one of ours
-- 2. Check if the pages match the ones we have
-- 3. Get book based on this information
--@param item1TplId string
--@param item2TplId string
--@param bookTplId string
--@return void
--]]
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

            LC['creatureManager'].OnBeforeSpawn(book)
            LC['creatureManager'].SpawnCreatureWithBook(book)
        else
            LC['log'].Debug(string.format('%s and %s not found in pages', item1TplId, item2TplId))
        end
    else
        LC['log'].Debug(string.format('Book "%s" created but not found in config list', bookTplId))
    end
end

--@param object string
local function OnTurnEnded(object)
    --LC['log'].Debug('Turn ended: ' .. object)
end

--@return void
local function PrintStartUpMessage()
    local mod        = Ext.Mod.GetMod(ModuleUUID)
    local version    = mod.Info.ModVersion
    local versionMsg = string.format('LegendaryCompanions v%s.%s.%s', version[1], version[2], version[3])
    LC['log'].Info(versionMsg)

    if #LC['integrationLogMessages'] > 0 then
        for _, msg in pairs(LC['integrationLogMessages']) do
            LC['log'].Info(msg)
        end
    end
end

local function OnSessionLoaded()
    PrintStartUpMessage()
end

--@param item1 string
--@param item2 string
--@param item3 string
--@param item4 string
--@param item5 string
--@param character string
--@param newItem string
--@return void
local function OnCombined(item1, item2, item3, item4, item5, item6, newItem)
    -- Update me if we add books with more pages
    HandleBookCreated(item1, item2, newItem)
end

Ext.Events.SessionLoaded:Subscribe(OnSessionLoaded)
Ext.Osiris.RegisterListener('Combined', 7, 'after', OnCombined)
Ext.Osiris.RegisterListener('EnteredLevel', 3, 'after', OnEnteredLevel)
Ext.Osiris.RegisterListener('TurnEnded', 1, 'after', OnTurnEnded)
--TODO: add death handler that removes creatures and from buff table
