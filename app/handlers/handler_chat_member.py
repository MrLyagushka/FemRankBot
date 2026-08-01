import logging
from aiogram import Router, F, Bot
from aiogram.types import ChatMemberUpdated
from aiogram.enums import ChatMemberStatus

from app.utils.utils_group import DB_Group

from config import PATH_TO_DB_DATA, ADMIN_ID

router_chat_member = Router()

@router_chat_member.my_chat_member()
async def chat_member_chat_member_ship(update: ChatMemberUpdated, bot: Bot):
    try:
        chat_name = update.chat.full_name
        chat_id = update.chat.id
        chat_type = update.chat.type
        new_status = update.new_chat_member.status

        db = DB_Group(PATH_TO_DB_DATA)
        groups = await db.get_groups()
        if chat_id not in [x['id'] for x in groups]:
            await db.new_group(chat_id, chat_type, new_status, chat_name)
            for admin_id in ADMIN_ID:
                await bot.send_message(chat_id=admin_id, text=f"Бот добавлен в группу: \n{chat_name}\nТеперь статус бота: \n{new_status}")
            await bot.send_message(chat_id=chat_id, text="Всем хай! Через меня можно отсылать фоточки на оценку в группы)")
        else:
            for chat_data in groups:
                if chat_data['id'] == chat_id and chat_data['status'] != new_status:
                    await db.update_group(chat_id, chat_type, new_status, chat_name)
                    if new_status == "administrator":
                        await bot.send_message(chat_id=chat_id, text="Ыхыхыыхыхыххы, адмииинкаааа")
                    for admin_id in ADMIN_ID:
                        await bot.send_message(chat_id=admin_id, text=f"Статус бота обновлен в группе: \n{chat_name}\nТеперь статус бота: \n{new_status}")
        await db.close()
    except Exception as e:
        logging.warn(f"Ошибка в работе handler_chat_member: {e}")