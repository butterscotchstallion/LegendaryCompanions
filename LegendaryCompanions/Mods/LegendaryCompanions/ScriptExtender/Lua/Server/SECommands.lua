--[[
Commands for SE console
]]
local commands = {
    {
        --Credit: This command is based on code provided by FallenStar.
        name = 'dumpentity',
        params = 'uuid, filename',
        ---@param cmd string
        ---@param uuid string
        ---@param filename string
        func = function (cmd, uuid, filename)
            local hostGUID = tostring(Osi.GetHostCharacter())
            if uuid == 'host' then
                uuid = hostGUID
            end
            local entity = Ext.Entity.Get(uuid)
            filename = (filename or uuid) .. '.json'
            Ext.IO.SaveFile(filename, Ext.DumpExport(entity:GetAllComponents()))
            LC['log'].Debug(string.format('Saved dump file: %s', filename))
        end
    },
    {
        name = 'createhere',
        params = 'uuid',
        ---@param cmd string
        ---@param uuid string
        func = function (cmd, uuid)
            if uuid then
                local x, y, z = Osi.GetPosition(tostring(Osi.GetHostCharacter()))
                x = tonumber(x)
                if x and y and z then
                    LC['log'].Debug(string.format('Creating %s at position %s %s %s', uuid, x, y, z))
                    local spawnUUID = Osi.CreateAt(uuid, x, y, z, 0, 1, '')
                    if spawnUUID then
                        LC['Debug']('Create successful: UUID = ' .. spawnUUID)
                        Osi.RequestPing(x, y, z, spawnUUID, Osi.GetHostCharacter())
                    else
                        LC['Debug']('Failed to create ' .. uuid)
                    end
                end
            else
                LC['Critical']('No UUID specified')
            end
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
