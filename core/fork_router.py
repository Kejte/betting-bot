from utils.parser import parse_fork
from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from utils import keyboards

from aiogram.fsm.context import FSMContext
from utils.states import CalculateMoneyForkState, FreebetDataState
import importlib
from utils.caching import cache_forks, get_cached_fork_data
from utils.funcs import generate_fork_message, get_freebet_forks, generate_freebet_fork_message, get_user_permission 
from aiogram import Router, F

router = Router()

@router.callback_query(F.data.startswith('search_money'))
async def required_bookers_list(callback: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    await bot.send_message(
        callback.from_user.id, 
        'Выберите первого букмекера', 
        reply_markup=keyboards.bookers_list_keyboard(callback.data.split('_')[1]))

@router.callback_query(F.data.startswith('required_money'))
async def optional_bookers_list(callback: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    await bot.send_message(
        callback.from_user.id, 
        'Выберите второго букмекера\n\n'
        f'Выбранный букмекер: {callback.data.split('_')[-1]}', 
        reply_markup=keyboards.optional_bookers_list_keyboard(callback.data.split('_')[1],callback.data.split('_')[-1]))    

@router.callback_query(F.data.startswith('selected_money'))
async def search_fork(callback: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    second_booker = callback.data.split('_')[-1] if callback.data.split('_')[-1] != 'any' else 'Любая бк' 
    await bot.send_message(
        callback.from_user.id,
        f'Вы выбрали {callback.data.split('_')[-2]} - {second_booker}\n\n'
        'Ищу вилку'
    )
    bookers = f'{callback.data.split('_')[-2]}_{callback.data.split('_')[-1]}'.upper()
    permission = get_user_permission(callback.from_user.id)
    cache_key =  permission + '_'+ bookers
    module = importlib.import_module('core.constants')
    bookers = getattr(module,bookers)
    forks = get_cached_fork_data(cache_key)
    if not forks:
        print(permission)
        forks = parse_fork(bookers, permission=permission)
        cache_forks(forks, cache_key)
    try:
        fork = forks[0]
    except IndexError:
        await bot.send_message(callback.from_user.id,'К сожалению в данный момент по данным критериям нет доступных вилок')
        return
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

@router.callback_query(F.data.startswith('paginate_money'))
async def paginate_forks(callback: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    index = int(callback.data.split('_')[-4]) 
    permission = get_user_permission(callback.from_user.id)
    bookers = permission+'_'+callback.data.split('_')[-2]+'_'+callback.data.split('_')[-1]
    forks = get_cached_fork_data(permission + "_"+bookers)
    if not forks:
        module = importlib.import_module('core.constants')
        url = getattr(module,f'{bookers.split('_')[1]}_{bookers.split('_')[2]}')
        forks = parse_fork(link=url, permission=permission)
        cache_forks(forks, permission + "_"+bookers)
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
    
@router.callback_query(F.data.startswith('calculate_money_fork'))
async def pre_calculate_fork(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.answer_callback_query(callback.id)
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

@router.message(CalculateMoneyForkState.GET_AMOUNT)
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

@router.callback_query(F.data.startswith('search_freebet'))
async def choice_freebet_booker(callback: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    await bot.send_message(
        callback.from_user.id, 
        'Выберите букмекера с фрибетом', 
        reply_markup=keyboards.bookers_list_keyboard(callback.data.split('_')[1]))

@router.callback_query(F.data.startswith('required_freebet'))   
async def get_freebet_amount(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.answer_callback_query(callback.id)
    booker = callback.data.split('_')[-1].upper() + '_ANY'
    await state.set_state(FreebetDataState.GET_FREEBET_AMOUNT)
    await bot.send_message(
        callback.from_user.id,
        'Введите номинал фрибета',
        reply_markup=keyboards.cancel_keyboard()
    )
    await state.update_data(booker=booker)

@router.message(FreebetDataState.GET_FREEBET_AMOUNT)
async def get_freebet_coef(message: Message, bot: Bot, state: FSMContext):
    try:
        await state.update_data(amount=int(message.text))
        await state.set_state(FreebetDataState.GET_FREEBET_COEFF)
        await bot.send_message(
            message.from_user.id,
            'Введите ограничение по коэффиценту, если фрибет без ограничений, то напишите нет',
            reply_markup=keyboards.cancel_keyboard()
        )
    except Exception:
        await bot.send_message(message.from_user.id,'Введите целочисленное значение')

@router.message(FreebetDataState.GET_FREEBET_COEFF)
async def freebet_forks(message: Message, bot: Bot, state: FSMContext):
    try:
        context = await state.get_data()
        max_coeff = float(message.text) if message.text.lower() != 'нет' else 10
        await bot.send_message(
            message.from_user.id,
            'Ищу вилку подходящую вашим параметрам\n\n'
            f'Выбранный букмекер: {context['booker'][0] + context["booker"].split('_')[0][1:].lower()}\n\n'
            f'Номинал фрибета: {context['amount']}\n\n'
            f'Ограничение по коэффиценту: {max_coeff}' 
        )
        permission = get_user_permission(message.from_user.id)
        forks = get_freebet_forks(context['booker'], float(max_coeff), int(context['amount']), permission)
        fork = forks[0]
        response = generate_freebet_fork_message(fork, int(context['amount']), context['booker'])
        await state.clear()
        await bot.send_message(message.from_user.id, response, reply_markup=keyboards.freebet_fork_keyboard(index=0,lenght=len(forks),bookers=context['booker'],freebet=int(context['amount']),max_coeff=float(max_coeff)))
    except IndexError:
        await bot.send_message(message.from_user.id,'К сожалению в данный момент по данным критериям нет доступных вилок')
    # except Exception as e:
    #     print(e)
    #     await bot.send_message(message.from_user.id,'Введите целочисленное значение или дробное через точку, если ограничений нет, то напишите слово нет')

@router.callback_query(F.data.startswith('paginate_freebet'))
async def paginate_freebet_forks(callback: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    index = int(callback.data.split('_')[-3]) 
    bookers = callback.data.split('_')[-2]+'_'+callback.data.split('_')[-1]
    permission = get_user_permission(callback.from_user.id)
    forks = get_freebet_forks(bookers,float(callback.data.split('_')[-5]),int(callback.data.split('_')[-4]), permission)
    fork = forks[index]
    responce = generate_freebet_fork_message(fork,freebet=int(callback.data.split('_')[-4]),booker=bookers)
    await bot.send_message(
        callback.from_user.id, 
        responce, 
        reply_markup=keyboards.freebet_fork_keyboard(
        index=index,
        lenght=len(forks),
        bookers=bookers,
        max_coeff=float(callback.data.split('_')[-5]),
        freebet=int(callback.data.split('_')[-4])
        ))