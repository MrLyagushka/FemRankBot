import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN=os.getenv("BOT_TOKEN")
ADMIN_ID=list(map(int,(os.getenv("ADMIN_ID")).split(',')))
PATH_TO_DB_DATA=os.getenv("PATH_TO_DB_DATA")
PATH_TO_DB_PHOTO=os.getenv("PATH_TO_DB_PHOTO")
COLUMN_ARCHIVE=int(os.getenv("COLUMN_ARCHIVE"))
ROW_ARCHIVE=int(os.getenv("ROW_ARCHIVE"))

if not BOT_TOKEN:
    print("Ошибка запуска, не указан BOT_TOKEN")