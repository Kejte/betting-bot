from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from utils import keyboards
from utils.parser import parse_fork
from aiogram.fsm.context import FSMContext
from utils.states import CalculateMoneyForkState, FreebetDataState
import importlib
from utils.caching import cache_forks, get_cached_fork_data
from utils.funcs import generate_fork_message, sort_freebet_forks

async def hello_message(callback: Message, bot: Bot):
    await bot.send_message(callback.from_user.id,'Здарова заебал', reply_markup=keyboards.hello_keyboard())

async def required_bookers_list(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    await bot.send_message(
        callback.from_user.id, 
        'Выберите первого букмекера', 
        reply_markup=keyboards.bookers_list_keyboard(callback.data.split('_')[1]))

async def optional_bookers_list(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    await bot.send_message(
        callback.from_user.id, 
        'Выберите второго букмекера\n\n'
        f'Выбранный букмекер: {callback.data.split('_')[-1]}', 
        reply_markup=keyboards.optional_bookers_list_keyboard(callback.data.split('_')[1],callback.data.split('_')[-1]))    

async def search_fork(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    second_booker = callback.data.split('_')[-1] if callback.data.split('_')[-1] != 'any' else 'Любая бк' 
    await bot.send_message(
        callback.from_user.id,
        f'Вы выбрали {callback.data.split('_')[-2]} - {second_booker}\n\n'
        'Ищу вилку'
    )
    bookers = f'{callback.data.split('_')[-2]}_{callback.data.split('_')[-1]}'.upper()
    cache_key = bookers
    module = importlib.import_module('core.constants')
    bookers = getattr(module,bookers)
    forks = get_cached_fork_data(cache_key)
    if not forks:
        forks = parse_fork(bookers)
        cache_forks(forks, cache_key)
    fork = forks[0]
    responce = generate_fork_message(fork)
    await bot.send_message(
        callback.from_user.id, 
        responce, 
        reply_markup=keyboards.money_fork_keyboard(
        first_booker=fork['first_booker'],
        first_coef=float(fork['coef_on_first_booker']),
        second_booker=fork['second_booker'],
        second_coef=float(fork['coef_on_second_booker']),
        profit=float(fork['profit'].split('%')[0]),
        index=0,
        lenght=len(forks),
        bookers=cache_key
        ))

async def paginate_forks(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    index = int(callback.data.split('_')[-3]) 
    bookers = callback.data.split('_')[-2]+'_'+callback.data.split('_')[-1]
    forks = get_cached_fork_data(bookers)
    if not forks:
        module = importlib.import_module('core.constants')
        url = getattr(module,bookers)
        forks = parse_fork(url)
        cache_forks(forks, bookers)
    fork = forks[index]
    responce = generate_fork_message(fork)
    await bot.send_message(
        callback.from_user.id, 
        responce, 
        reply_markup=keyboards.money_fork_keyboard(
        first_booker=fork['first_booker'],
        first_coef=float(fork['coef_on_first_booker']),
        second_booker=fork['second_booker'],
        second_coef=float(fork['coef_on_second_booker']),
        profit=float(fork['profit'].split('%')[0]),
        index=index,
        lenght=len(forks),
        bookers=bookers
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

async def choice_freebet_booker(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    await bot.send_message(
        callback.from_user.id, 
        'Выберите букмекера с фрибетом', 
        reply_markup=keyboards.bookers_list_keyboard(callback.data.split('_')[1]))
    
async def get_freebet_amount(callback: CallbackQuery, bot: Bot, state: FSMContext):
    booker = callback.data.split('_')[-1].upper() + '_ANY'
    await bot.send_message(
        callback.from_user.id,
        'Введите номинал фрибета'
    )
    await state.set_state(FreebetDataState.GET_FREEBET_AMOUNT)
    await state.update_data(booker=booker)

async def get_freebet_coef(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(
        message.from_user.id,
        'Ведите ограничение по коэффиценту'
    )
    await state.update_data(amount=message.text)
    await state.set_state(FreebetDataState.GET_FREEBET_COEFF)

async def freebet_forks(message: Message, bot: Bot, state: FSMContext):
    context = await state.get_data()
    await bot.send_message(
        message.from_user.id,
        'Ищу вилку подходящую вашим параметрам\n\n'
        f'Выбранный букмекер: {context['booker']}\n\n'
        f'Номинал фрибета: {context['amount']}\n\n'
        f'Ограничение по коэффиценту: {message.text}' 
    )
    forks = sort_freebet_forks(context['booker'], float(message.text))
    fork = forks[0]
    response = generate_fork_message(fork)
    await bot.send_message(message.from_user.id, response)