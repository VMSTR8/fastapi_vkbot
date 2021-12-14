# Callback чат-бот на FastApi
Чат-помощник для страйкбольной команды. Главная функция бота, это помощь новчикам и тем, кто только собирается
вступить в команду.

Бот настроен на работу с inline клавиатурой. Текстовые команды не воспринимает. Реагирует на любые попытки
достать его не нажатием на кнопки.

Умеет довольно таки простенько модерировать чат. Удаляет любые сообщения участников, если их нет в white
list или они не являются администраторами чата.

Разрабатывается функционал поиска по запросу на тематических барахолках площадки vk.com

Стэк: Python 3.8, FastAPi, SQLAlchemy, PostgreSQL
## Начало работы с проектом
Для начала активируем вирутальное окружение: 
```bash
$ source venv/bin/activate
```

А затем устанавливаем все зависимости:
```bash
$ pip install -r requirements.txt
```
## Миграции Alembic
Для миграций нам понадобится alembic, он уже установился с зависимостями. 

Чтобы инициализировать Alembic выполняем команду:
```bash
$ alembic init migrations
```
Эта команда создаст в текущей директории файл alembic.ini и каталог migrations содержащий:

 - каталог versions, в котором будут хранится файлы миграций
 - скрипт env.py, запускающийся при вызове alembic
 - файл script.py.mako, содержащий шаблон для новых миграций.

В репозитории уже залиты вышеперечисленные файлы. Они перенастроены так, чтобы credentials подтягивались из переменных.
Как это сделать, можно почитать по ссылке ниже:

[Переменные окружения для Python проектов](https://habr.com/ru/post/472674/)

Для понимания, что переделали. Во-первых, в файле alembic.ini в строке
```ini
sqlalchemy.url = postgresql://%(DB_USER)s:%(DB_PASSWORD)s@%(DB_HOST)s/%(DB_NAME)s
```
Использовали формат %(variable_name)s. Он позволит нам установить разные значения переменных в зависимости от
среды окружения переопределяя их в файле **env.py** например вот так:
```python
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from vkbot_sql.models import Base
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

section = config.config_ini_section

config.set_section_option(section, 'DB_USER', os.environ.get('DB_USER'))
config.set_section_option(section, 'DB_PASSWORD', os.environ.get('DB_PASSWORD'))
config.set_section_option(section, 'DB_HOST', os.environ.get('DB_HOST'))
config.set_section_option(section, 'DB_NAME', os.environ.get('DB_NAME'))
```
Дальше нужно сгенерировать миграции и обновить БД (поздразумевается, что вы подключили и настроили базу данных, 
чуть позже обновлю README с инструкцией поднятия и подключения postgresql).
```bash
$ alembic revision --autogenerate -m "my first migration"
$ alembic upgrade head
```
Иструкции по миграциям взяты из [статьи на Хабре](https://habr.com/ru/post/513328/). Примеры переделаны под текущий
проект.