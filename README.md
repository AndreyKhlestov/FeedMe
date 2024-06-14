# Проект FeedMe Bot

## Описание

### Телеграм-Бот для Фонда Защиты Городских Животных.
Телеграм-бот, который позволяет автоматизировать процесс сбора, передачи и выгрузки информации для участников проекта "Накорми", а также будет формирует отчетную информацию. 

Функционал телеграм-бота:
- для волонтера: регистрация информации о получении и расходе корма (получение корма на точке сбора, кормление животных, передача корма другому волонтеру,  доступ в личный кабинет)
- для администратора: контроль за перемещением корма, статистика поступления и расхода корма

## Технологии
[![Python](https://img.shields.io/badge/python-3.11-blue?logo=python)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.4-blue)](https://docs.aiogram.dev/en/latest/)
[![Django](https://img.shields.io/badge/Django-4.2-blue?logo=python)](https://www.python.org/)
[![aiosqlite](https://img.shields.io/badge/PostgreSQL-blue)](https://www.postgresql.org/docs/)
[![APScheduler](https://img.shields.io/badge/APScheduler-blue)](https://docs-python.ru/packages/modul-apscheduler-python/)
![Redis](https://img.shields.io/badge/Redis-blue)
[![Loguru](https://img.shields.io/badge/Loguru-blue)](https://loguru.readthedocs.io/en/stable/)


## Запуск проекта локально

Клонируйте репозиторий и перейдите в него:

```
git clone https://github.com/AndreyKhlestov/FeedMe
cd FeedMe
```

Создайте виртуальное окружение:
```
py -3.11 -m venv venv
```
Активируйте виртуальное окружение:
```
Windows: source venv/Scripts/activate
Linux/macOS: source venv/bin/activate
```
Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
В корне проекта создайте файл .env и поместите в него:
```
# Переменные для PostgreSQL
POSTGRES_DB=test_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Переменные для Django-проекта (учетная запись аминистратора создается автоматически) :
SECRET_KEY='django-insecure-7f8jl#&fox9p+zm7@e2!8q66&+%+ex94vwe4razd8t5x+g5!qk'
DEBUG=False
HOST_IP='ip вашего сервера'
SUPER_USER_NAME=<имя админа>
SUPER_USER_PASS=<пароль админа>

# Переменные для телеграм ботa
BOT_TOKEN=<ваш токен для бота>
REDIS_HOST=redis - для локального запуска эту переменную нужно закомментировать
REDIS_PORT=6379 - для локального запуска эту переменную нужно закомментировать
```
Создайте базу данных, применив миграции (из корня проекта):
```
python django_app.py makemigrations
python django_app.py migrate
```
Запустите бота (из корня проекта):
```
python bot.py
```
В отдельном терминале запустите админ панель (из корня проекта)
```
python django_app.py runserver
```
## Запуск проекта на сервере
Клонируйте репозиторий на сервер и перейдите в него:
```
git clone https://github.com/AndreyKhlestov/FeedMe
cd FeedMe
```
В корневой директории проекта <ваш_сервер>/:~FeedMe создайте файл с переменными окружения .env и заполните его по образцу выше
```
sudo nano .env
```
Запускаем Docker-compose и проверяем на наличие ошибок
```
sudo docker-compose up
```
Закрываем подключение, чтобы не останавлиать контенеры и подключаемся снова к серверу;

Переходим в директорию с проектом и заходим в запущенный Docker контейнер
```
sudo docker-compose exec backend bash
```
Можно проверять работу бота и админ панели (перейдя по ссылке типа http://ip_вашего_сервера/)

### Обращаем Ваше внимание, что BOT_TOKEN вы должны получить заранее самостоятельно при создании и регистрации бот-чата в телеграм сервисе по созданию ботов https://t.me/BotFather

## Команда разработки
[Андрей Хлестов](https://github.com/AndreyKhlestov) (тимлид команды)

[Константин Стеблев](https://github.com/KonstantinSKS) (разработчик)

[Илья Фабиянский](https://github.com/fabilya)  (разработчик)

[Татьяна Мусатова](https://github.com/Tatiana314) (разработчик)

[Анна Победоносцева](https://github.com/ZebraHr) (разработчик)


