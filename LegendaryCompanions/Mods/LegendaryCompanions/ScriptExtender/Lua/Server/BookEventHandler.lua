--[[
-- BookEventHandler!
--]]
local LCBookEventHandler = {}
-- template -> { ingredients }
local books = {
    ['BOOK_LC_Githzerai_Combined_Tome_3'] = {
        'BOOK_LC_Githzerai_TornPage_01',
        'BOOK_LC_Githzerai_TornPage_02'
    }
}

function string.starts(String, Start)
    return string.sub(String, 1, string.len(Start)) == Start
end

local function GetTplNameByBookTplId(bookTplId)
    for bookTplName, _ in pairs(books) do
        if string.starts(bookTplId, bookTplName) then
            return bookTplName
        end
    end
end

local function GetTplNameByPageTplId(bookTplId, itemPageTplId)
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
    local bookTplName = GetTplNameByBookTplId(bookTplId)
    if bookTplName then
        local page1TplId = GetTplNameByPageTplId(bookTplName, item1TplId)
        local page2TplId = GetTplNameByPageTplId(bookTplName, item2TplId)
        if page1TplId and page2TplId then
            MuffinLogger.Debug(string.format('"%s" created!', bookTplName))
        else
            MuffinLogger.Debug(string.format('%s and %s not found in ingredients', item1TplId, item2TplId))
        end
    else
        MuffinLogger.Debug(string.format('Book %s created but not one of ours', bookTplName))
    end
end

LC['BookEventHandler'] = LCBookEventHandler
