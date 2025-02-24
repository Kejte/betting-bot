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
    await bot.send_message(callback.from_user.id, responce)
    await state.set_state(CalculateMoneyForkState.WAITING_ACTION)
    await state.update_data(first_booker=fork['first_booker'], first_coeff=['coef_on_first_booker'], second_booker=['second_booker'], second_coef=['coef_on_second_booker'])

async def pre_calculate_fork(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.answer('Введите сумму вилки')
    await state.set_state(CalculateMoneyForkState.GET_AMOUNT)

async def calculate_fork(callback: CallbackQuery, bot: Bot, state: FSMContext):
    ...
