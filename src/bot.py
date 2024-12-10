import asyncio 
import logging

from aiogram import Bot, Dispatcher

from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from aiogram.fsm.storage.memory import MemoryStorage

from configs.config_reader import cfg
import handlers as handlers


async def main() -> None:
    bot = Bot(token=cfg.bot_token.get_secret_value(),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.include_router(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="logs.log",filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    asyncio.run(main())