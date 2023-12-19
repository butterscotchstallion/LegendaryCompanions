local muffinLogger = {}
local logPrefix    = '[LC]'

--The annotations for the print functions are NYI
---@param message string
---@param level string
function muffinLogger.Log(message, level)
    local fmtMsg = string.format('%s[%s] %s', logPrefix, level, message)
    if level == 'CRITICAL' then
        Ext.Utils.PrintError(fmtMsg)
    elseif level == 'WARN' then
        Ext.Utils.PrintWarning(fmtMsg)
    elseif level == 'INFO' or level == 'DEBUG' or not level then
        _P(fmtMsg)
    end
end

---@param message string
function muffinLogger.Debug(message)
    if LC['logLevel'] == 'DEBUG' then
        muffinLogger.Log(message, 'DEBUG')
    end
end

---@param message string
function muffinLogger.Info(message)
    muffinLogger.Log(message, 'INFO')
end

---@param message string
function muffinLogger.Warn(message)
    muffinLogger.Log(message, 'WARN')
end

---@param message string
function muffinLogger.Critical(message)
    muffinLogger.Log(message, 'CRITICAL')
end

LC['log']      = muffinLogger
--Shortcuts
LC['Debug']    = muffinLogger.Debug
LC['Info']     = muffinLogger.Info
LC['Warn']     = muffinLogger.Warn
LC['Critical'] = muffinLogger.Critical
