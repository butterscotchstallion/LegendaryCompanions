--[[
    The below code is based on code provided by FallenStar.

    Thanks!
--]]
local commands = {
    {
        name = "dumpentity",
        params = "uuid, filename",
        func = function(cmd, uuid, filename)
            ---@diagnostic disable-next-line: undefined-global
            if uuid == "host" then uuid = Osi.GetHostCharacter() end
            local entity = Ext.Entity.Get(uuid)
            filename = (filename or uuid) .. ".json"
            Ext.IO.SaveFile(filename, Ext.DumpExport(entity:GetAllComponents()))
            MuffinLogger.debug(string.format('Saved dump file: %s', filename))
        end
    }
}
local function RegisterCommands()
    for _, command in ipairs(commands) do
        MuffinLogger.debug(string.format('Registered command %s', command.name))
        Ext.RegisterConsoleCommand(command.name, command.func)
    end
end
RegisterCommands()
