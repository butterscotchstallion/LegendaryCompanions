--[[
    The below code is based on code provided by FallenStar.
    Thanks!
--]]
local commands = {
    {
        name = 'dumpentity',
        params = 'uuid, filename',
        func = function (cmd, uuid, filename)
            if uuid == 'host' then uuid = Osi.GetHostCharacter() end
            local entity = Ext.Entity.Get(uuid)
            filename = (filename or uuid) .. '.json'
            Ext.IO.SaveFile(filename, Ext.DumpExport(entity:GetAllComponents()))
            LC['log'].Debug(string.format('Saved dump file: %s', filename))
        end
    }
}
local function RegisterCommands()
    for _, command in ipairs(commands) do
        LC['log'].Debug(string.format('Registered command %s', command.name))
        Ext.RegisterConsoleCommand(command.name, command.func)
    end
end
RegisterCommands()
