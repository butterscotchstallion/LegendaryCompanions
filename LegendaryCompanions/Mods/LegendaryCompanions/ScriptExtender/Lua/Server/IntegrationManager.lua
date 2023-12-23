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
---@param config table Integration config
---@return table errors
local function IsValidConfiguration(config)
    local messages = {
        ['errors']   = {},
        ['warnings'] = {},
    }
    local isInvalidConfigName = not config['name'] or string.len(config['name']) == 0

    if isInvalidConfigName then
        table.insert(messages['errors'], 'Integration name must not be empty')
    else
        local configExists = LC['configUtils'].GetConfigByName(config['name'])

        if configExists then
            table.insert(messages['errors'], 'Integration name must be unique')
        else
            --Check books, and if we have any then check book contents
            local hasNoBooks = not config['books'] or #config['books'] == 0
            if hasNoBooks then
                table.insert(messages['errors'], 'Integration must have at least one book')
            else
                for _, book in pairs(config['books']) do
                    if not book['name'] or string.len(book['name']) == 0 then
                        table.insert(
                            messages['errors'],
                            string.format(
                                'Integration book name must not be empty',
                                book['name']
                            )
                        )
                    end

                    local pages = book['pages']
                    if not pages or #pages < 2 then
                        table.insert(
                            messages['errors'],
                            string.format(
                                'Integration book "%s" must have at least two pages',
                                book['name']
                            )
                        )
                    end

                    --Check book type specific features
                    local isUpgradeBook    = LC['configUtils'].IsUpgradeBook(book)
                    local isPartyBuffsBook = LC['configUtils'].IsPartyBuffsBook(book)
                    if isPartyBuffsBook then
                        --Must have at least one party buff
                        if not book['partyBuffs'] or #book['partyBuffs'] then
                            table.insert(
                                messages['errors'],
                                string.format(
                                    'Integration upgrade book "%s" must have at least one party buff',
                                    book['name']
                                )
                            )
                        end
                    elseif isUpgradeBook then
                        local upgradeInfo    = book['upgrade'] or {}
                        local bookEntityUUID = upgradeInfo['entityUUID']
                        local passives       = upgradeInfo['passives']

                        --Check entityUUID
                        if not bookEntityUUID or string.len(bookEntityUUID) == 0 then
                            table.insert(
                                messages['errors'],
                                string.format(
                                    'Integration upgrade book %s must have an entityUUID',
                                    book['name']
                                )
                            )
                        end

                        --Check passives
                        if not passives or #passives == 0 then
                            table.insert(
                                messages['errors'],
                                string.format(
                                    'Integration upgrade book "%s" must have at least one passive',
                                    book['name']
                                )
                            )
                        end
                    else
                        --Regular book - check spells
                        local hasNoSpells = not book['summonSpells'] or #book['summonSpells'] == 0
                        if hasNoSpells then
                            table.insert(
                                messages['errors'],
                                string.format(
                                    'Integration book "%s" must have at least one summoning spell',
                                    book['name']
                                )
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
---@param config table Integration config
---@return boolean Returns true if integration is valid
local function AddIntegration(config)
    local integrationDisabled = config['enabled'] == false
    local isDebugMode         = LC['logLevel'] == 'DEBUG'
    local isDebugConfig       = isDebugMode and config['name'] == 'LC_Debug_Integration'
    local numBooks            = #config['books']
    local name                = config['name']
    local messages            = {
        ['Info']     = {},
        ['Warn']     = {},
        ['Critical'] = {},
        ['Debug']    = {},
    }

    -- Do not add disabled integrations
    if integrationDisabled then
        return false
    end

    --[[
    Don't print debug messages about the debug configuration
    if we're not debugging. We don't want to confuse anyone
    ]]
    if not isDebugMode and isDebugConfig then
        return false
    end

    --[[

    END EARLY RETURNS

    ]]

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
        table.insert(messages['Info'], logMsg)
    else
        config['enabled'] = false
        table.insert(
            messages['Critical'],
            string.format('%s has been disabled! Errors below:', name)
        )

        if #validityInfo['errors'] > 0 then
            for _, error in pairs(validityInfo['errors']) do
                table.insert(messages['Critical'], error)
            end
        end

        if #validityInfo['warnings'] > 0 then
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

    return validityInfo['isValid']
end

intMgr.AddIntegration    = AddIntegration
LC['integrationManager'] = intMgr
