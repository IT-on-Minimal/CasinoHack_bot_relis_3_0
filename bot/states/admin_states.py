from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    awaiting_add_id = State()
    awaiting_remove_id = State()
