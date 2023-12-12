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

local function OnTurnEnded(object)
    --LC['log'].Debug('Turn ended: ' .. object)
end

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

Ext.Events.SessionLoaded:Subscribe(OnSessionLoaded)
Ext.Osiris.RegisterListener('WentOnStage', 2, 'after', LC['creatureManager'].OnWentOnStage)
Ext.Osiris.RegisterListener('Combined', 7, 'after', OnCombined)
Ext.Osiris.RegisterListener('EnteredLevel', 3, 'after', OnEnteredLevel)
Ext.Osiris.RegisterListener('TurnEnded', 1, 'after', OnTurnEnded)
-- TODO add death handler that removes creatures and from buff table
