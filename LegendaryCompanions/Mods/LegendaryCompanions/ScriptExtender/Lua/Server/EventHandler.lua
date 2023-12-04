--[[
-- Legendary Companions - Event Handler
--]]

-- item1, item2, item3, item4, item5, character, newItem
local function OnCombined(item1, item2, _, _, _, _, newItem)
    LC['BookEventHandler'].HandleBookCreated(item1, item2, newItem)
end

Ext.Osiris.RegisterListener('WentOnStage', 2, 'after', LC['CreatureManager']['OnWentOnStage'])
Ext.Osiris.RegisterListener('Combined', 7, 'after', OnCombined)
-- Ext.Osiris.RegisterListener('Opened', 1, 'after', OnItemOpened)

-- TODO add death handler that removes creatures and from buff table
