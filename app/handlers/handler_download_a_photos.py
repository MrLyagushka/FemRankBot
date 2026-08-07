from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio

from app.utils.utils_download_photos import DB_DownloadPhoto
from app.handlers.handler_my_photos import my_photos_finish_sending, keyboard_my_photos_new_photos, keyboard_my_photos_first_choice, DownloadPhotos
from app.utils.dinamic_keyboard import DinamicKeyboard, RatingKeyboard

from app.utils.utils_group import DB_Group
from config import PATH_TO_DB_DATA, PATH_TO_DB_PHOTO

router_download_photos = Router()

is_avalible = True

async def delete_(bot, chat_id, message_id, message, time):
    global is_avalible
    if not is_avalible:
        return
    is_avalible = False
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    await asyncio.sleep(1)
    await message.answer(text='Докинешь еще сладких ножек:З ', reply_markup=keyboard_my_photos_new_photos.markup)
    is_avalible = True

@router_download_photos.message(F.photo, DownloadPhotos.wait)
async def download_photos_start(message: Message, state: FSMContext, bot: Bot):
    message_id = (await state.get_data())['message_id']
    chat_id = (await state.get_data())['chat_id']
    if message.media_group_id == None:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        user_id = message.from_user.id
        text = message.caption
        file_id = (message.photo)[-1].file_id
        media_group_id = 0
        db = DB_DownloadPhoto(PATH_TO_DB_PHOTO)
        primary_key = await db.new_download_photo(user_id, file_id, media_group_id, text)
        if primary_key == -999999999:
            await message.answer("Это фото уже есть в вашем архиве, пришлите другое", reply_markup=keyboard_my_photos_first_choice.markup)
        else:
            await state.update_data(count=1)
            await state.update_data(file_id=file_id)
            await state.update_data(id=primary_key)
            await db.close()
            await state.set_state(DownloadPhotos.successfuly)
            db = DB_Group(PATH_TO_DB_DATA)
            group = await db.get_groups()
            if group != []:
                await message.answer('Выберите счастливчиков: ', reply_markup= await DinamicKeyboard(1, 3, 'no', 0, f'groups_{message.from_user.id}').generate_keyboard())
            elif group == []:
                await message.answer(text="Нет подключенных групп, обратитесь к админу @cute_femboychik_3", reply_markup=keyboard_my_photos_first_choice.markup)
    else:
        asyncio.create_task(delete_(bot, chat_id, message_id, message, 2))
        user_id = message.from_user.id
        text = message.caption
        file_id = (message.photo)[-1].file_id
        media_group_id = message.media_group_id
        await state.update_data(media_group_id=media_group_id)
        count = (await state.get_data())['count']
        print(count)
        await state.update_data(count=count + 1)
        db = DB_DownloadPhoto(PATH_TO_DB_PHOTO)
        await db.new_download_photo(user_id, file_id, media_group_id, text)
        await db.close()

@router_download_photos.callback_query(F.data[:21] == "callback_data_groups_")
async def my_photos_callback_data_groups(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    group_id = callback.data.split('_')[4]
    count = (await state.get_data())['count']
    if count == 1:
        primary_key = (await state.get_data())['id']
        db = DB_DownloadPhoto(PATH_TO_DB_PHOTO)
        groups_where_id = await db.get_download_photo_where_id(primary_key)
        file_id = groups_where_id['file_id']
        await bot.send_photo(chat_id=group_id, photo=file_id, reply_markup=await RatingKeyboard(primary_key).generate_keyboard())
        try:
            await callback.message.edit_text(inline_message_id=callback.inline_message_id, text="Фото успешно отправлено")
            await callback.message.delete_reply_markup(inline_message_id=callback.inline_message_id)
        except Exception as e:
            try:
                await callback.message.edit_caption(inline_message_id=callback.inline_message_id, caption="Фото успешно отправлено")
                await callback.message.delete_reply_markup(inline_message_id=callback.inline_message_id)
            except Exception as e:
                pass
    elif count > 1:
        media_group_id = (await state.get_data())['media_group_id']
        db = DB_DownloadPhoto(PATH_TO_DB_PHOTO)
        groups = await db.get_download_photo()
        datas = [[x['id'],x['file_id']] for x in groups if x['media_group_id'] == int(media_group_id)]
        for data in datas:
            await bot.send_photo(chat_id=group_id, photo=f"{data[1]}", reply_markup=await RatingKeyboard(data[0]).generate_keyboard())
        await db.close()
        await callback.message.edit_text(inline_message_id=callback.inline_message_id, text="Фото успешно отправлено")
        await callback.message.delete_reply_markup(inline_message_id=callback.inline_message_id)
    else:
        print("Ошибка, я хз вообще как это может случиться handler_download_a_photos")