--[[
Commands for SE console

Credit: The below code is based on code provided by FallenStar.
]]
local commands = {
    {
        name = 'dumpentity',
        params = 'uuid, filename',
        --@param cmd string
        --@param uuid string
        --@param filename string
        func = function (cmd, uuid, filename)
            local hostGUID = tostring(Osi.GetHostCharacter())
            --@type string
            if uuid == 'host' then
                uuid = hostGUID
            end
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
