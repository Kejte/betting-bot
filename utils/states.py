from aiogram.fsm.state import StatesGroup, State

class CalculateMoneyForkState(StatesGroup):
    GET_AMOUNT=State()