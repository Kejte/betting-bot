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
from core import fork_router

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
    dp.include_routers(fork_router.router)
    

    #etc handlers
    dp.message.register(handlers.hello_message, Command(commands='start'))
    dp.callback_query.register(handlers.hello_message,F.data=='main_menu')
    dp.callback_query.register(handlers.payments, F.data == 'payments')
    dp.callback_query.register(handlers.tariffs_list, F.data == 'tariffs')
    dp.callback_query.register(handlers.retrieve_tariff, F.data.startswith('tariff_'))
    dp.callback_query.register(handlers.feedback, F.data == 'feedback')
    dp.callback_query.register(handlers.tech_support, F.data == 'tech_support')
    dp.message.register(handlers.create_tech_support_report, states.TechSupportState.GET_TEXT)
    dp.callback_query.register(handlers.update_ticket, F.data == 'update_ticket')
    dp.message.register(handlers.create_update_ticket, states.UpdateTicketState.GET_TICKET_TEXT)
    dp.callback_query.register(handlers.update_log, F.data == 'update_log')
    dp.callback_query.register(handlers.public_offer, F.data == 'public_offer')
    dp.callback_query.register(handlers.create_purchase_request, F.data.startswith('purchase_'))
    dp.callback_query.register(handlers.update_purchase_request, F.data.startswith('upd_payment'))
    dp.callback_query.register(handlers.retrieve_subcription, F.data == 'actual_subscribe')
    
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(load_bot())