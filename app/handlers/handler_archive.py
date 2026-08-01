from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from app.utils.dinamic_keyboard import DinamicKeyboard
from app.utils.utils_download_photos import DB_DownloadPhoto

from config import PATH_TO_DB_PHOTO

router_archive = Router()

@router_archive.callback_query(F.data == "arcive")
async def archive_start(callback: CallbackQuery, state: FSMContext):
    await state.update_data(first_index=0)
    await callback.answer()
    db = DB_DownloadPhoto(PATH_TO_DB_PHOTO)
    await db.get_download_photo_where_user_id(callback.from_user.id)
    if db.groups_where_user_id == []:
        await callback.message.answer("Ваш архив пуст")
    else:
        await callback.message.answer_photo(photo=f"{db.groups_where_user_id[0]['file_id']}" ,caption='Ваши фото :З', reply_markup=await DinamicKeyboard(1,3,'no',0,f"archive_{callback.from_user.id}").generate_keyboard())
        await db.close()