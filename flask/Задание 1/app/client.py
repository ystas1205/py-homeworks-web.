import requests

response = requests.post(
    "http://127.0.0.1:5000/announcement",
    json={"title": "title1", "user": "user1",
          "description": "description1"},
)

# response = requests.get(
#     "http://127.0.0.1:5000/announcement/1",
# )

# response = requests.patch(
#     "http://127.0.0.1:5000/announcement/1",
#     json={"title": "title2", "description": "description2",
#           "user": "user2"},
# )

# response = requests.delete(
#     "http://127.0.0.1:5000/announcement/3",
# )

print(response.status_code)
print(response.json())
