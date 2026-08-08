from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from app.keyboards.keyboard_rating import keyboard_rating_first_choice, keyboard_rating_cute_punped_up_femboys, keyboard_rating_cute_femboys, keyboard_rating_cute_femboys_legs, keyboard_rating_cute_femboys_other_beauty, keyboard_rating_cute_femboys_skirts

router_rating = Router()

@router_rating.message(F.text == "Рейтинг")
async def rating_start(message: Message, state: FSMContext):
    await state.clear()

    await message.answer("Выбери сторону:", reply_markup=keyboard_rating_first_choice.markup)

@router_rating.callback_query(F.data == "cute_femboys")
async def rating_cute_femboys(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup=keyboard_rating_cute_femboys.markup)

@router_rating.callback_query(F.data[:17] == "cute_femboys_legs")
async def rating_cute_femboys(callback: CallbackQuery, state: FSMContext):
    data = callback.data
    if data == "cute_femboys_legs":
        await callback.answer()
        await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup=keyboard_rating_cute_femboys_legs.markup)
    elif data == "cute_femboys_legs_week":
        await callback.answer()
        keyboard_rating_cute_femboys_legs.update_button('Недельный рейтинг', "В разработке")
        await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup=keyboard_rating_cute_femboys_legs.markup)
        keyboard_rating_cute_femboys_legs.update_button("В разработке", 'Недельный рейтинг')
    elif data == "cute_femboys_legs_month":
        await callback.answer()
        keyboard_rating_cute_femboys_legs.update_button('Месячный рейтинг', "В разработке")
        await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup=keyboard_rating_cute_femboys_legs.markup)
        keyboard_rating_cute_femboys_legs.update_button("В разработке", 'Месячный рейтинг')
    elif data == "cute_femboys_legs_back":
        await callback.answer()
        await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup=keyboard_rating_cute_femboys.markup)
        

@router_rating.callback_query(F.data[:19] == "cute_femboys_skirts")
async def rating_cute_femboys(callback: CallbackQuery, state: FSMContext):
    data = callback.data
    if data == "cute_femboys_skirts":
        await callback.answer()
        await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup=keyboard_rating_cute_femboys_skirts.markup)
    elif data == "cute_femboys_skirts_week":
        await callback.answer()
        keyboard_rating_cute_femboys_skirts.update_button('Недельный рейтинг', "В разработке")
        await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup=keyboard_rating_cute_femboys_skirts.markup)
        keyboard_rating_cute_femboys_skirts.update_button("В разработке", 'Недельный рейтинг')
    elif data == "cute_femboys_skirts_month":
        await callback.answer()
        keyboard_rating_cute_femboys_skirts.update_button('Месячный рейтинг', "В разработке")
        await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup=keyboard_rating_cute_femboys_skirts.markup)
        keyboard_rating_cute_femboys_skirts.update_button("В разработке", 'Месячный рейтинг')
    elif data == "cute_femboys_skirts_back":
        await callback.answer()
        await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup=keyboard_rating_cute_femboys.markup)

@router_rating.callback_query(F.data[:25] == "cute_femboys_other_beauty")
async def rating_cute_femboys(callback: CallbackQuery, state: FSMContext):
    data = callback.data
    if data == "cute_femboys_other_beauty":
        await callback.answer()
        await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup=keyboard_rating_cute_femboys_other_beauty.markup)
    elif data == "cute_femboys_other_beauty_week":
        await callback.answer()
        keyboard_rating_cute_femboys_other_beauty.update_button('Недельный рейтинг', "В разработке")
        await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup=keyboard_rating_cute_femboys_other_beauty.markup)
        keyboard_rating_cute_femboys_other_beauty.update_button("В разработке", 'Недельный рейтинг')
    elif data == "cute_femboys_other_beauty_month":
        await callback.answer()
        keyboard_rating_cute_femboys_other_beauty.update_button('Месячный рейтинг', "В разработке")
        await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup=keyboard_rating_cute_femboys_other_beauty.markup)
        keyboard_rating_cute_femboys_other_beauty.update_button("В разработке", 'Месячный рейтинг')
    elif data == "cute_femboys_other_beauty_back":
        await callback.answer()
        await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup=keyboard_rating_cute_femboys.markup)
