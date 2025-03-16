from aiogram.fsm.state import StatesGroup, State

class CalculateMoneyForkState(StatesGroup):
    GET_AMOUNT=State()

class FreebetDataState(StatesGroup):
    GET_FREEBET_AMOUNT=State()
    GET_FREEBET_COEFF=State()

class TechSupportState(StatesGroup):
    GET_TEXT=State()

class UpdateTicketState(StatesGroup):
    GET_TICKET_TEXT=State()