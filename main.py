import asyncio
import os
import logging
from core import handlers
from core.settings import settings
from aiogram import Bot, Dispatcher, F 
from aiogram.filters import Command
from utils.commands import set_commands
from aiogram.client.default import DefaultBotProperties
from utils import states
from core.middlewares import RegisterMiddleware


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен!')

async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот выключен!')

async def load_bot():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s] - %(name)s -'''
                               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
                        )
    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()

    # STAFF handlers
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.middleware.register(RegisterMiddleware())
    dp.callback_query.middleware.register(RegisterMiddleware())

    dp.message.register(handlers.hello_message, Command(commands='start'))
    dp.callback_query.register(handlers.hello_message,F.data=='main_menu')
    dp.callback_query.register(handlers.required_bookers_list, F.data.startswith('search_money'))
    dp.callback_query.register(handlers.optional_bookers_list, F.data.startswith('required_money'))
    dp.callback_query.register(handlers.search_fork,F.data.startswith('selected_money'))
    dp.callback_query.register(handlers.paginate_forks,F.data.startswith('paginate_money'))
    dp.callback_query.register(handlers.paginate_freebet_forks, F.data.startswith('paginate_freebet'))
    dp.callback_query.register(handlers.pre_calculate_fork, F.data.startswith('calculate_money_fork'))
    dp.callback_query.register(handlers.choice_freebet_booker, F.data.startswith('search_freebet'))
    dp.callback_query.register(handlers.get_freebet_amount,F.data.startswith('required_freebet'))
    dp.message.register(handlers.calculate_fork, states.CalculateMoneyForkState.GET_AMOUNT)
    dp.message.register(handlers.get_freebet_coef, states.FreebetDataState.GET_FREEBET_AMOUNT)
    dp.message.register(handlers.freebet_forks, states.FreebetDataState.GET_FREEBET_COEFF)
    dp.callback_query.register(handlers.payments, F.data == 'payments')
    dp.callback_query.register(handlers.tariffs_list, F.data == 'tariffs')
    dp.callback_query.register(handlers.retrieve_tariff, F.data.startswith('tariff_'))

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(load_bot())