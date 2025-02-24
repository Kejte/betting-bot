from aiogram.fsm.state import StatesGroup, State

class ForkActionState(StatesGroup):
    WAITING_ACTION=State()
    Calculating=State()