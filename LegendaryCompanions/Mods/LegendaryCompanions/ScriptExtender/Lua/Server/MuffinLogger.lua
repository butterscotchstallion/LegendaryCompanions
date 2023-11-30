MuffinLogger = {}
local LOG_PREFIX = '[SOTA]'

function MuffinLogger.log(message, level)
    local fmt_msg = string.format('%s[%s] %s', LOG_PREFIX, level, message)
    if level == 'CRITICAL' then
        Ext.Utils.PrintError(fmt_msg)
    elseif level == 'WARN' then
        Ext.Utils.PrintWarning(fmt_msg)
    elseif level == 'INFO' or level == 'DEBUG' or not level then
        _P(fmt_msg)
    end
end

function MuffinLogger.debug(message)
    if SOTA_LOG_LEVEL == 'DEBUG' then
        MuffinLogger.log(message, 'DEBUG')
    end
end

function MuffinLogger.info(message)
    MuffinLogger.log(message, 'INFO')
end

function MuffinLogger.warn(message)
    MuffinLogger.log(message, 'WARN')
end

function MuffinLogger.critical(message)
    MuffinLogger.log(message, 'CRITICAL')
end
