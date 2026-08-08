import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from app.keyboards.keyboard_groups import keyboard_groups_start, keyboard_groups_choice
from app.keyboards.keyboard_my_photos import keyboard_my_photos_first_choice
from app.utils.dinamic_keyboard import DinamicKeyboard
from app.utils.utils_group import DB_Group
from config import PATH_TO_DB_DATA

router_groups = Router()

@router_groups.message(F.text == "Группы")
async def groups_start(message: Message, state: FSMContext):
    await state.clear()

    db = DB_Group(PATH_TO_DB_DATA)
    group = await db.get_groups()
    if group != []:
        await message.answer('Выберите группу для настройки: ', reply_markup= await DinamicKeyboard(1, 3, 'no', 0, f'groupssetting_{message.from_user.id}').generate_keyboard())
    elif group == []:
        await message.answer(text="Нет подключенных групп, добавьте бота в группу", reply_markup=keyboard_my_photos_first_choice.markup)


@router_groups.callback_query(F.data[:27] == 'callback_data_groupssetting')
async def groups_groupssetting(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    db = DB_Group(PATH_TO_DB_DATA)
    groups = [
        {
            'id': x['id'],
            'type': x['type'],
            'status': x['status'],
            'full_name': x['full_name'],
            'on_off': x['on_off']
        }
        for x in await db.get_groups()
        if x['id'] == int(callback.data.split(' ')[1].split('_')[1])
    ]
    group = groups[0]
    await state.update_data(groupsettingid=group['id'])

    logging.info(group)

    await callback.message.edit_text(inline_message_id=callback.inline_message_id, text=f"Группа '{group['full_name']}'\nТип группы: {group['type']}\nId группы: {group['id']}\nСтатус бота в группе: {group['status']}")
    try:
        if group['on_off'] == '1':
            db.update_group(group['id'], group['type'], group['status'], group['full_name'], group['on_off'])
            keyboard_groups_choice.update_button('✅Включено', '❌Выключено')
        elif group['on_off'] == '0':
            db.update_group(group['id'], group['type'], group['status'], group['full_name'], group['on_off'])
            keyboard_groups_choice.update_button('❌Выключено', '✅Включено')
    except Exception as e:
        pass
    await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id, reply_markup=keyboard_groups_choice.markup)

@router_groups.callback_query(F.data[:12] == 'groupsstatus')
async def groups_groupssetting(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = (await state.get_data())['groupsettingid']
    db = DB_Group(PATH_TO_DB_DATA)
    group = [
        {
            'id': x['id'],
            'type': x['type'],
            'status': x['status'],
            'full_name': x['full_name'],
            'on_off': x['on_off']
        }
        for x in await db.get_groups()
        if x['id'] == data
    ]
    
    if group['on_off'] == '1':
        db.update_group(group['id'], group['type'], group['status'], group['full_name'], group['on_off'])
        keyboard_groups_choice.update_button('✅Включено', '❌Выключено')
    elif group['on_off'] == '0':
        db.update_group(group['id'], group['type'], group['status'], group['full_name'], group['on_off'])
        keyboard_groups_choice.update_button('❌Выключено', '✅Включено')
    try:
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id, reply_markup=keyboard_groups_choice.markup)
    except Exception as e:
        pass
