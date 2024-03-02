from datetime import datetime
from enum import StrEnum
from typing import NotRequired, Required, Unpack

from typing_extensions import TypedDict


class LogMessageLevel(StrEnum):
    info = "INFO"
    error = "ERROR"
    # These don't exist on the logger currently
    # warn = "WARN"
    critical = "CRITICAL"


class LogMessageKeywords(TypedDict):
    message: Required[str]
    module_name: Required[str]
    level: NotRequired[LogMessageLevel]


class LogMessage:
    message: str
    module_name: str
    level: LogMessageLevel
    timestamp: datetime

    def __init__(self, **kwargs: Unpack[LogMessageKeywords]):
        self.timestamp = datetime.now()
        self.message = kwargs["message"]
        self.module_name = kwargs["module_name"]
        self.level = LogMessageLevel.info

        if "level" in kwargs:
            self.level = kwargs["level"]


class InfoMessage(LogMessage):
    def __init__(self, **kwargs: Unpack[LogMessageKeywords]):
        super().__init__(**kwargs)
        self.level = LogMessageLevel.info


class ErrorMessage(LogMessage):
    def __init__(self, **kwargs: Unpack[LogMessageKeywords]):
        super().__init__(**kwargs)
        self.level = LogMessageLevel.error


class CriticalErrorMessage(LogMessage):
    def __init__(self, **kwargs: Unpack[LogMessageKeywords]):
        super().__init__(**kwargs)
        self.level = LogMessageLevel.critical
