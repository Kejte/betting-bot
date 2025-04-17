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
from core.handlers import get_max_money_fork

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
    dp.callback_query.register(handlers.create_purchase_request, F.data.startswith('purchase_'))
    dp.callback_query.register(handlers.update_purchase_request, F.data.startswith('upd_payment'))
    dp.callback_query.register(handlers.retrieve_subcription, F.data == 'actual_subscribe')
    dp.callback_query.register(handlers.activate_trial_period, F.data.startswith('activate_trial'))
    dp.callback_query.register(handlers.pre_create_purchase_request, F.data.startswith('pre_purchase'))
    dp.callback_query.register(handlers.get_promocodes_list,F.data.startswith('promocodes'))
    dp.callback_query.register(handlers.retrieve_promocode_message,F.data.startswith('promocode'))    
    dp.callback_query.register(handlers.activate_promocode_handler, F.data.startswith('activate_promo'))
    dp.callback_query.register(handlers.refferal_program, F.data == 'refferal_system')
    dp.callback_query.register(handlers.payout_request, F.data.startswith('payout_'))
    dp.callback_query.register(handlers.accept_payout_request, F.data.startswith('accept_payout_'))
    dp.callback_query.register(handlers.get_user_id_for_mailing, F.data == 'mail_user')
    dp.message.register(handlers.get_message_for_mailing, states.MailingState.GET_TELEGRAM_ID)
    dp.message.register(handlers.mail_message, states.MailingState.GET_MESSAGE)
    dp.callback_query.register(handlers.admin_pannel, F.data == 'admin')
    dp.callback_query.register(handlers.mailing_update_log, F.data == 'update_log_mailing')

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        # loop = asyncio.get_event_loop()
        # loop.create_task(shedule_message(bot))
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

async def shedule_message(bot: Bot):
    while True:
        await get_max_money_fork(bot)
        await asyncio.sleep(1800)

if __name__ == '__main__':
    asyncio.run(load_bot())