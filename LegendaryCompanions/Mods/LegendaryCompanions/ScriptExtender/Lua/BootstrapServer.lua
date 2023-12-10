--[[
--------------------------------------------------------------------
---------------------LegendaryCompanions----------------------------
--------------------------------------------------------------------
--]]
LC = {
    ['logLevel']               = 'DEBUG',
    ['integrations']           = {},
    ['log']                    = {},
    ['configUtils']            = {},
    ['bookEventHandler']       = {},
    ['creatureManager']        = {},
    ['integrationManager']     = {},
    ['integrationLogMessages'] = {},
}
Ext.Require('Server/HotStatsReload.lua')
Ext.Require('Server/SimoLoops.lua')
Ext.Require('Server/MuffinLogger.lua')
Ext.Require('Server/IntegrationManager.lua')
Ext.Require('Server/Integrations.lua')
Ext.Require('Server/SECommands.lua')
Ext.Require('Server/ConfigUtils.lua')
Ext.Require('Server/CreatureManager.lua')
Ext.Require('Server/BookEventHandler.lua')
Ext.Require('Server/EventHandler.lua')

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
