from aiogram.dispatcher.filters.state import StatesGroup, State

class reg_user(StatesGroup):
    text = State()
    state = State()
    url = State()