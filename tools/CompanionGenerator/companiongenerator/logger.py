import sys

from loguru import logger

logger.add(sys.stdout, colorize=True, format="<level>{message}</level>")
