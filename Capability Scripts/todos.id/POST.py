import requests

# POST a specific todo
todo_id = "1"
todo_data = {
    "doneStatus": True
}
response = requests.post(f"http://localhost:4567/todos/{todo_id}", json=todo_data)

print("Status Code:", response.status_code)
print("Response Data:", response.json())
