------------------------------------------------------------------
---------------------LegendaryCompanions--------------------------
------------------------------------------------------------------
LC = {
    logLevel = 'DEBUG'
}
Ext.Require('Server/Config.lua')
Ext.Require('Server/HotStatsReload.lua')
Ext.Require('Server/SimoLoops.lua')
Ext.Require('Server/MuffinLogger.lua')
Ext.Require('Server/SECommands.lua')
Ext.Require('Server/LCConfigUtils.lua')
Ext.Require('Server/CreatureManager.lua')
Ext.Require('Server/Integrations.lua')
Ext.Require('Server/BookEventHandler.lua')
Ext.Require('Server/EventHandler.lua')

local function PrintStartUpMessage()
    local mod = Ext.Mod.GetMod(ModuleUUID)
    local version = mod.Info.ModVersion
    local versionMsg = string.format('LegendaryCompanions v%s.%s.%s', version[1], version[2], version[3])
    MuffinLogger.Info(versionMsg)
end

local function OnSessionLoaded()
    PrintStartUpMessage()
end

Ext.Events.SessionLoaded:Subscribe(OnSessionLoaded)
