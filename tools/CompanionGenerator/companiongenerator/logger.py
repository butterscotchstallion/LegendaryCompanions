from loguru import logger

logger.add(
    "../logs/LC-Automation.log",
    colorize=True,
    format="<level>{time:YYYY-MM-DD at HH:mm:ss}{message}</level>",
    rotation="1 day",
)
