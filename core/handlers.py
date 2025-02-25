from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from utils import keyboards
from utils.parser import parse_fork
from core.constants import DEFAULT_LINK
from aiogram.fsm.context import FSMContext
from utils.states import CalculateMoneyForkState

async def hello_message(callback: CallbackQuery, bot: Bot):
    await bot.send_message(callback.from_user.id,'Здарова заебал', reply_markup=keyboards.hello_keyboard())

async def all_forks(callback: CallbackQuery, bot: Bot, state: FSMContext):
    forks = parse_fork(link=DEFAULT_LINK)
    fork = forks[0]
    responce = (f'Событие: {fork['event']}\n\n'  
               f'Вид спорта: {fork['sport']}\n\n' 
               f'Лига/Чемпионат: {fork['championship']}\n\n'
               f'Дата начала события: {fork['start_date']}\n\n'
               f'Возраст вилки: {fork['lifetime']}\n\n'
               f'Прибыль: {fork['profit']}\n\n'
               f'Букмекеры: {fork['first_booker']} - {fork['second_booker']} \n\n'
               f'Ставка на первом букмекере: {fork['bet_on_first_booker']} коэффицент - {fork['coef_on_first_booker']}\n\n'
               f'Ставка на втором букмекере: {fork['bet_on_second_booker']} коэффицент - {fork['coef_on_second_booker']}')
    await bot.send_message(
        callback.from_user.id, 
        responce, 
        reply_markup=keyboards.money_fork_keyboard(
        first_booker=fork['first_booker'],
        first_coef=float(fork['coef_on_first_booker']),
        second_booker=fork['second_booker'],
        second_coef=float(fork['coef_on_second_booker']),
        profit=float(fork['profit'].split('%')[0])
        ))

async def pre_calculate_fork(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.answer('Введите сумму вилки')
    await state.set_state(CalculateMoneyForkState.GET_AMOUNT)
    data = callback.data.split('_')
    await state.update_data(
        first_booker=data[3],
        first_coef=data[4],
        second_booker=data[5],
        second_coef=data[6],
        profit=data[7]
    )

async def calculate_fork(message: Message, bot: Bot, state: FSMContext):
    context = await state.get_data()
    amount = message.text
    chance = 1/float(context['first_coef'])+1/float(context['second_coef'])
    try:
        amount = int(amount)
    except Exception:
        await message.answer('Введите только целочисленное значение')
        return
    bet_on_the_first_booker = (1/float(context['first_coef'])/chance) * amount 
    bet_on_the_second_booker = (1/float(context['second_coef'])/chance) * amount
    profit=amount/100*float(context['profit'])
    await message.answer(
        f'Сумма ставки на {context['first_booker']}: {round(bet_on_the_first_booker)}\n\n'
        f'Сумма ставки на {context['second_booker']}: {round(bet_on_the_second_booker)}\n\n'
        f'Гарантированный доход: {round(profit,2)} руб.',
        reply_markup=keyboards.money_fork_calculating_keyboard(context['first_booker'],context['first_coef'],context['second_booker'],context['second_coef'],context['profit'])
    )
    await state.clear()