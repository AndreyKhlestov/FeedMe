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
[![APScheduler](https://img.shields.io/badge/APScheduler-blue)](https://docs-python.ru/packages/modul-apscheduler-python/)
![Redis](https://img.shields.io/badge/Redis-blue)
[![Loguru](https://img.shields.io/badge/Loguru-blue)](https://loguru.readthedocs.io/en/stable/)


## Запуск проекта на сервере
Клонируйте репозиторий на сервер и перейдите в него:
```
git clone https://github.com/AndreyKhlestov/FeedMe
cd FeedMe
```
В корневой директории проекта <ваш_сервер>/:~FeedMe переименуйте файл с переменными окружения .env.template в .env, уберите комментарии и заполните недостающие поля:

в ALLOWED_HOSTS замените id-адрес сервера на адрес сервера, на котором устанавливается бот
в BOT_TOKEN укажите токен вашего бота
SUPER_USER_NAME и SUPER_USER_PASS - логин и пароль администратора Django (для автоматического создания в системе)
POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD - можно менять на ваше усмотрение или оставить как есть
остальные поля не менять, если вы не разбираетесь в коде

Запускаем Docker-compose и проверяем на наличие ошибок
```
sudo docker-compose up
```
Можно проверять работу бота и админ панели (перейдя по ссылке типа http://ip_вашего_сервера/)

### Обращаем Ваше внимание, что BOT_TOKEN вы должны получить заранее самостоятельно при создании и регистрации бот-чата в телеграм сервисе по созданию ботов https://t.me/BotFather

## Команда разработки
[Андрей Хлестов](https://github.com/AndreyKhlestov) (тимлид команды)

[Константин Стеблев](https://github.com/KonstantinSKS) (разработчик)

[Илья Фабиянский](https://github.com/fabilya)  (разработчик)

[Татьяна Мусатова](https://github.com/Tatiana314) (разработчик)

[Анна Победоносцева](https://github.com/ZebraHr) (разработчик)


