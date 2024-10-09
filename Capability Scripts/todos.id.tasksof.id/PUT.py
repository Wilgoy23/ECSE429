import requests

# PUT a specific todo
todo_id = "28"
project_id = "1"
data = {
    "title": "hello",
    "doneStatus": False,
    "description": "no"
    }
response = requests.put(f"http://localhost:4567/todos/{todo_id}/tasksof/{project_id}", json=data)

if response.status_code == 201:
    print("Response Data:", response.json())
print("Status Code:", response.status_code)
