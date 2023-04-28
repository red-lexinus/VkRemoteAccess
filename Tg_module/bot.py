import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types.bot_command import BotCommand as BtCmd

from other_module import CONFIG
from handlers import (base, help, commands, setting)


async def set_bot_commands(bot: Bot):
    await bot.set_my_commands([
        BtCmd(command='/my_answers', description='Мои, быстрые ответ'),
        BtCmd(command='/my_groups', description='Мои группы'),
        BtCmd(command='/my_tokens', description='Мои токены'),
        BtCmd(command='/account', description='Мой аккаунт'),
        BtCmd(command='/help', description='Помощь'),
        BtCmd(command='/start', description='Запуск бота'),
    ])


async def start_bot() -> None:
    bot = Bot(CONFIG.TG_TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        setting.fms_router,
        help.cb_router, setting.cb_router,
        commands.router, base.router,
    )

    await set_bot_commands(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_bot())
