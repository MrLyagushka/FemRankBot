from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.utils.utils_download_photos import DB_DownloadPhoto
from app.handlers.handler_my_photos import my_photos_finish_sending, keyboard_my_photos_new_photos, DownloadPhotos
from app.utils.dinamic_keyboard import DinamicKeyboard

from config import PATH_TO_DB_PHOTO

router_download_photos = Router()



@router_download_photos.message(F.photo, DownloadPhotos.wait)
async def download_photos_start(message: Message, state: FSMContext, bot: Bot):
    message_id = (await state.get_data())['message_id']
    chat_id = (await state.get_data())['chat_id']
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    if message.media_group_id == None:
        user_id = message.from_user.id
        text = message.caption
        file_id = (message.photo)[-1].file_id
        media_group_id = 0
        db = DB_DownloadPhoto(PATH_TO_DB_PHOTO)
        await db.new_download_photo(user_id, file_id, media_group_id, text)
        await db.close()
        await state.set_state(DownloadPhotos.successfuly)
        await state.update_data(count=1)
        await message.answer('Выберите группу: ', reply_markup= await DinamicKeyboard(1, 3, 'no', 0, f'groups_{message.from_user.id}').generate_keyboard())
    else:
        await message.answer(text='Выберите: ', reply_markup=keyboard_my_photos_new_photos.markup)
        user_id = message.from_user.id
        text = message.caption
        file_id = (message.photo)[-1].file_id
        media_group_id = message.media_group_id
        count = (await state.get_data())['count']
        await state.update_data(count=count + 1)
        db = DB_DownloadPhoto(PATH_TO_DB_PHOTO)
        await db.new_download_photo(user_id, file_id, media_group_id, text)
        await db.close()
        