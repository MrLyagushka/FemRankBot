# Игнорируем файлы с такими же именами, как команды
.PHONY: help install reload start stop logs status clean db-clean db-update update

# Команда по умолчанию (срабатывает, если написать просто "make")
.DEFAULT_GOAL := help

help: ## ℹ️ Показать эту справку со списком команд
	@echo "Доступные команды:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## 🚀 Первичная установка (запуск install.sh)
	@chmod +x install.sh
	@bash install.sh

reload: ## 🔄 Пересборка и перезапуск контейнеров (применит новый код) с git pull и logs
	@echo "🗃️ Скачиваем обновление с github репозитория"
	git pull origin main
	@echo "🏗 Собираем новую версию основного бота (это может занять время)..."
	docker compose build bot_dzshka
	@echo "🚀 Запускаем обновленного бота..."
	docker compose up -d bot_dzshka
	@echo "✅ Обновление завершено! Бот снова в строю."
	@echo "📋 Вывод логов..."
	docker compose logs -f

reload-no-logs: ## 🔄 Пересборка и перезапуск контейнеров (применит новый код) с git pull без logs
	@echo "🗃️ Скачиваем обновление с github репозитория"
	git pull origin main
	@echo "🏗 Собираем новую версию основного бота (это может занять время)..."
	docker compose build bot_dzshka
	@echo "🚀 Запускаем обновленного бота..."
	docker compose up -d bot_dzshka
	@echo "✅ Обновление завершено! Бот снова в строю."

reload-no-git-pull-no-logs: ## 🔄 Пересборка и перезапуск контейнеров (применит новый код) без git pull без logs
	@echo "🏗 Собираем новую версию основного бота (это может занять время)..."
	docker compose build bot_dzshka
	@echo "🚀 Запускаем обновленного бота..."
	docker compose up -d bot_dzshka
	@echo "✅ Обновление завершено! Бот снова в строю."

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

update: ## Обновление с git репозетория
	git pull origin main

db-update: ## 🗃️ Автоматически добавить новые столбцы/таблицы из .sql шаблонов
	@echo "🗃️ Запуск умной синхронизации баз данных..."
	docker compose run --rm bot_dzshka python db_sync.py