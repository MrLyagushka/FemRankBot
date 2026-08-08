from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.keyboards.keyboard_start import keyboard_start_user, keyboard_start_admin
from app.utils.utils_users import DB_User

from config import ADMIN_ID, PATH_TO_DB_DATA

router_start = Router()

@router_start.message(CommandStart())
async def router_start_start(message: Message):
    if message.chat.type == 'private':
        await message.answer_photo(photo="AgACAgIAAxkBAANTam0jEiPZAaUNyQKKOd9gCt6leJwAAr4aaxv_72lLbpKSR281WukBAAMCAAN5AAM9BA")
        db = DB_User(PATH_TO_DB_DATA)
        await db.new_user(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
        await db.close()
        if message.from_user.id in ADMIN_ID:
            await message.answer("Приветики, мы уже почти закончили, остались только рейтинги фембоев)", reply_markup=keyboard_start_admin.markup)
        else:
            await message.answer("Приветики, мы уже почти закончили, остались только рейтинги фембоев)", reply_markup=keyboard_start_user.markup)

