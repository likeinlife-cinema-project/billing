# Описание
Сервис для оповещения пользователя по:
   - email (smtp) - Готово
   - email (сторонний сервис) - В разработке
   - websocket - В разработке

# Запуск
1. Убедитесь, что RabbitMQ работает (make)
2. В `sample.env` нужно установить значения: `SMTP_LOGIN`, `SMTP_PASSWORD`
3. Запустите
   - Локально: `python src/main.py`, нужно сделать файл .env
   - В контейнере: docker build, docker run
4. Для теста можно сгенерировать сообщение:
   - Локально: `python src/produce_once.py`
   - В контейнере: `docker exec -it <id_container> python src/produce_once.py`