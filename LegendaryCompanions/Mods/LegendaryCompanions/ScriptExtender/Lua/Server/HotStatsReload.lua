local MOD_PATH = 'Public/LegendaryCompanions/Stats/Generated/Data/'
local FILES_TO_RELOAD = {
    'LC_Summons_Buffs.txt',
    --'LC_Summons.txt',
    --'LC_Summons_Githzerai.txt',
    --'LC_Summons_RSO.txt',
    'LC_Books.txt',
}

local function OnReset()
    for _, filename in pairs(FILES_TO_RELOAD) do
        if filename then
            local filePath = string.format('%s%s', MOD_PATH, filename)
            if string.len(filename) > 0 then
                LC['log'].Info(string.format('RELOADING %s', filePath))
                ---@diagnostic disable-next-line: undefined-field
                Ext.Stats.LoadStatsFile(filePath, false)
            else
                LC['log'].Critical(string.format('Invalid file: %s', filePath))
            end
        end
    end
end

Ext.Events.ResetCompleted:Subscribe(OnReset)
