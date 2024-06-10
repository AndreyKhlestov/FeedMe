import sys

from environs import Env
from loguru import logger

# from tg_bot.logs.logs_setup import loggers


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
log_format_info = " <blue>{level}</blue>" + log_format_base
log_format_debug = " <cyan>{level}</cyan>" + log_format_base
log_format_warning = " <yellow>{level}</yellow>" + log_format_base
log_format_error = " <red>{level}</red>" + log_format_base
log_format_file = (
    " {level} | {time:YYYY-MM-DD HH:mm:ss} | "
    "{file.name}:{function}:{line}\n{message}"
)
logger.add(
    sys.stdout,
    format=log_format_info,
    level="INFO",
    filter=lambda record: record["level"].name == "INFO",
)
logger.add(
    sys.stdout,
    format=log_format_debug,
    level="DEBUG",
    filter=lambda record: record["level"].name == "DEBUG",
)
logger.add(
    sys.stdout,
    format=log_format_warning,
    level="WARNING",
    filter=lambda record: record["level"].name == "INFO",
)
logger.add(
    sys.stdout,
    format=log_format_error,
    level="ERROR",
    filter=lambda record: record["level"].name == "ERROR",
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
