import requests

# POST a specific todo
todo_id = "2"
project_id = "1"
todo_data = {
    "id": "1"
}
response = requests.post(f"http://localhost:4567/todos/{todo_id}/tasksof/{project_id}", json=todo_data)

print("Status Code:", response.status_code)

