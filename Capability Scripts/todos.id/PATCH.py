import requests

# PATCH a specific todo
todo_id = "1"
data = {
    "title": "hello",
    "doneStatus": False,
    "description": "no"
    }
response = requests.patch(f"http://localhost:4567/todos/{todo_id}", json=data)

if response.status_code == 201:
    print("Response Data:", response.json())
print("Status Code:", response.status_code)

