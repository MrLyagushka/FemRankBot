import sqlite3
import os
import glob

# Папка с базами данных (относительно корня проекта)
DB_DIR = "./app/db"

def sync_databases():
    print("🔍 Начинаем синхронизацию баз данных с шаблонами...")
    
    # Ищем все .sql файлы в папке
    sql_files = glob.glob(os.path.join(DB_DIR, "*.sql"))
    if not sql_files:
        print("⚠️ Файлы шаблонов (.sql) не найдены.")
        return

    for sql_file in sql_files:
        # Получаем имя .db файла (убираем .sql на конце)
        db_file = sql_file[:-4] 
        db_name = os.path.basename(db_file)
        print(f"\n🗃️ Проверяем базу: {db_name}")

        # 1. Создаем "идеальную" базу в оперативной памяти из вашего шаблона
        mem_conn = sqlite3.connect(":memory:")
        try:
            with open(sql_file, "r", encoding="utf-8") as f:
                mem_conn.executescript(f.read())
        except Exception as e:
            print(f"  ❌ Ошибка чтения шаблона {sql_file}: {e}")
            continue

        # 2. Подключаемся к вашей реальной базе
        real_conn = sqlite3.connect(db_file)
        real_cur = real_conn.cursor()
        mem_cur = mem_conn.cursor()

        # Получаем список таблиц из "идеальной" базы
        mem_cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in mem_cur.fetchall()]

        for table in tables:
            # Получаем структуру столбцов идеальной таблицы
            mem_cur.execute(f"PRAGMA table_info('{table}')")
            ideal_cols = mem_cur.fetchall()  # Список: (cid, name, type, notnull, dflt_value, pk)

            # Проверяем, есть ли таблица в реальной БД
            real_cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table,))
            if not real_cur.fetchone():
                # Таблицы нет вообще — берем её CREATE запрос и создаем
                mem_cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (table,))
                create_sql = mem_cur.fetchone()[0]
                real_cur.execute(create_sql)
                print(f"  ➕ Создана новая таблица '{table}'")
                continue

            # Если таблица есть, сравниваем столбцы
            real_cur.execute(f"PRAGMA table_info('{table}')")
            real_cols = [row[1] for row in real_cur.fetchall()]

            for col in ideal_cols:
                col_name, col_type = col[1], col[2]
                col_notnull, col_default = col[3], col[4]

                if col_name not in real_cols:
                    # Столбца нет — формируем запрос на добавление
                    query = f"ALTER TABLE {table} ADD COLUMN {col_name} {col_type}"
                    
                    # Если в шаблоне стоит DEFAULT, переносим и его
                    if col_default is not None:
                        query += f" DEFAULT {col_default}"
                    elif col_notnull:
                        # SQLite требует DEFAULT, если добавляется NOT NULL столбец
                        query += " DEFAULT '' NOT NULL"
                    
                    try:
                        real_cur.execute(query)
                        print(f"  ➕ В таблицу '{table}' добавлен столбец '{col_name}' ({col_type})")
                    except Exception as e:
                        print(f"  ❌ Ошибка при добавлении '{col_name}': {e}")

        real_conn.commit()
        real_conn.close()
        mem_conn.close()
    
    print("\n✅ Синхронизация успешно завершена!")

if __name__ == "__main__":
    sync_databases()