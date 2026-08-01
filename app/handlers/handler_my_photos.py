from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from app.keyboards.keyboard_my_photos import keyboard_my_photos_first_choice, keyboard_my_photos_new_photos, keyboard_my_photos_is_sending
from app.utils.dinamic_keyboard import DinamicKeyboard

class DownloadPhotos(StatesGroup):
    wait = State()
    successfuly = State()

router_my_photos = Router()

@router_my_photos.message(F.text == "Мои фоточки")
async def my_photos_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Скинешь ножки?):", reply_markup=keyboard_my_photos_first_choice.markup)

@router_my_photos.callback_query(F.data == "new_photos")
async def my_photos_new_photos(callback: CallbackQuery, state: FSMContext):
    await state.set_state(DownloadPhotos.wait)
    await callback.answer()
    await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup=keyboard_my_photos_new_photos.markup)
    await state.update_data(count=0)
    await state.update_data(message_id=callback.message.message_id)
    await state.update_data(chat_id=callback.message.chat.id)


@router_my_photos.callback_query(F.data == "finish_sending")
async def my_photos_finish_sending(callback: CallbackQuery, state: FSMContext):
    count = (await state.get_data())['count']
    if count > 0:
        await state.set_state(DownloadPhotos.successfuly)
        await callback.answer()
        await callback.message.answer('Хотите ли вы сохранить фото в архив, или хотите опубликовать?', reply_markup=keyboard_my_photos_is_sending.markup)
    else:
        await callback.answer()
        await callback.message.edit_text(inline_message_id=callback.inline_message_id, text="Выберите хотя бы одно фото", reply_markup=keyboard_my_photos_new_photos.markup)

@router_my_photos.callback_query(F.data == "back_my_photos_first_choice")
async def my_photos_back_my_photos_first_choice(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id, reply_markup=keyboard_my_photos_first_choice.markup)

@router_my_photos.callback_query(F.data == "saving_in_archive")
async def my_photos_saving_in_archive(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(inline_message_id=callback.inline_message_id, text='Выберите счастливчиков: ')
    await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup= await DinamicKeyboard(1, 3, 'no', 0, f'groups_{callback.message.from_user.id}').generate_keyboard())