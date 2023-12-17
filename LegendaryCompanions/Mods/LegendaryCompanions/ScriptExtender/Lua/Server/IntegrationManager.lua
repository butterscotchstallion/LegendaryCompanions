--[[
IntegrationManager - Handles adding of new integrations
and validating the supplied configuration
]]
local intMgr                 = {}
LC['integrations']           = {}
LC['integrationLogMessages'] = {
    ['totalIntegrations'] = 0,
    ['Info']              = {},
    ['Warn']              = {},
    ['Critical']          = {},
    ['Debug']             = {},
}

--Validates configuration
--Check if name is blank
--If name is not blank, check if name is unique
--If name is valid, check if there is at least one book
--If books are valid, check if each book has at least one spell
---@param config table
---@return table
local function IsValidConfiguration(config)
    local messages = {
        ['errors']   = {},
        ['warnings'] = {},
    }
    local isInvalidConfigName = not config['name'] or string.len(config['name']) == 0

    if isInvalidConfigName then
        table.insert(messages['errors'], 'Integration name must not be empty')
    else
        local configExists = LC['configUtils'].getConfigByName(config['name'])

        if configExists then
            table.insert(messages['errors'], 'Integration name must be unique')
        else
            --Check books, and if we have any then check book contents
            local hasNoBooks = not config['books'] or #config['books'] == 0
            if hasNoBooks then
                table.insert(messages['errors'], 'Integration must have at least one book')
            else
                for _, book in pairs(config['books']) do
                    local isUpgradeBook = LC['configUtils'].IsUpgradeBook(book)
                    if not book['name'] or string.len(book['name']) == 0 then
                        table.insert(
                            messages['errors'],
                            'Integration book name must not be empty'
                        )
                    end

                    local pages = book['pages']
                    if not pages or #pages < 2 then
                        table.insert(
                            messages['errors'],
                            'Integration book name must have at least one two pages'
                        )
                    end

                    --If this is an upgrade book, check out those options
                    if isUpgradeBook then
                        local upgradeInfo    = book['upgrade']
                        local bookEntityUUID = upgradeInfo['entityUUID']
                        local passives       = upgradeInfo['passives']
                        if not bookEntityUUID or string.len(bookEntityUUID) == 0 then
                            table.insert(
                                messages['errors'],
                                'Integration upgrade book must have an entityUUID'
                            )
                        end
                        if not passives or #passives == 0 then
                            table.insert(
                                messages['errors'],
                                'Integration upgrade book must have at least one passive'
                            )
                        end
                    else
                        --Regular book - check spells
                        local hasNoSpells = not book['summonSpells'] or #book['summonSpells'] == 0
                        if hasNoSpells then
                            table.insert(
                                messages['errors'],
                                string.format('Integration must have at least one summoning spell for book "%s"!',
                                    book['name'])
                            )
                        end
                    end
                end
            end
        end
    end

    return {
        ['isValid']  = #messages['errors'] == 0,
        ['errors']   = messages['errors'],
        ['warnings'] = messages['warnings'],
    }
end

--Validates and adds config if valid, with log messages
---@param config table
local function AddIntegration(config)
    local isDebugMode   = LC['logLevel'] == 'DEBUG'
    local isDebugConfig = isDebugMode and config['name'] == 'LC_Debug_Integration'
    local numBooks      = 0
    local name          = config['name']
    local messages      = {
        Info     = {},
        Warn     = {},
        Critical = {},
        Debug    = {},
    }

    --[[
    Don't print debug messages about the debug configuration
    if we're not debugging. We don't want to confuse anyone
    ]]
    if not isDebugMode and isDebugConfig then
        return false
    end

    numBooks                                          = #config['books']
    --Used in the start up messages for debugging
    LC['integrationLogMessages']['totalIntegrations'] = LC['integrationLogMessages']['totalIntegrations'] + 1

    --[[
        This is stored here instead of directly logging because I want
        to delay printing of the log messages until the first one, after
        all the bootstrap stuff. This is so all the messages are grouped
        together where I can see them.
    ]]
    local validityInfo = IsValidConfiguration(config)

    if validityInfo['isValid'] then
        --Integration valid; add it!
        table.insert(LC['integrations'], config)

        local booksWord = 'books'
        if numBooks == 1 then
            booksWord = 'book'
        end
        local logMsg = string.format(
            'Integration loaded: %s (%s %s)',
            name,
            numBooks,
            booksWord
        )
        --Add log message
        table.insert(messages['Info'], logMsg)
    else
        config['enabled'] = false
        table.insert(
            messages['Critical'],
            string.format('%s has been disabled! Errors below:', name)
        )

        if validityInfo['errors'] then
            for _, error in pairs(validityInfo['errors']) do
                table.insert(messages['Critical'], error)
            end
        end

        if validityInfo['warnings'] then
            for _, warning in pairs(validityInfo['warnings']) do
                table.insert(messages['Warn'], warning)
            end
        end
    end

    for severity, _ in pairs(messages) do
        for _, msg in pairs(messages[severity]) do
            local messagesBySeverity = LC['integrationLogMessages'][severity]

            if type(messagesBySeverity) == 'table' then
                table.insert(messagesBySeverity, msg)
            end
        end
    end
end

intMgr.AddIntegration    = AddIntegration
LC['integrationManager'] = intMgr
