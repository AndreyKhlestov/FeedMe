import sys

from environs import Env
from loguru import logger


env = Env()
env.read_env()

"""Tokens"""
BOT_TOKEN = env.str("BOT_TOKEN")

"""Loggers"""
logger.remove()
log_format_base = (
    " | "
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<yellow>{file.name}:{function}</yellow>:"
    "<fg #006400>{line}</fg #006400>\n"
    "{message}"
)
log_formats = {
    "INFO": f" <blue>{{level}}</blue>{log_format_base}",
    "DEBUG": f" <cyan>{{level}}</cyan>{log_format_base}",
    "WARNING": f" <yellow>{{level}}</yellow>{log_format_base}",
    "ERROR": f" <red>{{level}}</red>{log_format_base}",
}


def create_filter(level):
    return lambda record: record["level"].name == level


log_format_file = (
    " {level} | {time:YYYY-MM-DD HH:mm:ss} | "
    "{file.name}:{function}:{line}\n{message}"
)

for level, log_format in log_formats.items():
    logger.add(
        sys.stdout,
        format=log_format,
        level=level,
        filter=create_filter(level),
    )

logger.add(
    "bot.log",
    rotation="500 MB",
    retention="10 days",
    format=log_format_file,
)

"""Redis"""
redis_host = env.str("REDIS_HOST", None)
redis_port = env.str("REDIS_PORT", None)

"""Django"""
super_user_name = env.str("SUPER_USER_NAME")
super_user_pass = env.str("SUPER_USER_PASS")
