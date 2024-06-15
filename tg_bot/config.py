from environs import Env
from tg_bot.settings_logger import logger


env = Env()
env.read_env()

"""Tokens"""
BOT_TOKEN = env.str("BOT_TOKEN")


"""Redis"""
redis_host = env.str("REDIS_HOST", None)
redis_port = env.str("REDIS_PORT", None)

"""Django"""
super_user_name = env.str("SUPER_USER_NAME")
super_user_pass = env.str("SUPER_USER_PASS")
site_url = env.str('HOST_IP')