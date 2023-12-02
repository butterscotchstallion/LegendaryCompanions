local MOD_PATH = 'Public/LegendaryCompanions/Stats/Generated/Data/'
local FILES_TO_RELOAD = {
    'LC_Summons_Buffs.txt',
    'LC_Summons.txt',
}

local function on_reset()
    for _, filename in pairs(FILES_TO_RELOAD) do
        local file_path = string.format('%s%s', MOD_PATH, filename)
        if filename then
            MuffinLogger.critical(string.format('RELOADING %s', file_path))
            ---@diagnostic disable-next-line: undefined-field
            Ext.Stats.LoadStatsFile(file_path, false)
        else
            MuffinLogger.critical(string.format('Invalid file: %s', file_path))
        end
    end
end

Ext.Events.ResetCompleted:Subscribe(on_reset)
