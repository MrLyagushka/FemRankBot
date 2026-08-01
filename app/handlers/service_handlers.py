from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message, InputMediaPhoto
import logging
from aiogram.fsm.context import FSMContext
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.utils.dinamic_keyboard import DinamicKeyboard, MyCallbackData
from app.utils.utils_download_photos import DB_DownloadPhoto

from config import PATH_TO_DB_PHOTO, COLUMN_ARCHIVE, ROW_ARCHIVE

router_service_handlers = Router()


@router_service_handlers.callback_query(MyCallbackData.filter())
async def on_the_what(callback: CallbackQuery, callback_data: MyCallbackData, state: FSMContext):
    await callback.answer()
    first_index = callback_data.first_index
    if callback_data.callback_data == '<':
        first_index = first_index - 1 if first_index > 0 else first_index
    elif callback_data.callback_data == '>':
        first_index = first_index + 1 if callback_data.len_button_list > first_index + callback_data.row*callback_data.column else first_index
    await state.update_data(first_index=first_index)
    if first_index != callback_data.first_index:
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,
                                             reply_markup = await DinamicKeyboard(row=callback_data.row,
                                                                          column=callback_data.column,
                                                                          is_always_bigger_column_multiply_row=callback_data.is_always_bigger,
                                                                          first_index=first_index,
                                                                          button_info=callback_data.button_info).generate_keyboard())


@router_service_handlers.callback_query(F.data[:4] == "mark")
async def service_hadlers_mark(callback: CallbackQuery):
    await callback.answer()
    data = callback.data.split('_')
    primary_key = data[2]
    db = DB_DownloadPhoto(PATH_TO_DB_PHOTO)
    await db.get_download_photo_where_id(int(primary_key))
    user_id = callback.from_user.id
    author_id = db.groups_where_id['user_id']
    mark = int(data[1])
    if int(user_id) != int(author_id):
        await db.new_mark(user_id, author_id, mark)
    await db.close()

@router_service_handlers.callback_query(F.data[:12] == "average_mark")
async def service_hadlers_average_mark(callback: CallbackQuery):
    await callback.answer()
    data = callback.data.split('_')
    primary_key = data[2]
    db = DB_DownloadPhoto(PATH_TO_DB_PHOTO)
    await db.get_average_mark(primary_key)
    print(db.average_mark)


@router_service_handlers.callback_query(F.data[:21] == "callback_data_archive")
async def service_handlers_callback_data_archive(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    primary_key = (callback.data.split('_'))[4]
    first_index = (await state.get_data())['first_index']
    db = DB_DownloadPhoto(PATH_TO_DB_PHOTO)
    await db.get_download_photo_where_id(primary_key)
    await callback.message.edit_media(inline_message_id=callback.inline_message_id,media=InputMediaPhoto(media=f"{db.groups_where_id['file_id']}"), reply_markup=await DinamicKeyboard(ROW_ARCHIVE,COLUMN_ARCHIVE,'no',first_index,f"archive_{callback.from_user.id}").generate_keyboard())
    await db.close()

    