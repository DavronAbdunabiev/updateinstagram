from aiogram.dispatcher.filters.state import State,StatesGroup


class ReklamaState(StatesGroup):
    add_image = State()
    add_text = State()
    add_check = State()
