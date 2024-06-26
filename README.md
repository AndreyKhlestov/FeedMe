# Проект FeedMe Bot

## Описание

### Телеграм-Бот для Фонда Защиты Городских Животных.
Телеграм-бот, который позволяет автоматизировать процесс сбора, передачи и выгрузки информации для участников проекта "Накорми", а также формирует отчетную информацию. 

Функционал телеграм-бота:
- для волонтера: регистрация информации о получении и расходе корма (получение корма на точке сбора, кормление животных, передача корма другому волонтеру,  доступ в личный кабинет)
- для администратора: контроль за перемещением корма, статистика поступления и расхода корма

## Технологии
[![Python](https://img.shields.io/badge/python-3.11-blue?logo=python)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.4-blue)](https://docs.aiogram.dev/en/latest/)
[![Django](https://img.shields.io/badge/Django-4.2-blue?logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgeSQL-blue?logo=postgresql)](https://www.postgresql.org/docs/)
[![Docker](https://img.shields.io/badge/Docker-blue?logo=Docker)](https://docs.docker.com/)
[![APScheduler](https://img.shields.io/badge/APScheduler-blue)](https://docs-python.ru/packages/modul-apscheduler-python/)
![Redis](https://img.shields.io/badge/Redis-blue)
[![Loguru](https://img.shields.io/badge/Loguru-blue)](https://loguru.readthedocs.io/en/stable/)
[![Boto3](https://img.shields.io/badge/Boto3-blue)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
[![Django-storages](https://img.shields.io/badge/Django_storages-blue)](https://django-storages.readthedocs.io/en/latest/index.html)

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
В корневой директории проекта переименуйте файл с переменными окружения .env.template в .env, уберите комментарии и заполните недостающие поля:
```
HOST_IP - замените id-адрес сервера на адрес сервера, на котором устанавливается бот.
ВАЖНО! Ваш домен должен быть доступен по протоколу https!
BOT_TOKEN - укажите токен вашего бота
SUPER_USER_NAME и SUPER_USER_PASS - логин и пароль администратора Django (для автоматического создания в системе)
POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD - можно менять на ваше усмотрение или оставить как есть
REDIS_HOST=redis - для локального запуска эту переменную нужно закомментировать
REDIS_PORT=6379 - для локального запуска эту переменную нужно закомментировать

Остальные поля не менять, если вы не разбираетесь в коде
```
Создайте базу данных, применив миграции (из корня проекта):
```
python django_app.py makemigrations
python django_app.py migrate
```
### Настройте ngrok:
1. Перейдите на официальный сайт ngrok: [ngrok.com](https://ngrok.com/)
2. Зарегистрируйтесь или войдите в свою учетную запись.
3. Скачайте ngrok для вашей операционной системы и распакуйте архив.
4. Авторизуйтесь в ngrok:
```
ngrok authtoken YOUR_AUTH_TOKEN - токен вы получите при регистрации
```
5. Запустите ngrok для вашего локального сервера
```
ngrok http http://localhost:8000
```
В результате выполнения команды вы получите публичный URL, который будет перенаправлять запросы на ваш локальный сервер. Например:
```
Forwarding                    https://12345678.ngrok.io -> http://localhost:8000
```
6. Добавьте полученный URL в файл .env. Например:
```
HOST_IP='12345678.ngrok.io'
```
Запустите бота (из корня проекта):
```
python bot.py
```
В отдельном терминале запустите админ панель (из корня проекта)
```
python django_app.py runserver
```
Админ панель будет доступна по адресу, полученному через ngrok
## Запуск проекта на сервере
Клонируйте репозиторий на сервер и перейдите в него:
```
git clone https://github.com/AndreyKhlestov/FeedMe
cd FeedMe
```
В корневой директории проекта <ваш_сервер>/:~FeedMe переименуйте файл с переменными окружения .env.template в .env и внесите правки согласно инструкции выше

Запускаем Docker-compose и проверяем на наличие ошибок
```
sudo docker-compose up
```
Можно проверять работу бота и админ панели (перейдя по ссылке типа https://ip_вашего_сервера/)

### Обращаем Ваше внимание, что BOT_TOKEN вы должны получить заранее самостоятельно при создании и регистрации бот-чата в телеграм сервисе по созданию ботов https://t.me/BotFather


## Команда разработки
[Андрей Хлестов](https://github.com/AndreyKhlestov) (тимлид команды)

[Константин Стеблев](https://github.com/KonstantinSKS) (разработчик)

[Илья Фабиянский](https://github.com/fabilya)  (разработчик)

[Татьяна Мусатова](https://github.com/Tatiana314) (разработчик)

[Анна Победоносцева](https://github.com/ZebraHr) (разработчик)


