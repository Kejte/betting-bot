from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.constants import BOOKERS_LIST

def hello_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text='Найти денежную вилку', callback_data='search_money_fork')
    builder.button(text='Найти фрибетную вилку', callback_data='search_freebet_fork')
    builder.button(text='Настройки подписки', callback_data='payments')
    builder.button(text='Обратная связь', callback_data='feedback')
    
    builder.adjust(1)

    return builder.as_markup()

def bookers_list_keyboard(fork_type: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for booker in BOOKERS_LIST:
        builder.button(text=booker, callback_data=f'required_{fork_type}_{booker}')
    
    builder.button(text='Назад в меню', callback_data='main_menu')
    
    builder.adjust(1)

    return builder.as_markup()

def optional_bookers_list_keyboard(fork_type: str, first_booker: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for booker in BOOKERS_LIST:
        if booker == first_booker:
            continue
        builder.button(text=booker, callback_data=f'selected_{fork_type}_{first_booker}_{booker}')
    
    builder.button(text='Любой', callback_data=f'selected_{fork_type}_{first_booker}_any')

    builder.button(text='Изменить выбранного букмекера', callback_data=f'search_{fork_type}_fork')
    
    builder.adjust(1)

    return builder.as_markup()
    

def money_fork_keyboard(first_booker: str, first_coef: float, second_booker: str, second_coef: float, profit: float, index: int, lenght: int, bookers: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if index + 1 != lenght:
        builder.button(text='Следующая', callback_data=f'paginate_money_next_fork_{index+1}_{bookers}')
    if index != 0:
        builder.button(text='Предыдущая', callback_data=f'paginate_money_previous_fork_{index-1}_{bookers}')
    builder.button(text='Рассчитать вилку', callback_data=f'calculate_money_fork_{first_booker}_{first_coef}_{second_booker}_{second_coef}_{profit}')
    builder.button(text='Назад в меню', callback_data='main_menu')

    builder.adjust(1)

    return builder.as_markup()

def freebet_fork_keyboard(index: int, lenght: int, bookers: str, max_coeff: float, freebet: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if index + 1 != lenght:
        builder.button(text='Следующая', callback_data=f'paginate_freebet_next_fork_{max_coeff}_{int(freebet)}_{index+1}_{bookers}')
    if index != 0:
        builder.button(text='Предыдущая', callback_data=f'paginate_freebet_previous_fork_{max_coeff}_{int(freebet)}_{index-1}_{bookers}')
    builder.button(text='Назад в меню', callback_data='main_menu')

    builder.adjust(1)

    return builder.as_markup()

def money_fork_calculating_keyboard(first_booker: str, first_coef: float, second_booker: str, second_coef: float, profit: float):
    builder = InlineKeyboardBuilder()

    builder.button(text='Пересчитать',callback_data=f'calculate_money_fork_{first_booker}_{first_coef}_{second_booker}_{second_coef}_{profit}')

    builder.adjust(1)

    return builder.as_markup()

def cancel_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text='Назад в меню', callback_data='main_menu')

    builder.adjust(1)

    return builder.as_markup()

def tariffs_keyboard(tariffs: list[dict]):
    builder = InlineKeyboardBuilder()
    
    for tariff in tariffs:
        builder.button(text=tariff['title'], callback_data=f'tariff_{tariff['id']}_{tariff['title']}')
    
    builder.button(text='Назад в меню', callback_data='main_menu')
    
    builder.adjust(1)

    return builder.as_markup()

def payments_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text='Моя подпискa', callback_data='actual_subscribe')
    builder.button(text='Тарифы', callback_data='tariffs')
    builder.button(text='История платежей', callback_data='payment_history')
    builder.button(text='Назад в меню', callback_data='main_menu')

    builder.adjust(1)

    return builder.as_markup()

def tariff_keyboard(id: int):
    builder = InlineKeyboardBuilder()

    builder.button(text='Купить', callback_data='purchase_tariff')
    builder.button(text='Назад к тарифам', callback_data='tariffs')
    builder.button(text='Назад в меню', callback_data='main_menu')

    builder.adjust(1)

    return builder.as_markup()
