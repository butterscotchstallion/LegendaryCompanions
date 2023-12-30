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

--[[
Validates configuration.

1. Check if name is blank
2. If name is not blank, check if name is unique
3. If name is valid, check if there is at least one book
4. If books are valid, check if each book has at least one spell
]]
---@param config table Integration config
---@return table errors
local function IsValidConfiguration(config)
    local messages = {
        ['isValid']  = false,
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
                                'Integration book "%s" name must not be empty',
                                book['name']
                            )
                        )
                    else
                        --Check book name format
                        if not LC['configUtils'].IsLCBook(book['name']) then
                            table.insert(
                                messages['errors'],
                                string.format(
                                    'Integration book "%s" must start with "BOOK_LC_"',
                                    book['name']
                                )
                            )
                        end
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
                    local isSummonBook     = LC['configUtils'].IsSummonBook(book)
                    if isPartyBuffsBook then
                        --Must have at least one party buff
                        if not book['buffPartySpells'] or #book['buffPartySpells'] == 0 then
                            table.insert(
                                messages['errors'],
                                string.format(
                                    'Integration upgrade book "%s" must have at least one party buff',
                                    book['name']
                                )
                            )
                        end
                    elseif isUpgradeBook then
                        local upgradeInfo            = book['upgrade'] or {}
                        local bookEntityUUID         = upgradeInfo['entityUUID']
                        local passives               = upgradeInfo['passives']
                        local upgradeScrollUUID      = book['upgradeScrollUUID']
                        local upgradeScrollSpellName = book['upgradeScrollSpellName']

                        --Check scroll UUID
                        if not upgradeScrollUUID or string.len(upgradeScrollUUID) ~= 36 then
                            table.insert(
                                messages['errors'],
                                string.format(
                                    'Integration upgrade book "%s" must have a valid upgradeScrollUUID that is 36 characters',
                                    book['name']
                                )
                            )
                        end

                        --Check scroll spell name
                        if not upgradeScrollSpellName then
                            table.insert(
                                messages['errors'],
                                string.format(
                                    'Integration upgrade book "%s" must have a valid upgradeScrollSpellName',
                                    book['name']
                                )
                            )
                        end

                        --Check entityUUID
                        if not bookEntityUUID or string.len(bookEntityUUID) ~= 36 then
                            table.insert(
                                messages['errors'],
                                string.format(
                                    'Integration upgrade book "%s" must have a valid entityUUID that is 36 characters',
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
                    elseif isSummonBook then
                        --Regular book - check scroll
                        local isInvalidScrollUUID = not book['summonScrollUUID']
                            or string.len(book['summonScrollUUID']) ~= 36
                        if isInvalidScrollUUID then
                            table.insert(
                                messages['errors'],
                                string.format(
                                    'Integration book "%s" must have a summonScrollUUID that is 36 characters',
                                    book['name']
                                )
                            )
                        end

                        if book['summonSpells'] then
                            for _, spell in pairs(book['summonSpells']) do
                                if spell['name'] then
                                    local error =
                                        string.format(
                                            'Integration book "%s" "name" field is deprecated and not used! Be sure to set "summonScrollUUID"',
                                            book['name']
                                        )
                                    table.insert(
                                        messages['warnings'],
                                        error
                                    )
                                end
                            end
                        end
                    else
                        table.insert(
                            messages['errors'],
                            string.format(
                                'Integration book "%s" has an invalid type: %s',
                                book['name'],
                                book['type']
                            )
                        )
                    end
                end
            end
        end
    end

    messages['isValid'] = #messages['errors'] == 0

    return messages
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
        local numErrors = #validityInfo['errors']
        local errorWord = 'errors'
        if numErrors == 1 then
            errorWord = 'error'
        end
        table.insert(
            messages['Critical'],
            string.format(
                'Integration "%s" has been disabled! %s %s below:',
                name,
                numErrors,
                errorWord
            )
        )

        if numErrors > 0 then
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
