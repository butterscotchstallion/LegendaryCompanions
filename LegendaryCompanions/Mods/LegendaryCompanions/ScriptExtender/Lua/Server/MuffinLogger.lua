MuffinLogger = {}
local LOG_PREFIX = '[LC]'

function MuffinLogger.Log(message, level)
    local fmt_msg = string.format('%s[%s] %s', LOG_PREFIX, level, message)
    if level == 'CRITICAL' then
        Ext.Utils.PrintError(fmt_msg)
    elseif level == 'WARN' then
        Ext.Utils.PrintWarning(fmt_msg)
    elseif level == 'INFO' or level == 'DEBUG' or not level then
        _P(fmt_msg)
    end
end

function MuffinLogger.Debug(message)
    if LC_LOG_LEVEL == 'DEBUG' then
        MuffinLogger.log(message, 'DEBUG')
    end
end

function MuffinLogger.Info(message)
    MuffinLogger.log(message, 'INFO')
end

function MuffinLogger.Warn(message)
    MuffinLogger.log(message, 'WARN')
end

function MuffinLogger.Critical(message)
    MuffinLogger.log(message, 'CRITICAL')
end
