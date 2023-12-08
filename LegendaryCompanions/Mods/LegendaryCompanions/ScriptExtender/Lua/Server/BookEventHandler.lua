--[[
-- BookEventHandler!
--]]
local LCBookEventHandler = {}

--[[
-- When a book is created:
------------------------------------------------
-- 1. Check if it's one of ours
-- 2. Check if the pages match the ones we have
-- 3. Get template based on book info
-- @param item1TplId string
-- @param item2TplId string
-- @param bookTplId string
-- @return void
--]]
function LCBookEventHandler.HandleBookCreated(item1TplId, item2TplId, bookTplId)
    local books = LCConfigUtils.GetBooksWithIntegrationName()
    local book  = LCConfigUtils.GetBookByBookTplId(books, bookTplId)

    if book then
        local pages = {
            item1TplId,
            item2TplId,
        }
        local pagesMatch = LCConfigUtils.IsPageMatch(book, pages)
        if pagesMatch then
            MuffinLogger.Debug(string.format('"%s" created!', book['name']))
            -- SpawnCreature based on book
            local templateId = LCConfigUtils.GetTemplateByBookInfo(book)

            if templateId then
                LC['CreatureManager'].SpawnCreatureByTemplateId(templateId, book)
            else
                MuffinLogger.Debug(string.format('No templates for book %s', book['name']))
                -- Find creature based on rarity?
            end
        else
            MuffinLogger.Debug(string.format('%s and %s not found in pages', item1TplId, item2TplId))
        end
    else
        MuffinLogger.Debug(string.format('Book %s created but not one of ours', bookTplId))
    end
end

LC['BookEventHandler'] = LCBookEventHandler
