from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from app.keyboards.keyboard_groups import keyboard_groups_start
from app.utils.dinamic_keyboard import DinamicKeyboard

router_groups = Router()

@router_groups.message(F.text == "Группы")
async def groups_start(message: Message, state: FSMContext):
    await state.clear()

    await message.answer("Выберите группу", reply_markup = await DinamicKeyboard(1, 3, 'no', 0, f'groups_{message.from_user.id}').generate_keyboard())