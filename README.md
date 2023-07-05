# Тестовое задание на позицию: «Разработчик Python (Junior)».

## 1 задача. Python, scraping, PostgreSQL:

- Извлечь данные с сайта https://nedradv.ru/nedradv/ru/auction и сохранить их в базе данных PostgreSql:
    - Требования к данным:
        - Дата
        - Участок
        - Регион
        - Статус
        - Срок подачи заявок
        - Взнос за участие в аукционе
        - Организатор
- Создайть схему БД с необходимыми таблицами и полями для хранения извлечённых данных.
- Написать скрипт для вставки данных в БД (убедитесь, что скрипт обрабатывает ошибки и исключения, которые могут возникнуть в процессе вставки данных).
- Протестировать парсер на нескольких страницах сайта, чтобы убедиться, что он может обрабатывать различные форматы и макеты.
- Сформировать краткий отчёт с описанием предпринятых шагов и проблем, возникших в процессе выполнения задания.

Результат выполнения задания: скрипт для извлечения с сайта и вставки в БД PostgreSql указанных данных, краткий отчёт о выполненном задании.

Дополнительно (необязательно):
Оптимизируйте парсер для сокращения времени извлечения данных и добавьте в отчёт предпринятые шаги и проблемы, с которыми столкнулись при оптимизации.

## 2 задача. SQL

Дано 2 таблицы:
![Alt text](image.png)

- Сформировать SQL-запросы, позволяющие получить:
    - Список, содержащий ФИО и время разговора по суткам
    - Список звонков, где время разговора за сутки больше 5 минут
    - Список звонков, где перерывы между звонками не более 5 минут
    - Список, содержащий информацию по абонентам:
        - количество звонков в день
        - средняя и медиана разговора в минутах
        - размах по времени разговора

## Установка и запуск проекта

### Для запуска проекта необходимо:

- Python версии 3.11
- склонировать репозиторий консольной командой `git clone git@github.com:vaniamaksimov/scraping_sql_testwork.git`
- перейти в папку с проектом консольной командой `cd scraping_sql_testwork`
- выполнить команду `mv .env.example .env`
- установить зависимости с помощью poetry https://python-poetry.org/docs/basic-usage/ или воспользоваться пакетным менеджером pip, для этого:
    - устанавливаем виртуальное окружение командой `python -m venv venv` или `python3 -m venv venv` на unix системах
    - активируем виртуальное окружение командой `source venv/scripts/activate` или `source venv/bin/activate` на unix системах
    - устанавливаем зависимости командой `pip install -r requirements.txt`
- для поднятия базы данных я рекомендую воспользоваться Docker https://docs.docker.com/desktop/install/
- команда для поднятия контейнера с базой данных: `docker run --env=POSTGRES_PASSWORD=postgres --env=POSTGRES_USER=postgres --env=POSTGRES_DB=postgres --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/lib/postgresql/15/bin --env=PGDATA=/var/lib/postgresql/data --volume=/var/lib/postgresql/data -p 5432:5432 -d postgres:15-alpine`
- применить миграции, для этого в корне проекта выполнить консольную команду `alembic upgrade head`
- для запуска парсера в корне проекта выполнить консольную команду `scrapy crawl auctions`

Парсер имеет настройку DOWNLOAD_DELAY = 2.5, для ускорения работы парсера следует уменьшить это число в разумных пределах.

### Отчет о выполнении задания:

1. Выбор инструмента парсинга:

    - для выбора инструмента парсинга мне потребовалось изучить страницу с данными. Получив необходимую информацию о структуре сайта я остановил свой выбор на фреймворке Scrapy. Из приемуществ данного фреймворка: асинхронность, широкие возможности по настройке парсера, несколько вариантов вывода данных.

2. Проблемы при парсинге данных:

из основных проблем при парсинге и сохранении данных в бд можно выделить

    - несогласованность данных на сайте.
        * У многих аукционов отсуствуют регионы
        * У некоторых аукционов отсуствует или некоректно указан статус
        * У некоторых аукционов остуствует срок подачи заявок
        * Время начала аукциона указано по разному (По Московому времени, по местному времени, и т.д.)