import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs
from config_data.config import Config, load_config
from dialogs.start.dialogs import start_dialog
from fluentogram import TranslatorHub
from handlers.commands import commands_router
from handlers.other import other_router
from middlewares.i18n import TranslatorRunnerMiddleware
from utils.i18n import create_translator_hub

# Настраиваем базовую конфигурацию логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s'
)

# Инициализируем логгер модуля
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main() -> None:

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Создаем объект типа TranslatorHub
    translator_hub: TranslatorHub = create_translator_hub()

    # Регистриуем роутеры в диспетчере
    dp.include_router(commands_router)
    dp.include_router(other_router)
    dp.include_router(start_dialog)

    # Регистрируем миддлварь для i18n
    dp.update.middleware(TranslatorRunnerMiddleware())

    # Запускаем функцию настройки проекта для работы с диалогами
    setup_dialogs(dp)
    # Запускаем polling
    await dp.start_polling(bot, _translator_hub=translator_hub)


asyncio.run(main())