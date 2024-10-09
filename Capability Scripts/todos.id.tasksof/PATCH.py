import requests

# PATCH a specific todo
todo_id = "1"
data = {
    "id":"1"
    }
response = requests.patch(f"http://localhost:4567/todos/{todo_id}/tasksof", json=data)

if response.status_code == 201:
    print("Response Data:", response.json())
print("Status Code:", response.status_code)

