--[[
-- Legendary Companions - Event Handler
--]]

-- item1, item2, item3, item4, item5, character, newItem
local function OnCombined(item1, item2, _, _, _, _, newItem)
    -- Update me if we add books with more pages
    LC['bookEventHandler'].HandleBookCreated(item1, item2, newItem)
end

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

Ext.Osiris.RegisterListener('WentOnStage', 2, 'after', LC['creatureManager'].OnWentOnStage)
Ext.Osiris.RegisterListener('Combined', 7, 'after', OnCombined)
Ext.Osiris.RegisterListener('EnteredLevel', 3, 'after', OnEnteredLevel)
-- TODO add death handler that removes creatures and from buff table
