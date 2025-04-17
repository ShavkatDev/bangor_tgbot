from aiogram.fsm.state import StatesGroup, State

class LoginState(StatesGroup):
    waiting_for_privacy = State()
    waiting_for_login = State()
    waiting_for_password = State()

class SupportState(StatesGroup):
    waiting_for_question = State()