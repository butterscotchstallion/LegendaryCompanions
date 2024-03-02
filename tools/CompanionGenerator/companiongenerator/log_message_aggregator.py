from companiongenerator.log_message import (
    LogMessage,
    LogMessageLevel,
)
from companiongenerator.logger import logger


class LogMessageAggregator:
    messages: set[LogMessage]

    def __init__(self):
        self.messages: set[LogMessage] = set()

    def _get_formatted_message(self, message: LogMessage) -> str:
        return f"[{message.module_name}] {message.level}: {message.message}]"

    def log(self, message: LogMessage):
        self.messages.add(message)
        formatted_message = self._get_formatted_message(message)
        getattr(logger, message.level.lower())(formatted_message)

    def get_messages_by_level(self, level: LogMessageLevel) -> list[LogMessage]:
        return [msg for msg in self.messages if msg.level == level]

    def get_error_messages(self) -> list[LogMessage]:
        return self.get_messages_by_level(LogMessageLevel.error)

    def get_critical_error_messages(self) -> list[LogMessage]:
        return self.get_messages_by_level(LogMessageLevel.critical)

    def has_errata(self) -> bool:
        return len(self.get_error_messages()) > 0

    def has_critical_errata(self) -> bool:
        return len(self.get_critical_error_messages()) > 0
