# Набір потрібних команд для цього проекту

+ 1 ```docker container inspect website``` - тут подивимось детально інфу про конретний контейнер - ```website```
+ 2  ```docker build -t web:source_site_0_07 .``` - це для створення нового імейджа для докер компоуса. Дивитися детальніше в docker-compose.yml
+ 3 ```docker rm website db_web_form_container``` - це ми видаляємо контейнера. Головне щоб вони були зупинені(Зупинити можна в залежності яким чином вони були запущені якщо через docker compose up&& docker compose start -> docker compose stop)
+ 4 ```docker volume rm leadgenerator_website_data leadgenerator_web_form_db``` це видалення volume які монтуються в дерикторії докера, і підтягують дані при запуску контейнера
+ 5 ```docker compose up --build``` - ця команда остання поки в переліку, вона запустить перелічені в docker-compose.yml контейнера 