# api_yamdb
Данный проект создан в рамках курса Python Backend школы Yandex Practicum.
**API YaMDB** - это проект, который предоставляет REST API для работы с базой данных отзывов на фильмы, книги и музыку. В этой базе данных пользователи могут оставлять отзывы и комментарии, а также ставить оценки произведениям.

### Авторы
Студенты 55 когорты курсы [Python Backend](https://practicum.yandex.ru/profile/backend-developer/) школы Yandex Practicum.
- Анатолий Шерин: [github](https://github.com/AnatoliyPracticum)
- Геннадий Умикашвили: [github](https://github.com/Gennady-Umikashvili)
- Константин Волков : [github](https://github.com/tr202)

### Технологии
Python 3.9
Django 3.2.16
DRF 3.12.4

### Описание API
Redoc: http://127.0.0.1:8000/redoc/
или в [YAML файле](https://github.com/tr202/api_yamdb/blob/4d01d088f4191888bf62c20965f0f797a6285cf3/api_yamdb/static/redoc.yaml)

### Запуск проекта в dev-режиме
- Установите и активируйте виртуальное окружение
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- В папке с файлом manage.py:
Выполните миграцию БД и наполнение БД тестовыми данными:
```
python3 manage.py migrate
python3 manage.py load_csv_data
```
- Запустите приложение:
```
python3 manage.py runserver
```

- Протестируйте один из следующих запросов
```
http://127.0.0.1:8000/api/v1/auth/signup/
http://127.0.0.1:8000/api/v1/auth/token/
http://127.0.0.1:8000/api/v1/users/me/
```
