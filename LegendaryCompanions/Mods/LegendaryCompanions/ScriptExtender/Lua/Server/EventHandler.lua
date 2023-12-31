--[[
Event Handler
]]

--[[
When summoning via spell, we have to listen for this event to get
the GUID of the entity
]]
---@param objectTemplate string
---@param originalUUID string
---@param levelName string
local function OnEnteredLevel(objectTemplate, originalUUID, levelName)
    if LC['creatureManager']['isExpectingSummonBook'] then
        local objectUUID = LC['creatureManager'].GetGUIDFromTpl(objectTemplate)
        LC['log'].Debug(string.format('%s entered (%s)!', objectUUID, levelName))
        LC['creatureManager'].HandleCreatureSpawn(
            tostring(objectUUID),
            LC['creatureManager']['isExpectingSummonBook']
        )
    end
end

local function PrintVersionMessage()
    local mod = Ext.Mod.GetMod(ModuleUUID)
    if mod then
        local version    = mod.Info.ModVersion
        local versionMsg = string.format(
            'LegendaryCompanions v%s.%s.%s',
            version[1],
            version[2],
            version[3]
        )
        LC['Info'](versionMsg)
    end
end

local function PrintIntegrationMessages()
    for _, msg in pairs(LC['integrationLogMessages']['Info']) do
        LC['Info'](msg)
    end
    for _, msg in pairs(LC['integrationLogMessages']['Warn']) do
        LC['Warn'](msg)
    end
    for _, msg in pairs(LC['integrationLogMessages']['Critical']) do
        LC['Critical'](msg)
    end
    for _, msg in pairs(LC['integrationLogMessages']['Debug']) do
        LC['Debug'](msg)
    end
    local configTotals = LC['configUtils'].GetConfigTotals()
    LC['Info'](
        string.format(
            'Integrations: %s/%s configs enabled',
            configTotals['enabledCount'],
            configTotals['totalCount']
        )
    )
end

local function OnSessionLoaded()
    PrintVersionMessage()
    PrintIntegrationMessages()
end

--[[
Finds scroll and adds to inventory based on the book
that was closed and its type
]]
---@param item string Item template name
---@param character string Character UUID
local function OnGameBookInterfaceClosed(item, character)
    local isLCBook = LC['configUtils'].IsLCBook(item)
    if isLCBook then
        local books = LC['configUtils'].GetBooksWithIntegrationName()
        local book  = LC['configUtils'].GetBookByBookTplId(books, item)
        if book then
            local scroll = LC['configUtils'].GetScrollFromBook(book)
            if scroll then
                LC['Debug']('Adding scroll to inventory!')
                LC['configUtils'].AddScrollToInventory(scroll)
            end
        end
    end
end

---@param caster GUIDSTRING
---@param spellName string
---@param spellType string
---@param spellElement string
---@param storyActionID integer
local function OnCastSpell(caster, spellName, spellType, spellElement, storyActionID)
    if LC['creatureManager']['isExpectingSummonBook'] then
        LC['creatureManager'].HandleSummonCompanionSpell(LC['creatureManager']['isExpectingSummonBook'])
        LC['creatureManager']['isExpectingSummonBook'] = nil
    elseif LC['creatureManager']['isExpectingUpgradeBook'] then
        LC['creatureManager'].HandleUpgradeCompanionSpell(LC['creatureManager']['isExpectingUpgradeBook'])
        LC['creatureManager']['isExpectingUpgradeBook'] = nil
    end
end

---@param caster GUIDSTRING
---@param spell string
---@param isMostPowerful integer
---@param hasMultipleLevels integer
local function OnPreviewingSpell(caster, spell, isMostPowerful, hasMultipleLevels)
    local summonBookType   = LC['configUtils'].GetSummonBookType()
    local upgradeBookType  = LC['configUtils'].GetCompanionUpgradeBookType()
    local summonSpellBook  = LC['configUtils'].GetBookBySpellName(spell, summonBookType)
    local upgradeSpellBook = LC['configUtils'].GetBookBySpellName(spell, upgradeBookType)
    if summonSpellBook then
        LC['creatureManager']['isExpectingSummonBook'] = summonSpellBook
        LC['Debug']('Expecting summon: ' .. spell)
    elseif upgradeSpellBook then
        LC['creatureManager']['isExpectingUpgradeBook'] = upgradeSpellBook
        LC['Debug']('Expecting upgrade: ' .. spell)
    end
end

--Listeners
Ext.Events.SessionLoaded:Subscribe(OnSessionLoaded)
Ext.Osiris.RegisterListener('EnteredLevel', 3, 'after', OnEnteredLevel)
Ext.Osiris.RegisterListener('GameBookInterfaceClosed', 2, 'after', OnGameBookInterfaceClosed)
Ext.Osiris.RegisterListener('CastSpell', 5, 'after', OnCastSpell)
Ext.Osiris.RegisterListener('StartedPreviewingSpell', 4, 'after', OnPreviewingSpell)
