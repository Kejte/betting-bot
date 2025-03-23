from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from utils import keyboards

from aiogram.fsm.context import FSMContext
from utils.states import TechSupportState, UpdateTicketState
from utils.funcs import get_tariffs, get_tariff, create_tech_support_ticket, create_update_support_ticket, get_update_log, create_purchase_tariff, update_purchase_status, get_subscribe
from core.constants import MANAGER, GROUP_ID
from aiogram.types import FSInputFile

async def hello_message(callback: CallbackQuery, bot: Bot):
    try:
        await callback.message.delete()
        await bot.answer_callback_query(callback.id)
    except AttributeError:
        ...
    await bot.send_message(
        callback.from_user.id,
        'Привет!\n\n'
        'Я бот по поиску букмекерских вилок. С моей помощью ты можешь найти вилки для отыгрыша баланса и твоих фрибетов.\n\n', 
        reply_markup=keyboards.hello_keyboard()
        )


async def feedback(callback: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    await bot.send_message(
        callback.from_user.id,
        'Вы перешли на вкладку *Обратная связь*\n\n'
        'Здесь вы можете обратиться за помощью в тех.поддержку или поделиться своей идеей для усовершенствования бота\n\n'
        'Выберите действие:',
        reply_markup=keyboards.feedback_keyboard(),
        parse_mode='Markdown'
    )

async def payments(callback: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    await bot.send_message(
        callback.from_user.id,
        'Вы перешли на вкладку *Настройка подписки\n\n*'
        'Здесь ты можешь посмотреть информацию о своей актуальной подписке, просмотреть существующие тарифы и историю своих платежей\n\n'
        'Для новых пользователей доступен пробный период, чтобы его активировать перейди по кнопке тарифы\n\n'
        'Выбери действие:',
        parse_mode='Markdown',
        reply_markup=keyboards.payments_keyboard()

    )

async def tariffs_list(callback: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    tariffs = get_tariffs()
    await bot.send_message(
        callback.from_user.id,
        'При выборе тарифа отправится сообщение с подробной информацией о конкретном тарифе\n\n'
        'Список доступных тарифов:',
        reply_markup=keyboards.tariffs_keyboard(tariffs)
    )

async def retrieve_tariff(callback: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    tariff = get_tariff(callback.data.split('_')[-2])
    cost_string = f'{tariff['cost']} руб. / {tariff['duration']} дней' if tariff['duration'] > 5 else f'{tariff['cost']} / {tariff['duration']} дня'
    await bot.send_message(
        callback.from_user.id,
        f'Тариф {callback.data.split('_')[-1]}\n\n'
        f'{tariff['description']}\n\n'
        f'*{cost_string}*',
        reply_markup=keyboards.tariff_keyboard(int(callback.data.split('_')[-2])),
        parse_mode="Markdown"
    )

async def tech_support(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    await bot.send_message(
        callback.from_user.id,
        'Пожалуйста, опишите свою проблему',
        reply_markup=keyboards.cancel_keyboard()
    )
    await state.set_state(TechSupportState.GET_TEXT)

async def create_tech_support_report(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    await bot.send_message(
        message.from_user.id,
        'Ваше обращение передано в тех.поддержку, в скором времени с вами свяжутся через телеграмм, приносим извинения за неудобства',
        reply_markup=keyboards.cancel_keyboard()
        )
    create_tech_support_ticket(message.text, message.from_user.id)
    await bot.send_message(
        MANAGER,
        f'Новое обращение в техническую поддержку!\n\n'
        f'Пользователь @{message.from_user.username}\n\n'
        f'{message.text}'
    )

async def update_ticket(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    await bot.send_message(
        callback.from_user.id,
        'Опишите своё предложение',
        reply_markup=keyboards.cancel_keyboard()
    )
    await state.set_state(UpdateTicketState.GET_TICKET_TEXT)

async def create_update_ticket(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    create_update_support_ticket(message.text,message.from_user.id)
    await bot.send_message(
        message.from_user.id,
        'Ваше предложение принято на заметку, спасибо за участие в развитии проекта!',
        reply_markup=keyboards.cancel_keyboard()
        )

async def retrieve_subcription(callback: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    subscribe = get_subscribe(callback.from_user.id)
    await bot.send_message(
        callback.from_user.id,
        f'Текущий тарифный план: {subscribe['tariff']}\n\n'
        f'Осталось дней до конца подписки: {subscribe['remained_days']}\n\n'
        f'Стоимость тарифа: {subscribe['cost']}',
        reply_markup=keyboards.back_to_payment_keyboard()
    )

async def update_log(callback: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    data = get_update_log()
    await bot.send_message(
        callback.from_user.id,
        f'Обновление от {data['created_at']}\n\n'
        f'{data['text']}',
        reply_markup=keyboards.cancel_keyboard()
    )

async def public_offer(callback: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    await bot.send_document(
            callback.from_user.id,
            FSInputFile('files/public_offer.pdf'),
            reply_markup=keyboards.cancel_keyboard()
        )

async def create_purchase_request(callback: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    payment_id = create_purchase_tariff(tariff=callback.data.split('_')[-1],tg_id=callback.from_user.id)
    match payment_id:
        case False:
            await bot.send_message(
                callback.from_user.id,
                'У вас есть действующая подписка или вы уже оставили действующий запрос на покупку тарифного плана, во втором случае в скором времени с вами свяжется администратор',
                reply_markup=keyboards.cancel_keyboard()
            )
        case _:
            tariff = get_tariff(callback.data.split('_')[-1])
            await bot.send_message(
                callback.from_user.id,
                f'Ваша заявка на покупку тарифа {tariff['title']} принята в обработку, для оплаты с вами свяжется администратор. Спасибо, что выбрали наш сервис!',
                reply_markup=keyboards.cancel_keyboard()
            )
            await bot.send_message(
                GROUP_ID,
                f'Пользователь @{callback.from_user.username} оставил заявку на преобретение тарифа {tariff['title']}',
                message_thread_id=2,
                reply_markup=keyboards.purchase_request_keyboard(payment_id=payment_id)
            )

async def update_purchase_request(callback: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    action = callback.data.split('_')[-2]
    update_purchase_status(payment_id=callback.data.split('_')[-1], action=action)
    match callback.data.split('_')[-2]:
        case 'cancel':
            await bot.send_message(
                GROUP_ID,
                f'Заявка №{callback.data.split('_')[-1]} была отклонена',
                message_thread_id=29
            )
            tariffs = get_tariffs()
            await bot.send_message(
                callback.from_user.id,
                f'По некоторым причинам ваша заявка на преобретение тарифа отклонена, создайте новую подписку или обратитесь в техническую поддержку.',
                keyboards.tariffs_keyboard(tariffs=tariffs)
            )
        case 'accept':
            await bot.send_message(
                GROUP_ID,
                f'Заявка №{callback.data.split('_')[-1]} была успешно принята',
                message_thread_id=4
            )
            await bot.send_message(
                callback.from_user.id,
                f'Благодарим вас за покупку! Вам выдан доступ к боту в соответствии с вашим тарифным планом',
                reply_markup=keyboards.hello_keyboard()
            )
            
async def activate_trial_period(callback: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    



