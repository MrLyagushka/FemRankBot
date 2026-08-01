from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message, InputMediaPhoto
import logging
from aiogram.fsm.context import FSMContext
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.utils.dinamic_keyboard import DinamicKeyboard, MyCallbackData, RatingKeyboard
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
    try:
        tick_index = (await state.get_data())['tick_index']
    except KeyError:
        tick_index=0
    if first_index != callback_data.first_index:
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,
                                             reply_markup = await DinamicKeyboard(row=callback_data.row,
                                                                          column=callback_data.column,
                                                                          is_always_bigger_column_multiply_row=callback_data.is_always_bigger,
                                                                          first_index=first_index,
                                                                          button_info=callback_data.button_info, tick_index=tick_index).generate_keyboard())


@router_service_handlers.callback_query(F.data[:4] == "mark")
async def service_hadlers_mark(callback: CallbackQuery):
    await callback.answer()
    data = callback.data.split('_')
    primary_key = data[2]
    db = DB_DownloadPhoto(PATH_TO_DB_PHOTO)
    groups_where_id = await db.get_download_photo_where_id(int(primary_key))
    user_id = callback.from_user.id
    author_id = groups_where_id['user_id']
    mark = int(data[1])
    if int(user_id) != int(author_id):
        await db.new_mark(primary_key, user_id, author_id, mark)
    average_mark = await db.get_average_mark(primary_key)
    try:
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id, reply_markup=await RatingKeyboard(primary_key, average_mark=average_mark).generate_keyboard())
    except Exception as e:
        pass
    await db.close()

@router_service_handlers.callback_query(F.data[:12] == "average_mark")
async def service_hadlers_average_mark(callback: CallbackQuery):
    await callback.answer()
    data = callback.data.split('_')
    primary_key = data[2]
    flashing_light = int(data[3])
    db = DB_DownloadPhoto(PATH_TO_DB_PHOTO)
    average_mark = await db.get_average_mark(primary_key)
    await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id, reply_markup=await RatingKeyboard(primary_key, average_mark=average_mark, flashing_light=flashing_light).generate_keyboard())
    await db.close()

@router_service_handlers.callback_query(F.data[:21] == "callback_data_archive")
async def service_handlers_callback_data_archive(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    primary_key = (callback.data.split('_'))[4]
    tick_index = int((callback.data.split('_'))[3])-1
    first_index = (await state.get_data())['first_index']
    await state.update_data(tick_index=tick_index)
    db = DB_DownloadPhoto(PATH_TO_DB_PHOTO)
    groups_where_id = await db.get_download_photo_where_id(primary_key)
    await callback.message.edit_media(inline_message_id=callback.inline_message_id,media=InputMediaPhoto(media=f"{groups_where_id['file_id']}"), reply_markup=await DinamicKeyboard(ROW_ARCHIVE,COLUMN_ARCHIVE,'no',first_index,f"archive_{callback.from_user.id}", tick_index).generate_keyboard())
    await db.close()

@router_service_handlers.callback_query(F.data[:3] == "dk_")
async def service_handlers_dk_(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    data = callback.data.split("_")
    primary_key = data[2]
    mode = data[1]
    db = DB_DownloadPhoto(PATH_TO_DB_PHOTO)
    await state.update_data(id=primary_key)
    await state.update_data(count=1)
    groups_where_id = await db.get_download_photo_where_id(primary_key)
    if mode == "delete":
        await bot.send_photo(chat_id=-1004376588120, photo=f"{groups_where_id['file_id']}")
        await db.delete_photo(primary_key)
    elif mode == "send":
        await callback.message.edit_caption(inline_message_id=callback.inline_message_id, caption='Выберите счастливчиков: ')
        await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup= await DinamicKeyboard(1, 3, 'no', 0, f'groups_{callback.from_user.id}').generate_keyboard())
    await db.close()

