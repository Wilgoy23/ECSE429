import requests

# GET a specific todo
todo_id = "1"  # Example ID
project_id = "1"
data = {
    "id": "1"
    }
response = requests.get(f"http://localhost:4567/todos/{todo_id}/tasksof/{project_id}")

print("Status Code:", response.status_code)
