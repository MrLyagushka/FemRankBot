# Игнорируем файлы с такими же именами, как команды
.PHONY: help install reload start stop logs status clean db-clean

# Команда по умолчанию (срабатывает, если написать просто "make")
.DEFAULT_GOAL := help

help: ## ℹ️ Показать эту справку со списком команд
	@echo "Доступные команды:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## 🚀 Первичная установка (запуск install.sh)
	@chmod +x install.sh
	@bash install.sh

reload: ## 🔄 Пересборка и перезапуск контейнеров (применит новый код)
	@echo "🔄 Перезапуск и пересборка контейнеров..."
	docker compose down
	docker compose up -d --build
	@echo "✅ Бот успешно перезапущен!"

start: ## ▶️ Запуск остановленных контейнеров
	@echo "▶️ Запуск бота..."
	docker compose up -d

stop: ## ⏹️ Остановка контейнеров
	@echo "⏹️ Остановка бота..."
	docker compose down

logs: ## 📋 Просмотр логов в реальном времени (Ctrl+C для выхода)
	@echo "📋 Вывод логов..."
	docker compose logs -f

status: ## 📊 Проверка статуса (работает ли бот)
	@echo "📊 Статус контейнеров:"
	docker compose ps

clean: ## 🧹 Удаление контейнеров бота и связанных сетей
	@echo "🧹 Удаление контейнеров..."
	docker compose down --remove-orphans

db-clean: ## ⚠️ ВНИМАНИЕ: Сброс и удаление файлов баз данных (.db)!
	@echo "⚠️ Удаление баз данных..."
	rm -f ./app/db/*.db
	@echo "✅ Базы данных удалены. При следующем 'make install' они будут созданы заново."

safe-reload: ## 🔄 Безопасная пересборка (с включением сообщения о техобслуживании)
	@echo "🛑 Останавливаем основного бота..."
	docker compose stop bot_dzshka
	@echo "🛠 Включаем бота-заглушку..."
	docker compose --profile maintenance up -d stub
	@echo "🏗 Собираем новую версию основного бота (это может занять время)..."
	docker compose build bot_dzshka
	@echo "⏹️ Выключаем заглушку..."
	docker compose --profile maintenance down
	@echo "🚀 Запускаем обновленного бота..."
	docker compose up -d bot_dzshka
	@echo "✅ Обновление завершено! Бот снова в строю."

update: ## Обновление с git репозетория
	git pull origin main