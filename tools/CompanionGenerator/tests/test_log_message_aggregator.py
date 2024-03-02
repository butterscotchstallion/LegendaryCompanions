from companiongenerator.log_message import (
    CriticalErrorMessage,
    ErrorMessage,
    LogMessage,
    LogMessageLevel,
)
from companiongenerator.log_message_aggregator import LogMessageAggregator


def test_log_message_aggregator():
    aggregator = LogMessageAggregator()
    module_name = "TestModule"
    message = "Testing the error aggregator!"
    error_message = ErrorMessage(message=message, module_name=module_name)
    error_message_output: str = aggregator._get_formatted_message(error_message)

    assert error_message_output.startswith(
        f"[{module_name}]"
    ), "Log message doesn't start with the module name"
    assert message in error_message_output


def test_has_errata():
    aggregator = LogMessageAggregator()
    module_name = "TestModule"
    message = "Testing the error aggregator!"
    error_message = ErrorMessage(message=message, module_name=module_name)
    info_message = LogMessage(message="Regular info message", module_name=module_name)

    aggregator.log(
        CriticalErrorMessage(message="Critical error message", module_name=module_name)
    )
    assert (
        aggregator.has_critical_errata()
    ), "Failed to verify critical error message count"

    aggregator.log(error_message)
    aggregator.log(info_message)

    info_messages = aggregator.get_messages_by_level(LogMessageLevel.info)

    assert len(info_messages) == 1, "Failed to verify info message count"
    assert aggregator.has_errata(), "Failed to verify error message count"
