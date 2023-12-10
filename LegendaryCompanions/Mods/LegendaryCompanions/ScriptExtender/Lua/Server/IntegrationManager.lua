local intMgr       = {}
LC['integrations'] = {}

-- @param name string
-- @param config table
local function addIntegration(config)
    local numBooks = 0
    local name     = config['name']
    if not LC['integrations'][name] then
        numBooks                 = #config['books']
        LC['integrations'][name] = config
        local logMsg             = string.format('Integration loaded: %s (%s books)', name, numBooks)
        table.insert(LC['integrationLogMessages'], logMsg)
    else
        LC['log'].Critical('Attempting to add config that exists')
    end
end

intMgr.addIntegration    = addIntegration
LC['integrationManager'] = intMgr
