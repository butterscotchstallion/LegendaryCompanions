--[[
-- BookEventHandler!
--]]
local LCBookEventHandler = {}

function string.starts(String, Start)
    return string.sub(String, 1, string.len(Start)) == Start
end

local function GetTplNameByBookTplId(books, bookTplId)
    _D(books)
    for _, bookTplName in pairs(books) do
        if string.starts(bookTplId, bookTplName) then
            return bookTplName
        end
    end
end

local function GetTplNameByPageTplId(books, bookTplId, itemPageTplId)
    if books[bookTplId] then
        for _, pageTplId in pairs(books[bookTplId]) do
            if string.starts(itemPageTplId, pageTplId) then
                return pageTplId
            end
        end
    else
        MuffinLogger.Critical('Invalid bookTplId ' .. bookTplId)
    end
end

function LCBookEventHandler.HandleBookCreated(item1TplId, item2TplId, bookTplId)
    local books       = LCConfigUtils.GetBooksWithIntegrationName()
    local bookTplName = GetTplNameByBookTplId(books, bookTplId)

    if bookTplName then
        local book = LCConfigUtils.GetBookByTplName(bookTplName)
        if bookTplName and book then
            local page1TplId = GetTplNameByPageTplId(books, bookTplName, item1TplId)
            local page2TplId = GetTplNameByPageTplId(books, bookTplName, item2TplId)
            if page1TplId and page2TplId then
                MuffinLogger.Debug(string.format('"%s" created!', bookTplName))
                -- SpawnCreature based on book
                local templateId = LCConfigUtils.GetTemplateByBookInfo(book)
                local isFriendly = book['isFriendly'] or true
                if templateId then
                    LC['CreatureManager'].SpawnCreatureByTemplateId(templateId, isFriendly)
                else
                    MuffinLogger.Debug(string.format('No templates for book %s', bookTplName))
                    -- Find creature based on rarity?
                end
            else
                MuffinLogger.Debug(string.format('%s and %s not found in ingredients', item1TplId, item2TplId))
            end
        else
            MuffinLogger.Debug(string.format('Book %s created but not one of ours', bookTplName))
        end
    else
        MuffinLogger.Debug(string.format('Could not find book with tpl id: %s', bookTplId))
    end
end

LC['BookEventHandler'] = LCBookEventHandler
