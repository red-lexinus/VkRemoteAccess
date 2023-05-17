import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types.bot_command import BotCommand as BtCmd

from OtherModule import CONFIG
from OtherModule.Logger import logger
from handlers import (base, help, commands, setting, commenting)
from TgModule.bot_server import Server
from DbManagerModule import getter


async def set_bot_commands(bot: Bot):
    await bot.set_my_commands([
        BtCmd(command='/my_answers', description='Мои, быстрые ответ'),
        BtCmd(command='/my_groups', description='Мои группы'),
        BtCmd(command='/my_tokens', description='Мои токены'),
        BtCmd(command='/account', description='Мой аккаунт'),
        BtCmd(command='/help', description='Помощь'),
        BtCmd(command='/start', description='Запуск бота'),
    ])


# @logger.catch
async def start_bot() -> None:
    bot = Bot(CONFIG.TG_TOKEN)

    bot = Bot(CONFIG.TG_TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        commands.router,
        setting.fms_router, commenting.fms_router,
        help.cb_router, setting.cb_router, commenting.cb_router,
        base.router,
    )

    # await set_bot_commands(bot)
    server = Server(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    tasks = [
        asyncio.create_task(dp.start_polling(bot)),
        server.startup(300, 5),
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(start_bot())