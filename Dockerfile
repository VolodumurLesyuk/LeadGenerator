# Використовуємо офіційне зображення Python як базовий образ
FROM python:3.12.3

# Встановлення клієнта PostgreSQL
RUN apt-get update && apt-get install -y postgresql-client netcat-traditional

# Встановлення робочої директорії
WORKDIR /app

# Створення віртуального середовища
RUN python -m venv venv

# Активуємо віртуальне середовище і встановлюємо залежності
COPY requirements.txt .
RUN /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"


# Копіюємо всі файли проекту в контейнер
COPY . .


RUN #/bin/bash -c "source venv/bin/activate && python manage.py migrate"


#RUN cp /app/simple_calendar.py /app/venv/lib/python3.12/site-packages/aiogram_calendar/simple_calendar.py

RUN sed -i 's/^DATABASE_HOST=.*/DATABASE_HOST=db_web_form_container/' .env
# Вказуємо команду для запуску бота у віртуальному середовищі
#CMD ["sh", "-c", ". venv/bin/activate && python manage.py runserver"]

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Вказуємо команду для запуску сервера у віртуальному середовищі
CMD ["/entrypoint.sh"]


#CMD ["/bin/bash", "-c", "source venv/bin/activate && python manage.py runserver 0.0.0.0:8000"]
