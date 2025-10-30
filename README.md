# Bike Rental System

Система проката велосипедов с GUI и консольным интерфейсом.

## Функции
- Регистрация / вход
- Оренда велосипедов
- Управление станциями и велосипедами (менеджер)
- Звіти про доходи та попит
- Експорт/імпорт XML

## Запуск

```bash
pip install -r requirements.txt
python main.py
База данных

Создайте БД MySQL: bike_rental
Выполните database.sql
Создайте .env:

DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=bike_rental