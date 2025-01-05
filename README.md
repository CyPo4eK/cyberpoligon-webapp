Простое веб приложение на Django.

Подверженно RCE уязвимости

Для запуска необходимо настроить settings.py (указать allowed_hosts и креды базы данных).
```bash
cp myproject/settings.py.example myproject/settings.py
```

Запуск:
`docker compose up -d --build`

Миграции:
```bash
docker compose exec -it webapp python manage.py makemigrations
docker compose exec -it webapp python manage.py migrate
docker compose exec -it webapp python manage.py createsuperuser
```
1. Создаем миграции
2. Выполняем миграцию
3. Создаем пользователя

В приложении реализована система одноразовых паролей. После ввода логина и пароля в веб интерфейсе, можно прочитать логи прложения при помощи команды `docker compose logs webapp`. Там должен появится одноразовый код для входа в систему.
