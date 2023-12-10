local MuffinLogger = {}
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
    if LC['logLevel'] == 'DEBUG' then
        MuffinLogger.Log(message, 'DEBUG')
    end
end

function MuffinLogger.Info(message)
    MuffinLogger.Log(message, 'INFO')
end

function MuffinLogger.Warn(message)
    MuffinLogger.Log(message, 'WARN')
end

function MuffinLogger.Critical(message)
    MuffinLogger.Log(message, 'CRITICAL')
end

LC['log'] = MuffinLogger
