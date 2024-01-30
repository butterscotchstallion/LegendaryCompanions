from loguru import logger

logger.add(
    "../logs/LC-Automation.log",
    colorize=True,
    format="<level>{message}</level>",
    rotation="1 day",
)
