import requests

# # регестрация пользователя и получения токена
# response = requests.post(
#     "http://127.0.0.1:5000/registration",
#     json={"password": "123456789", "email": "email2",
#           "user": "user2"},
# )
#
# # создание обьявление авторизованым пользователем
# response = requests.post(
#     "http://127.0.0.1:5000/announcement",
#     json={"title": "title1", "description": 'descriptions1', "user_id": 2},
# )

# response = requests.get(
#     "http://127.0.0.1:5000/announcement/1",
# )

# # удаление обьявление владельцем
# response = requests.delete(
#     "http://127.0.0.1:5000/announcement/2",
#     headers={"token": "8696ed70-7b52-4c48-be56-26d2f75a934c"}
# )

# изменение обьявление владельцем
response = requests.patch(
    "http://127.0.0.1:5000/announcement/1",
    json={"title": "title2", "description": "description2"},
    # headers={"token": "d3b63722-60cf-4ed2-bbb6-49b4a040410d"}
)

print(response.status_code)
print(response.json())
