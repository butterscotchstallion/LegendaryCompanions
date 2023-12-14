--[[
--------------------------------------------------------------------
---------------------LegendaryCompanions----------------------------
--------------------------------------------------------------------
--]]
LC = {
    ['configUtils']            = {},
    ['creatureManager']        = {},
    ['integrations']           = {},
    ['integrationLogMessages'] = {},
    ['integrationManager']     = {},
    ['log']                    = {},
    ['logLevel']               = 'DEBUG',
}
Ext.Require('Server/HotStatsReload.lua')
Ext.Require('Server/SimoLoops.lua')
Ext.Require('Server/MuffinLogger.lua')
Ext.Require('Server/ConfigUtils.lua')
Ext.Require('Server/IntegrationManager.lua')
Ext.Require('Server/Integrations.lua')
Ext.Require('Server/SECommands.lua')
Ext.Require('Server/CreatureManager.lua')
Ext.Require('Server/EventHandler.lua')
