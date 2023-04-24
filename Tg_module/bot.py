import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types.bot_command import BotCommand as BtCmd
from other_module import CONFIG

from handlers import base, commands


async def start_bot() -> None:
    bot = Bot(CONFIG.TG_TOKEN)
    dp = Dispatcher()
    dp.include_routers(commands.router, base.router)
    await bot.set_my_commands([
        BtCmd(command='/help', description='Помощь, да инструкции'),
        BtCmd(command='/account', description='Мой аккаунт'),
        BtCmd(command='/my_groups', description='Мои группы'),
        BtCmd(command='/my_tokens', description='Мои токены'),
        BtCmd(command='/setting_groups', description='Настройка групп'),
        BtCmd(command='/setting_tokens', description='Настройка токенов'),
        BtCmd(command='/start', description='Запуск бота'),

    ])
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_bot())
