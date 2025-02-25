from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def hello_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text='Найти вилку', callback_data='search_vilka')
    
    builder.adjust(1)

    return builder.as_markup()

def money_fork_keyboard(first_booker: str, first_coef: float, second_booker: str, second_coef: float, profit: float) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text='Следующая', callback_data='next_money_fork')
    builder.button(text='Предыдущая', callback_data='previous_money_fork')
    builder.button(text='Рассчитать вилку', callback_data=f'calculate_money_fork_{first_booker}_{first_coef}_{second_booker}_{second_coef}_{profit}')
    builder.button(text='Назад в меню', callback_data='main_menu')

    builder.adjust(1)

    return builder.as_markup()

def money_fork_calculating_keyboard(first_booker: str, first_coef: float, second_booker: str, second_coef: float, profit: float):
    builder = InlineKeyboardBuilder()

    builder.button(text='Пересчитать',callback_data=f'calculate_money_fork_{first_booker}_{first_coef}_{second_booker}_{second_coef}_{profit}')

    builder.adjust(1)

    return builder.as_markup()