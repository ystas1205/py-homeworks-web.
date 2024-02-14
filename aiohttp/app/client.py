import requests

# регестрация пользователя и получения токена
response = requests.post(
    "http://127.0.0.1:8080/registration",
    json={"password": "12345678", "email": 'email',
          "user": "user1"},
)

# # создание обьявление авторизованым пользователем
# response = requests.post(
#     "http://127.0.0.1:8080/announcement",
#     json={"title": "title1", "description": 'descriptions1', "user_id": 1},
# )

# response = requests.get(
#     "http://127.0.0.1:8080/announcement/11",
# )

# # удаление обьявление владельцем
# response = requests.delete(
#     "http://127.0.0.1:8080/announcement/10",
#     headers={"token": "c4ca02f0-3f28-4d07-8c76-16ec9842020d"}
# )
# # замена обьявление владельцем
# response = requests.patch(
#     "http://127.0.0.1:8080/announcement/1",
#     json={"title": "title2", "description": 'descriptions2'},
#     headers={"token": "e5da503c-d737-412c-87c0-cca9fc0bb881"}
# )
print(response.status_code)
print(response.text)
