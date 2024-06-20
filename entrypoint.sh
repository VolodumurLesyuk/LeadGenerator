#!/bin/bash

# Активуємо віртуальне середовище
source venv/bin/activate

# Очікуємо запуск PostgreSQL
echo "Waiting for postgres..."
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

# Виконуємо міграції
python manage.py migrate
echo "Creating superuser..."

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'P@F98r-8cX7n&(*uR7-X-NM7bv85;Pbe')" | python manage.py shell

# Запускаємо сервер Django
exec python manage.py runserver 0.0.0.0:8000
