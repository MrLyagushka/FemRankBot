#!/bin/bash

# 🐸 Автоматический деплой Python-ботов с Docker + Compose

# Остановка при любой ошибке, использовании необъявленной переменной или ошибке в пайплайне
set -euo pipefail 

echo "✅ Начинаем развёртывание бота..."

# 1. Обновляем систему (добавлен флаг DEBIAN_FRONTEND чтобы не вылезали интерактивные окна)
echo "🔧 Обновляем систему..."
export DEBIAN_FRONTEND=noninteractive
sudo apt update && sudo apt upgrade -y

# 2. Устанавливаем зависимости
echo "📥 Устанавливаем зависимости..."
sudo apt install -y ca-certificates curl gnupg lsb-release sqlite3

# 3. Устанавливаем Docker
if ! command -v docker &> /dev/null; then
    echo "🐳 Устанавливаем Docker..."
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -yes -o /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
else
    echo "🐳 Docker уже установлен"
fi

if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose v2 не найден. Установка прервана."
    exit 1
fi

# 4. Настройка .env файла и ввод данных (Токен, Админы)
ENV_FILE="./.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "⚠️ Файл $ENV_FILE не найден. Давайте его создадим."
    
    # Запрос данных у пользователя
    read -rp "🔑 Введите токен бота (BOT_TOKEN): " BOT_TOKEN
    read -rp "🛡️  Введите ID администраторов (через запятую, например: 12345,67890): " ADMIN_IDS
    
    # Запись в файл
    cat > "$ENV_FILE" <<EOF
BOT_TOKEN=${BOT_TOKEN}
ADMIN_IDS=${ADMIN_IDS}
EOF
    # Защита файла от чтения другими пользователями (Security best practice)
    chmod 600 "$ENV_FILE"
    echo "✅ Файл .env успешно создан и защищен."
else
    echo "✅ Файл .env уже существует. Пропускаем настройку переменных."
fi

# 5. Создаём папку db и инициализируем базы данных из SQL-файлов
echo "🗃️ Создаём папку баз данных и применяем схемы..."
mkdir -p ./app/db

TASK_DB="./app/db/data.db"
USERS_DB="./app/db/photo.db"

# Инициализация data.db
if [ ! -f "$TASK_DB" ]; then
    if [ -f "./db/data.db.sql" ]; then
        echo "   → Создаём data.db из файла схемы..."
        sqlite3 "$TASK_DB" < "./db/data.db.sql"
    else
        echo "❌ Ошибка: Файл ./db/data.db.sql не найден!"
        exit 1
    fi
else
    echo "   → data.db уже существует, пропускаем."
fi

# Инициализация photo.db
if [ ! -f "$USERS_DB" ]; then
    if [ -f "./db/photo.db.sql" ]; then
        echo "   → Создаём photo.db из файла схемы..."
        sqlite3 "$USERS_DB" < "./db/photo.db.sql"
    else
        echo "❌ Ошибка: Файл ./db/photo.db.sql не найден!"
        exit 1
    fi
else
    echo "   → photo.db уже существует, пропускаем."
fi
echo "✅ Базы данных проверены."

# 6. Проверяем наличие docker-compose.yml
COMPOSE_FILE="docker-compose.yml"
if [ ! -f "$COMPOSE_FILE" ]; then
    echo "❌ Не найден файл $COMPOSE_FILE"
    exit 1
fi

# 7. Запуск контейнеров
echo "🚀 Собираем и запускаем ботов..."
# Использование sudo при необходимости без прерывания скрипта
if groups | grep -q '\bdocker\b'; then
    docker compose -f "$COMPOSE_FILE" up -d --build
else
    echo "🔁 Текущий пользователь не в группе docker. Запускаем через sudo..."
    sudo docker compose -f "$COMPOSE_FILE" up -d --build
fi

echo "✅ Развёртывание завершено! Бот работает."