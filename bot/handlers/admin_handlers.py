from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from keyboards.admin_kb import admin_menu
from states.admin_states import AdminStates
from utils.id_utils import add_id, remove_id, load_ids

router = Router()
ADMIN_IDS = [123456789]

@router.message(F.command("admin"))
async def admin_entry(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        await message.answer("Админ-панель открыта:", reply_markup=admin_menu)

@router.message(F.text.in_(["📃 Показать все ID", "➕ Добавить ID", "➖ Удалить ID"]))
async def admin_actions(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return

    text = message.text
    if text == "📃 Показать все ID":
        ids = load_ids()
        await message.answer("\n".join(ids) if ids else "Список пуст.")
    elif text == "➕ Добавить ID":
        await message.answer("Введите ID для добавления:")
        await state.set_state(AdminStates.awaiting_add_id)
    elif text == "➖ Удалить ID":
        await message.answer("Введите ID для удаления:")
        await state.set_state(AdminStates.awaiting_remove_id)

@router.message(AdminStates.awaiting_add_id)
async def process_add(message: types.Message, state: FSMContext):
    add_id(message.text.strip())
    await message.answer("✅ ID добавлен.")
    await state.clear()

@router.message(AdminStates.awaiting_remove_id)
async def process_remove(message: types.Message, state: FSMContext):
    remove_id(message.text.strip())
    await message.answer("❌ ID удалён.")
    await state.clear()
