--[[
-- BookEventHandler!
--]]
local handler = {}

--[[
-- When a book is created:
------------------------------------------------
-- 1. Check if it's one of ours
-- 2. Check if the pages match the ones we have
-- 3. Get book based on this information
-- @param item1TplId string
-- @param item2TplId string
-- @param bookTplId string
-- @return void
--]]
function handler.HandleBookCreated(item1TplId, item2TplId, bookTplId)
    local books = LC['configUtils'].GetBooksWithIntegrationName()
    local book  = LC['configUtils'].GetBookByBookTplId(books, bookTplId)

    if book then
        local pages = {
            item1TplId,
            item2TplId,
        }
        local pagesMatch = LC['configUtils'].IsPageMatch(book, pages)
        if pagesMatch then
            LC['log'].Debug(string.format('"%s" created!', book['name']))

            LC['creatureManager'].OnBeforeSpawn(book)
            LC['creatureManager'].SpawnCreatureUsingStrategy(book)
        else
            LC['log'].Debug(string.format('%s and %s not found in pages', item1TplId, item2TplId))
        end
    else
        LC['log'].Debug(string.format('Book %s created but not found in config list', bookTplId))
    end
end

LC['bookEventHandler'] = handler
