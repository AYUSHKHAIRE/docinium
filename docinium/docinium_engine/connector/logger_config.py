from loguru import logger

logger.add(
    "docinium_container.log",
    rotation="10 MB",
    retention="7 days",
    level="TRACE",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)