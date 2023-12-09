--[[
-- Legendary Companions - Event Handler
--]]

-- item1, item2, item3, item4, item5, character, newItem
local function OnCombined(item1, item2, _, _, _, _, newItem)
    -- Update me if we add books with more pages
    LC['BookEventHandler'].HandleBookCreated(item1, item2, newItem)
end

local function OnItemOpened(itemTemplateId)
    MuffinLogger.Info(string.format('Opened item %s', itemTemplateId))
    LC['CreatureManager'].SpawnCreature()
end

--[[
-- When summoning via spell, we have to listen for this event to get
-- the GUID of the entity
--]]
local function OnEnteredLevel(object, objectRT, level)
    local creatureConfig = LC['CreatureManager']['creatureConfig']
    local objectGUID = LC['CreatureManager'].GetGUIDFromTpl(object)

    if creatureConfig then
        if creatureConfig['spawnedGUID'] == objectRT then
            MuffinLogger.Debug(string.format('%s (%s) entered level!', objectRT, level))
            LC['CreatureManager']['creatureConfig']['spawnedGUID'] = objectGUID
            LC['CreatureManager'].HandleCreatureSpawn()
        end
    end
end

Ext.Osiris.RegisterListener('WentOnStage', 2, 'after', LC['CreatureManager'].OnWentOnStage)
Ext.Osiris.RegisterListener('Combined', 7, 'after', OnCombined)
Ext.Osiris.RegisterListener('EnteredLevel', 3, 'after', OnEnteredLevel)
-- Ext.Osiris.RegisterListener('Opened', 1, 'after', OnItemOpened)
-- TODO add death handler that removes creatures and from buff table
