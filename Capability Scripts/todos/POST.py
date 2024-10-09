import requests

# POST a specific todo
todo_data = {
    "title": "New Todo Title",
    "doneStatus": False,
    "description": "New todo description"
}
response = requests.post(f"http://localhost:4567/todos", json=todo_data)

print("Status Code:", response.status_code)
print("Response Data:", response.json())
