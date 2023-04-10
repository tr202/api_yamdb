# api_yamdb
api_yamdb
### Технологии
Python 3.9
Django 3.2.16
DRF 3.12.4
### Запуск проекта в dev-режиме
- Установите и активируйте виртуальное окружение
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- В папке с файлом manage.py выполните команды:
```
python3 manage.py migrate
python3 manage.py load_csv_data
python3 manage.py runserver
```
- Протестируйте однин из следующих запросов
```
http://127.0.0.1:8000/api/v1/auth/signup/
http://127.0.0.1:8000/api/v1/auth/token/
http://127.0.0.1:8000/api/v1/users/me/
```
