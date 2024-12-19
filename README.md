![Pipeline Status](https://gitlab.crja72.ru/django/2024/autumn/course/projects/team-4/badges/main/pipeline.svg)

# Kanhub - сайт для управления задачами

## Содержание
- [Введение](#введение)
  - [Существующие решения](#существующие-решения)
  - [Возможности kanhub](#с-kanhub-вы-можете)
- [Структура проекта](#структура-проекта)
  - [Стек технологий](#используемые-фреймворки--библиотеки)
  - [База данных](#база-данных)
- [Развёртывание](#развёртывание)
- [Авторы](#авторы)

## Введение
Kanhub представляет собой сервис для управления задачами


### Существующие решения
Это не новая идея и уже существуют множество сервисов с похожим функционалом,
вот их небольшой срез: 

| Сервис                                      | Отслеживание прогресса | Календарь | История изменений	 | Коллаборация | Русский язык | API  |
|---------------------------------------------|-------------|---------------------|------------|--------------|---------|---------|
| [trello.com](https://trello.com/)  	      | Да (+)      | Да ($)             | Нет (-)     | Да (+)       | Нет (-) | Да (+)  |
| [todo.microsoft.com](https://todo.microsoft.com/)                   | Нет (+)     | Да (+)             | Нет (-)     | Нет (-)       | Да (+) | Нет (-)  |
| [notion.so](https://notion.so/)             | Да (-)      | Да (+)              | Да ($)     | Да ($)      | Нет (-) | Да (+)  |
| [basecamp.com](https://basecamp.com/)        | Да (-)      | Нет (+)              | Да ($)     | Да ($)      | Нет (-)  | Да ($)  |
| [rebrandly.com](https://www.rebrandly.com/) | Нет (+)     | Да (+)              | Да (+)     | Нет (-)      | Нет (-) | Да (+)  |
| [meistertask.com](https://www.meistertask.com/)          | Да (+)     | Да ($)              | Нет (-)     | Да ($)      | Нет (-) | Да (+)  |

(+) - функция есть; (-) - функции нет; ($) - функция платна

Kanhub предоставляет пользователю весь этот функционал!

### С Kanhub вы можете:
- Создавать задачи и устанавливать дедлайны
- Просматривать и управлять задачами с помощью удобного календаря
- Отслеживать историю изменений задач, чтобы видеть, какие правки были внесены
- Организовывать задачи по тегам для лучшей структуризации
- Совместно работать над задачами с коллегами в режиме реального времени
- Подключать интеграции через API для автоматизации управления задачами

## Структура проекта
### Используемые фреймворки / библиотеки
- [Bootstrap](https://getbootstrap.com/) - популярная (html / css / js) 
  библиотека для фронтенда
- [Django](https://www.djangoproject.com/) - основной фреймворк web сервиса

### База данных
Функциональная структура базы данных следующая:
![scheme](ER.jpg)

## Развёртывание

### Клонируем проект

```
git clone https://gitlab.crja72.ru/django/2024/autumn/course/projects/team-4/
```

### Устанавливаем venv

```
python -m venv venv
```

### Активируем activate

```
source venv/bin/activate
```

### Устанавливаем зависимости

```
pip install -r requirements/prod.txt
pip install -r requirements/dev.txt
pip install -r requirements/test.txt
pip install -r requirements/flake8.txt
```

### Копируем env

```
copy .env.example .env
```

### Переходим в папку с manage.py

```
cd lyceum
```

### Настраиваем язык (django-admin makemessages)

```
django-admin makemessages -l en
django-admin makemessages -l ru
```

### Скомпилировать в двоичный язык (django-admin compilemessages)

```
django-admin compilemessages -l en
django-admin compilemessages -l ru
```

### Настраиваем миграции

```
python manage.py migrate
```

### Загружаем фикструры

```
python manage.py loaddata fixtures/data.json
```

### Сбор статики 

```
python manage.py collectstatic
```

### Тестирование проекта

```
python manage.py test
```

### Запускаем сервер 

```
python manage.py runserver
```

### Переходим на сайт

```
http://127.0.0.1:8000/
```

## Авторы:
<div style="display: flex; align-items: center;">
  <span style="margin-left: 10px;">Крахмальников Илья (<a href="https://github.com/124476">Github</a>)</span>
</div>
<br>
<div style="display: flex; align-items: center;">
  <span style="margin-left: 10px;">Хуснуллин Марсель (<a href="https://github.com/mario12508">Github</a>)</span>
</div>
<br>
<div style="display: flex; align-items: center;">
  <span style="margin-left: 10px;">Тараненко Максим (<a href="https://github.com/maxpawgdbs">Github</a>)</span>
</div>