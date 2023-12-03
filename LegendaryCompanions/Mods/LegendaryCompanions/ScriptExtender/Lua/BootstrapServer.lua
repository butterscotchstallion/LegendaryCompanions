------------------------------------------------------------------
---------------------LegendaryCompanions-----------------------
------------------------------------------------------------------
Ext.Require('Server/Config.lua')
Ext.Require('Server/HotStatsReload.lua')
Ext.Require('Server/SimoLoops.lua')
Ext.Require('Server/MuffinLogger.lua')
Ext.Require('Server/SECommands.lua')
Ext.Require('Server/CommonStatuses.lua')
--Integrations
Ext.Require('Server/GithzeraiConfig.lua')
Ext.Require('Server/LegendaryCompanions.lua')

local function print_start_up_message()
    local mod = Ext.Mod.GetMod(ModuleUUID)
    local version = mod.Info.ModVersion
    local version_msg = string.format('LegendaryCompanions v%s.%s.%s', version[1], version[2], version[3])
    MuffinLogger.info(version_msg)
end

local function on_session_loaded()
    print_start_up_message()
end

Ext.Events.SessionLoaded:Subscribe(on_session_loaded)
