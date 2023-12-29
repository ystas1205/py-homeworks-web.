# # Домашнее задание к лекции «Docker»
# Задание 1

Создание образа: docker build -t file_html .

Запуск контейнера: docker run -v "${PWD}:/usr/share/nginx/html" -p 8090:80 -d html

# Задание 2

Создание образа: docker build -t django_project .

Запуск контейнера: docker run --name=django_test -d -p 8000:8000 django_project

Браузер http://localhost:8000/api/v2/