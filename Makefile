# Игнорируем файлы с такими же именами, как команды
.PHONY: help install reload start stop logs status clean db-clean

# Команда по умолчанию, если написать просто "make"
.DEFAULT_GOAL := help

help:
	@echo "Доступные команды:"
	@echo "  make install   - 🚀 Первичная установка (запуск install.sh)"
	@echo "  make reload    - 🔄 Пересборка и перезапуск контейнеров (с применением новых изменений в коде)"
	@echo "  make start     - ▶️ Запуск остановленных контейнеров"
	@echo "  make stop      - ⏹️ Остановка контейнеров"
	@echo "  make logs      - 📋 Просмотр логов в реальном времени (Ctrl+C для выхода)"
	@echo "  make status    - 📊 Проверка статуса контейнеров"
	@echo "  make clean     - 🧹 Удаление контейнеров бота и связанных сетей"
	@echo "  make db-clean  - ⚠️ ВНИМАНИЕ: Удаление файлов баз данных (.db)!"

install:
	@chmod +x install.sh
	@bash install.sh

reload:
	@echo "🔄 Перезапуск и пересборка контейнеров..."
	docker compose down
	docker compose up -d --build
	@echo "✅ Бот успешно перезапущен!"

start:
	@echo "▶️ Запуск бота..."
	docker compose up -d

stop:
	@echo "⏹️ Остановка бота..."
	docker compose down

logs:
	@echo "📋 Вывод логов..."
	docker compose logs -f

status:
	@echo "📊 Статус контейнеров:"
	docker compose ps

clean:
	@echo "🧹 Удаление контейнеров..."
	docker compose down --remove-orphans

db-clean:
	@echo "⚠️ Удаление баз данных..."
	rm -f ./app/db/*.db
	@echo "✅ Базы данных удалены. При следующем 'make install' они будут созданы заново."