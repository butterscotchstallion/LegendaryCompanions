local MOD_PATH = 'Public/LegendaryCompanions/Stats/Generated/Data/'
local FILES_TO_RELOAD = {
    'LC_Summons_Buffs.txt',
    'LC_Githzerai_Equipment.txt',
    'LC_Summons.txt',
    'LC_Books.txt',
}
local isGameLoaded = false

local function OnReset()
    for _, filename in pairs(FILES_TO_RELOAD) do
        local filePath = string.format('%s%s', MOD_PATH, filename)
        if string.len(filename) > 0 then
            MuffinLogger.Info(string.format('RELOADING %s', filePath))
            ---@diagnostic disable-next-line: undefined-field
            Ext.Stats.LoadStatsFile(filePath, false)
        else
            MuffinLogger.Critical(string.format('Invalid file: %s', filePath))
        end
    end
end

Ext.Events.ResetCompleted:Subscribe(OnReset)
